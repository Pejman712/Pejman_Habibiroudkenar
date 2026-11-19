"""Straighten the original glasses with a localized, conventional photo edit.

Only the existing frame pixels are rotated. OpenCV inpainting repairs their
old position; the original eyes, face, hair and expression are not replaced.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parent.parent
original=ImageOps.exif_transpose(Image.open(ROOT/'pics/misc/20260626_171510.jpg')).convert('RGB')
base=np.asarray(original).copy()
# Work on a small crop so the edit cannot affect the rest of the photograph.
x0,y0,x1,y1=1160,430,1470,580
patch=base[y0:y1,x0:x1].copy()
mask=np.zeros(patch.shape[:2],np.uint8)
def stroke(points,width):
    pts=np.int32(points)-[x0,y0]
    # Smooth an annotated centerline into a continuous frame curve.
    from scipy.interpolate import splprep,splev
    tck,_=splprep(pts.T,s=0,k=min(3,len(points)-1))
    smooth=np.array(splev(np.linspace(0,1,200),tck)).T
    cv2.polylines(mask,[np.round(smooth).astype(np.int32)],False,255,width,cv2.LINE_AA)

stroke([(1200,490),(1207,480),(1225,474),(1248,466)],7)
stroke([(1248,466),(1263,460),(1278,458),(1294,461),(1310,468),(1325,478),(1332,486)],6)
stroke([(1249,470),(1251,493),(1256,513),(1266,526),(1281,532),(1297,533),(1313,527),(1325,516),(1331,501),(1332,486)],6)
stroke([(1332,483),(1341,482),(1349,485),(1358,487)],5)
stroke([(1358,487),(1370,480),(1386,477),(1403,478),(1419,484),(1431,495)],6)
stroke([(1359,488),(1358,504),(1362,523),(1372,537),(1386,545),(1400,546),(1414,541),(1427,528),(1433,510),(1431,495)],6)
stroke([(1431,495),(1437,496),(1439,501)],5)

# A modest correction retains the photograph's natural head angle.
rotation=cv2.getRotationMatrix2D((1345-x0,487-y0),5.5,1.0)
source_alpha=cv2.GaussianBlur(mask,(0,0),.65).astype(np.float32)/255
premultiplied=patch.astype(np.float32)*source_alpha[...,None]
new_alpha=cv2.warpAffine(source_alpha,rotation,(patch.shape[1],patch.shape[0]),flags=cv2.INTER_CUBIC)
new_alpha=np.clip(new_alpha,0,1)
rotated=cv2.warpAffine(premultiplied,rotation,(patch.shape[1],patch.shape[0]),flags=cv2.INTER_CUBIC)
remove=cv2.dilate(mask,np.ones((5,5),np.uint8))
clean=cv2.inpaint(patch,remove,3,cv2.INPAINT_TELEA)
composite=np.uint8(np.clip(rotated+clean*(1-new_alpha[...,None]),0,255))
base[y0:y1,x0:x1]=composite
out=ROOT/'output/portraits';out.mkdir(parents=True,exist_ok=True)
Image.fromarray(base).save(out/'original-glasses-straightened.png')
Image.fromarray(base).save(out/'original-glasses-straightened.jpg',quality=96,subsampling=0)
preview=Image.new('RGB',(900,600),(16,19,19))
for i,im in enumerate([original,Image.fromarray(base)]):
    crop=im.crop((1150,315,1470,715)).resize((450,560),Image.LANCZOS)
    preview.paste(crop,(i*450,40))
draw=ImageDraw.Draw(preview)
draw.text((15,14),'Original photo',fill='white')
draw.text((465,14),'Original photo - glasses adjusted',fill='white')
preview.save(out/'original-glasses-comparison.jpg',quality=95)
outside=np.ones(base.shape[:2],bool);outside[y0:y1,x0:x1]=False
assert np.array_equal(base[outside],np.asarray(original)[outside])
print('Saved original photo with localized glasses correction; rest of photograph unchanged in PNG.')
