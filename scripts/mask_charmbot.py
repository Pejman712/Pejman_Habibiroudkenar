"""Create a transparent CHARMBot cutout with a hand-guided GrabCut mask.

Uses the existing photograph only; no image generation or synthetic pixels.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'assets/images/cern/charmbot-only.jpg'
DEST = ROOT / 'assets/images/cern/charmbot-cutout.png'
photo = Image.open(SOURCE).convert('RGB')
assert photo.size == (560, 418)
outline = np.array([
    (1,81),(17,72),(43,67),(72,64),(91,67),(91,48),(96,31),
    (106,24),(119,22),(134,28),(143,36),(154,28),(170,27),
    (175,17),(188,14),(198,19),(204,32),(221,25),(235,17),
    (255,13),(263,4),(276,1),(290,4),(302,7),(314,19),(321,40),
    (338,43),(352,57),(374,55),(390,59),(406,68),(414,86),
    (434,96),(439,112),(461,111),(475,106),(498,109),(516,116),
    (530,130),(534,149),(547,164),(551,184),(545,195),(546,210),
    (538,224),(520,239),(503,251),(486,258),(470,267),(447,279),
    (422,293),(395,309),(365,327),(335,345),(308,361),(294,379),
    (276,395),(251,407),(231,413),(214,411),(198,399),(184,381),
    (171,358),(158,337),(146,314),(132,290),(115,275),(97,255),
    (82,235),(66,217),(56,200),(49,182),(33,165),(20,147),
    (9,125),(3,104)
], dtype=np.int32)
silhouette = np.zeros((418, 560), np.uint8)
cv2.fillPoly(silhouette, [outline], 255)
mask = np.full(silhouette.shape, cv2.GC_BGD, dtype=np.uint8)
expanded = cv2.dilate(silhouette, np.ones((9,9), np.uint8))
interior = cv2.erode(silhouette, np.ones((15,15), np.uint8))
mask[expanded > 0] = cv2.GC_PR_BGD
mask[silhouette > 0] = cv2.GC_PR_FGD
mask[interior > 0] = cv2.GC_FGD
cv2.setRNGSeed(12)
cv2.grabCut(cv2.cvtColor(np.asarray(photo), cv2.COLOR_RGB2BGR), mask,
            None, np.zeros((1,65)), np.zeros((1,65)), 5, cv2.GC_INIT_WITH_MASK)
alpha = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
# Floor visible through the small cable loop at the back of the chassis.
cv2.fillPoly(alpha, [np.array([(180,21),(184,19),(190,19),(195,22),
                             (196,28),(192,31),(181,30),(178,26)],
                            dtype=np.int32)], 0)
alpha_image = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.45))
cutout = photo.convert('RGBA')
cutout.putalpha(alpha_image)
cutout.save(DEST)
preview = Image.new('RGBA', photo.size, (16,19,19,255))
preview.alpha_composite(cutout)
preview_path = ROOT / 'output/previews/charmbot-mask-preview.png'
preview_path.parent.mkdir(parents=True, exist_ok=True)
preview.convert('RGB').save(preview_path)
print(f'Saved {DEST}')
