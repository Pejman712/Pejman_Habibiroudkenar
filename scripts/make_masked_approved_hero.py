"""Mask the approved color portrait and place its grayscale pixels on black.

No image generation, face reconstruction, or facial retouching is used.
The narrow hand-guided trimap prevents segmentation from eating into the face.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
source = ROOT/'output/portraits/pejman-side-comb-level-glasses.png'
rgb = np.asarray(Image.open(source).convert('RGB'))
h, w = rgb.shape[:2]
outline = np.int32([
 (0,1217),(7,1145),(25,1105),(61,1062),(83,1022),(111,990),
 (153,962),(204,930),(272,894),(335,859),(395,823),(421,802),
 (446,786),(455,759),(456,710),(446,667),(425,625),
 (400,624),(380,609),(369,588),(363,558),(355,522),(355,492),
 (365,478),(378,474),(394,485),(393,466),
 (385,445),(383,410),(381,378),(378,348),(382,319),
 (391,286),(406,252),(424,227),(451,204),(482,186),
 (516,171),(548,161),(575,157),(601,152),(629,156),
 (658,164),(683,178),(701,197),(710,212),(739,219),
 (766,242),(785,275),(794,310),(799,347),(801,385),
 (799,420),(797,452),(808,451),(819,455),(824,470),
 (825,496),(832,524),(835,552),(831,578),(821,593),
 (809,600),(799,597),(793,627),(786,655),(776,680),
 (775,710),(794,738),(811,762),(822,791),(837,806),
 (882,827),(939,853),(1000,885),(1059,915),(1090,942),
 (1120,983),(1144,1035),(1155,1085),(1162,1148),(1170,1217)
])
guide = np.zeros((h,w),np.uint8)
cv2.fillPoly(guide,[outline],255)
trimap = np.full((h,w),cv2.GC_BGD,np.uint8)
outer = cv2.dilate(guide,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(21,21)))
inner = cv2.erode(guide,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19)))
trimap[outer>0] = cv2.GC_PR_BGD
trimap[guide>0] = cv2.GC_PR_FGD
trimap[inner>0] = cv2.GC_FGD
cv2.setRNGSeed(17)
cv2.grabCut(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),trimap,None,
            np.zeros((1,65)),np.zeros((1,65)),5,cv2.GC_INIT_WITH_MASK)
binary = np.uint8((trimap==cv2.GC_FGD)|(trimap==cv2.GC_PR_FGD))*255
# Keep only the subject and close isolated one-pixel holes, retaining hair detail.
count, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
largest = 1+np.argmax(stats[1:,cv2.CC_STAT_AREA])
binary = np.uint8(labels==largest)*255
binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
# Background lettering and a spectator touch the left silhouette. Explicitly
# bound that edge so their similarly colored pixels cannot join the subject.
from scipy.interpolate import PchipInterpolator
left_edge = np.float32([
 (350,380),(365,382),(390,384),(420,386),(445,389),(464,395),
 (470,380),(477,373),(490,369),(510,367),(530,368),(550,371),
 (570,376),(588,385),(601,395),(612,408),(619,425),(623,440),
 (635,449),(653,455),(675,458),(700,461),(730,461),(755,456),
 (775,450)
])
edge = PchipInterpolator(left_edge[:,0],left_edge[:,1])
for y in range(350,776):
    binary[y,:int(np.ceil(edge(y)))]=0
alpha = cv2.GaussianBlur(binary,(0,0),.85).astype(np.float32)/255
gray = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
out = ROOT/'output/portraits'
Image.fromarray(np.uint8(alpha*255)).save(out/'approved-portrait-mask.png')
rgba = np.dstack([gray,gray,gray,np.uint8(alpha*255)])
Image.fromarray(rgba,'RGBA').save(out/'approved-portrait-cutout.png')
# Uniform scaling only, with the same wide centered framing as the website.
scale = .84
matrix = np.float32([[scale,0,836-scale*610],[0,scale,44-scale*150]])
premultiplied = gray.astype(np.float32)*alpha
hero = cv2.warpAffine(premultiplied,matrix,(1672,941),flags=cv2.INTER_CUBIC)
# Fade the cropped lower torso into black, avoiding a rectangular source edge.
fade = np.clip((941-np.arange(941))/140,0,1)
fade = fade*fade*(3-2*fade)
hero *= fade[:,None]
hero = np.uint8(np.clip(hero,0,255))
im = Image.fromarray(hero).convert('RGB')
im.save(out/'pejman-masked-black-hero.png')
im.save(ROOT/'assets/images/pejman-hero-masked-black.webp','WEBP',quality=94,method=6)
# A neutral proof makes any remaining background fringe easier to inspect.
proof = gray.astype(np.float32)*alpha+90*(1-alpha)
Image.fromarray(np.uint8(proof)).save(out/'approved-mask-edge-proof.png')
assert np.array_equal(rgba[300:700,450:750,:3],np.repeat(gray[300:700,450:750,None],3,axis=2))
print('Created grayscale cutout, mask, edge proof and 1672x941 black-background hero.')
