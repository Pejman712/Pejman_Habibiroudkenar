"""Small conventional frame correction and side sweep of existing hair pixels."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import splprep, splev

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('/home/powerhouse2/Pictures/Screenshots/Screenshot from 2026-11-19 10-38-08.png')
original = np.asarray(Image.open(SOURCE).convert('RGB'))
result = original.copy()

# Rotate only the frame; retain the existing lens reflections and eyes.
x0, y0, x1, y1 = 252, 265, 538, 367
patch = original[y0:y1, x0:x1].copy()
mask = np.zeros(patch.shape[:2], np.uint8)
def stroke(points, width):
    points = np.array(points, dtype=float) - (x0, y0)
    tck, _ = splprep(points.T, s=0, k=min(3, len(points)-1))
    curve = np.array(splev(np.linspace(0, 1, 250), tck)).T
    cv2.polylines(mask, [np.round(curve).astype(np.int32)], False, 255, width, cv2.LINE_AA)

stroke([(265,303),(280,299),(295,296),(309,290)], 5)
stroke([(309,291),(319,282),(337,274),(353,274),(374,280),(390,287),(399,295)], 4)
stroke([(309,291),(310,315),(317,337),(331,352),(350,357),(371,352),(388,338),(398,316),(399,295)], 3)
stroke([(399,291),(407,289),(418,289),(428,291)], 4)
stroke([(428,291),(442,281),(460,277),(480,278),(500,285),(514,298)], 4)
stroke([(428,291),(427,315),(433,335),(449,351),(470,355),(491,347),(506,331),(514,312),(514,298)], 3)
stroke([(514,298),(520,299),(527,301)], 4)

alpha = cv2.GaussianBlur(mask, (0,0), .55).astype(np.float32)/255
matrix = cv2.getRotationMatrix2D((411-x0, 291-y0), 1.7, 1)
size = (patch.shape[1], patch.shape[0])
new_alpha = np.clip(cv2.warpAffine(alpha, matrix, size, flags=cv2.INTER_CUBIC), 0, 1)
frame = cv2.warpAffine(patch.astype(np.float32)*alpha[...,None], matrix, size, flags=cv2.INTER_CUBIC)
clean = cv2.inpaint(patch, cv2.dilate(mask, np.ones((3,3),np.uint8)), 2, cv2.INPAINT_TELEA)
result[y0:y1,x0:x1] = np.clip(frame + clean*(1-new_alpha[...,None]),0,255).astype(np.uint8)

# Smooth displacement field shifts the upper strands to the viewer's left.
# Fixed lower boundary protects forehead, eyebrows, and facial features.
hy0, hy1, hx0, hx1 = 80, 246, 225, 550
hair = original[hy0:hy1,hx0:hx1]
yy, xx = np.mgrid[hy0:hy1, hx0:hx1].astype(np.float32)
vertical = np.maximum(0, np.sin(np.pi*(yy-hy0)/(hy1-hy0)))**2
horizontal = np.maximum(0, np.sin(np.pi*(xx-hx0)/(hx1-hx0)))**2
weight = vertical*horizontal
shift = 18*weight
mapx = xx-hx0+shift
mapy = yy-hy0-2.5*weight
swept = cv2.remap(hair,mapx,mapy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
result[hy0:hy1,hx0:hx1] = swept

out = ROOT/'output/portraits'
out.mkdir(exist_ok=True, parents=True)
Image.fromarray(result).save(out/'pejman-glasses-side-sweep.png')
Image.fromarray(result).save(out/'pejman-glasses-side-sweep.jpg', quality=97, subsampling=0)
preview = Image.new('RGB',(900,590),(22,24,25))
for i, arr in enumerate([original,result]):
    crop = Image.fromarray(arr).crop((220,75,555,485)).resize((450,550),Image.LANCZOS)
    preview.paste(crop,(450*i,40))
draw = ImageDraw.Draw(preview)
draw.text((15,14),'Original',fill='white')
draw.text((465,14),'Glasses adjusted + subtle side sweep',fill='white')
preview.save(out/'pejman-retouch-comparison.jpg',quality=96)
print(out/'pejman-glasses-side-sweep.png')
