"""Non-generative 4x enlargement and hand-traced background mask.

Facial pixels are only resampled with Lanczos; no face restoration or retouch.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from scipy.interpolate import splprep, splev

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('/home/powerhouse2/Pictures/Screenshots/Screenshot from 2026-11-19 11-25-48.png')
original = Image.open(SOURCE).convert('RGB')
w,h = original.size
scale = 4
# Trace the actual blurred silhouette, including both ears and shoulders.
points = np.float64([
 (0,584),(8,559),(19,533),(28,510),(37,483),(48,463),
 (64,446),(86,432),(111,418),(140,403),(166,390),
 (187,378),(191,365),(196,352),(209,346),(212,333),
 (212,313),(210,297),(204,287),(198,282),(188,278),(179,269),
 (173,254),(169,241),(166,229),(170,219),(178,216),
 (185,222),(185,213),(183,202),(182,187),(181,173),
 (177,154),(179,141),(184,127),(190,115),(191,101),
 (196,90),(209,82),(224,76),(239,72),(254,70),
 (270,73),(289,76),(307,81),(323,88),(337,97),
 (348,108),(356,123),(361,140),(365,160),(367,181),
 (366,200),(366,211),(373,209),(376,218),(376,232),
 (378,246),(377,259),(372,270),(363,273),(359,282),
 (354,300),(352,320),(352,340),(357,353),(368,366),
 (387,379),(410,387),(435,397),(461,407),(483,420),
 (498,435),(508,455),(516,480),(522,508),(528,535),
 (534,559),(538,584),(400,590),(200,590),(0,584)
])
tck,_ = splprep(points.T, s=1.5, per=True)
curve = np.array(splev(np.linspace(0,1,4000),tck)).T
mask = np.zeros((h*scale,w*scale),np.uint8)
cv2.fillPoly(mask,[np.round(curve*scale).astype(np.int32)],255)
# Match the source's soft focus rather than adding a hard cutout boundary.
mask = cv2.GaussianBlur(mask,(0,0),2.8)
enlarged = np.asarray(original.resize((w*scale,h*scale),Image.LANCZOS))
alpha = mask.astype(np.float32)/255
result = np.round(enlarged.astype(np.float32)*alpha[...,None]).astype(np.uint8)
out = ROOT/'output/portraits';out.mkdir(exist_ok=True,parents=True)
Image.fromarray(result).save(out/'original-upscaled-black-background.png')
Image.fromarray(result).save(out/'original-upscaled-black-background.jpg',quality=97,subsampling=0)
Image.fromarray(np.dstack([enlarged,mask]),'RGBA').save(out/'original-upscaled-transparent.png')
Image.fromarray(mask).save(out/'original-upscaled-background-mask.png')
# Exact check: every fully opaque foreground pixel equals ordinary upscaling.
assert np.array_equal(result[mask==255],enlarged[mask==255])
assert np.all(mask[150*scale:310*scale,215*scale:345*scale]==255)
Image.fromarray(result).resize((w,h),Image.LANCZOS).save(out/'original-black-background-preview.png')
print(f'Saved {w*scale} x {h*scale}; all opaque subject pixels equal the unretouched Lanczos enlargement.')
