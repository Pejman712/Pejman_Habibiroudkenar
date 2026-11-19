"""Mask the original photograph onto a dark hero background without generation."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parent.parent
original=ImageOps.exif_transpose(Image.open(ROOT/'pics/misc/20260626_171510.jpg')).convert('RGB')
rgb=np.asarray(original)
small=np.asarray(original.resize((800,693),Image.LANCZOS))
# Hand-guided silhouette in the 800px preview coordinate system.
points=np.int32([(348,150),(351,131),(352,117),(358,104),(369,97),
 (382,94),(393,94),(407,98),(419,105),(425,117),(428,135),
 (427,151),(430,157),(429,171),(424,181),(420,190),(419,207),
 (435,217),(454,228),(467,240),(477,258),(482,280),(484,305),
 (483,329),(480,351),(473,370),(472,389),(477,420),(476,454),
 (480,488),(477,520),(477,560),(474,610),(474,650),(475,692),
 (424,692),(416,642),(410,605),(397,584),(387,611),(380,649),
 (376,692),(321,692),(324,647),(330,606),(329,561),(316,529),
 (310,496),(307,466),(303,440),(299,417),(288,410),(279,398),
 (273,378),(269,354),(268,329),(270,303),(273,282),(281,262),
 (292,246),(311,234),(334,224),(352,213),(359,206),(359,191),
 (355,180),(350,171)])
silhouette=np.zeros((693,800),np.uint8)
cv2.fillPoly(silhouette,[points],255)
mask=np.full((693,800),cv2.GC_BGD,np.uint8)
mask[cv2.dilate(silhouette,np.ones((11,11),np.uint8))>0]=cv2.GC_PR_BGD
mask[silhouette>0]=cv2.GC_PR_FGD
mask[cv2.erode(silhouette,np.ones((15,15),np.uint8))>0]=cv2.GC_FGD
cv2.setRNGSeed(7)
cv2.grabCut(cv2.cvtColor(small,cv2.COLOR_RGB2BGR),mask,None,
 np.zeros((1,65)),np.zeros((1,65)),6,cv2.GC_INIT_WITH_MASK)
alpha=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
alpha=cv2.resize(alpha,original.size,interpolation=cv2.INTER_CUBIC)
# The purple stage lighting has a similar brightness to dark hair. Preserve
# that outline with a manual head mask instead of letting GrabCut trim it.
head=np.float32([(377,94.5),(388,93),(400,94.5),(410,99),(418.5,103.5),
 (424.5,112.5),(427.5,124.5),(427,137.5),(426,147),(429.5,153.5),
 (431,163),(428,173.5),(423.5,179.5),(418,191.5),(418,215),
 (356,215),(360,207),(362,198),(362,190),(358.5,184.5),(355.5,179.5),(349.5,172),
 (347,162.5),(346.5,154),(350,149),(354.5,146),(354,135),
 (354.5,122),(360,109),(366,101)])
head_mask=np.zeros(alpha.shape,np.uint8)
head_native=np.round(head*np.float32([original.width/800,original.height/693])).astype(np.int32)
cv2.fillPoly(head_mask,[head_native],255)
join=int(205*original.height/693)
alpha[:join]=head_mask[:join]
alpha=cv2.GaussianBlur(alpha,(0,0),1.1).astype(np.float32)/255
# Frame the original upper body like the earlier wide portrait. Transform only
# the complete subject uniformly; no changes to facial features or expression.
scale=1.16
matrix=np.float32([[scale,0,836-scale*1320],[0,scale,42-scale*320]])
size=(1672,941)
warped_alpha=np.clip(cv2.warpAffine(alpha,matrix,size,flags=cv2.INTER_CUBIC),0,1)
gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
foreground=cv2.warpAffine(gray.astype(np.float32)*alpha,matrix,size,flags=cv2.INTER_CUBIC)
yy,xx=np.mgrid[:size[1],:size[0]]
# Restrained, smooth charcoal backdrop; no invented photographic detail.
light=np.exp(-(((xx-836)/690)**2+((yy-380)/680)**2))
backdrop=9+12*light
output=np.uint8(np.clip(foreground+backdrop*(1-warped_alpha),0,255))
image=Image.fromarray(output).convert('RGB')
image.save(ROOT/'assets/images/pejman-original-dark.png')
out=ROOT/'output/portraits';out.mkdir(parents=True,exist_ok=True)
Image.fromarray(np.uint8(warped_alpha*255)).save(out/'original-hero-mask.png')
print('Saved original-photo hero with masked background and monochrome styling. No face retouching or image generation.')
