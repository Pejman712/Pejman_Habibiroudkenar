"""Blend the approved portrait face into the original event photograph.

Conventional affine alignment, color transfer and a feathered mask only.
No image-generation models. The source photograph is never overwritten.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
original = ImageOps.exif_transpose(Image.open(ROOT/'pics/misc/20260626_171510.jpg')).convert('RGB')
face = Image.open(ROOT/'assets/images/pejman-hero-v7.png').convert('RGB')
base = np.asarray(original).copy()
height, width = base.shape[:2]
scale = np.array([width/1600, height/1385], dtype=np.float32)
source_points = np.float32([[797,249],[910,251],[850,445]])
target_points = np.float32([[761,291],[819,297],[785,390]]) * scale
transform = cv2.getAffineTransform(source_points, target_points)
warped = cv2.warpAffine(np.asarray(face), transform, (width,height), flags=cv2.INTER_CUBIC)
source_mask = np.zeros((face.height, face.width), np.uint8)
outline = np.int32([[708,245],[718,205],[742,174],[780,154],[835,144],
                    [895,151],[939,176],[969,209],[982,251],[977,304],
                    [960,354],[937,395],[904,428],[870,447],[838,450],
                    [804,441],[770,420],[744,391],[723,351],[708,304]])
cv2.fillPoly(source_mask,[outline],255)
mask = cv2.warpAffine(source_mask,transform,(width,height),flags=cv2.INTER_LINEAR)
mask = cv2.GaussianBlur(mask,(0,0),3.5)
alpha = mask.astype(np.float32)[...,None]/255

# Work in Lab: use the original event's skin chroma and broad lighting while
# retaining the approved face's eyes, glasses and expression.
lab_base = cv2.cvtColor(base,cv2.COLOR_RGB2LAB).astype(np.float32)
lab_face = cv2.cvtColor(warped,cv2.COLOR_RGB2LAB).astype(np.float32)
light_difference = cv2.GaussianBlur(lab_base[:,:,0]-lab_face[:,:,0],(0,0),18)
matched = lab_face.copy()
matched[:,:,0] = np.clip(lab_face[:,:,0]+light_difference,0,255)
matched[:,:,1:] = cv2.GaussianBlur(lab_base[:,:,1:],(0,0),7)
colored = cv2.cvtColor(np.uint8(np.clip(matched,0,255)),cv2.COLOR_LAB2RGB)
result = np.uint8(np.clip(colored*alpha+base*(1-alpha),0,255))
assert np.array_equal(result[mask==0],base[mask==0])
out = ROOT/'output/portraits'
out.mkdir(parents=True,exist_ok=True)
Image.fromarray(result).save(out/'original-with-final-face.png')
Image.fromarray(result).save(out/'original-with-final-face.jpg',quality=96,subsampling=0)
Image.fromarray(mask).save(out/'face-composite-mask.png')

box = tuple(np.int32(np.array([670,175,880,425])*np.tile(scale,2)))
comparison = Image.new('RGB',(840,540),(16,19,19))
for i,im in enumerate([original,Image.fromarray(result)]):
    crop=im.crop(box).resize((420,500),Image.LANCZOS)
    comparison.paste(crop,(i*420,40))
draw=ImageDraw.Draw(comparison)
draw.text((20,12),'Original',fill='white')
draw.text((440,12),'Edited face composite',fill='white')
comparison.save(out/'face-comparison.jpg',quality=94)
print('Saved full-resolution PNG and JPEG; all pixels outside the face mask are unchanged in the PNG.')
