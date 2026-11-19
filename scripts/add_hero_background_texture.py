"""Reuse the earlier charcoal texture without regenerating the portrait."""
from pathlib import Path
import argparse
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--zoom',type=float,default=1.0)
parser.add_argument('--lift',type=int,default=0)
args = parser.parse_args()
if not 0.5 <= args.zoom <= 1.0:
    parser.error('--zoom must be between 0.5 and 1.0')
if not 0 <= args.lift <= 200:
    parser.error('--lift must be between 0 and 200 pixels')
portrait = np.asarray(Image.open(ROOT/'output/portraits/latest-portrait-monochrome-hero.png').convert('L'))
suffix = '-zoomed' if args.zoom != 1.0 else ''
if args.lift:
    suffix += f'-raised-{args.lift}'
if args.zoom != 1.0 or args.lift:
    h,w = portrait.shape
    smaller = Image.fromarray(portrait).resize((round(w*args.zoom),round(h*args.zoom)),Image.LANCZOS)
    canvas = Image.new('L',(w,h),0)
    canvas.paste(smaller,((w-smaller.width)//2,h-smaller.height-args.lift))
    portrait = np.asarray(canvas)
old = np.asarray(Image.open(ROOT/'assets/images/pejman-hero-restored.png').convert('L'))
# This rectangle contains only the earlier wall, clear of the old portrait.
sample = old[10:460,40:640].astype(np.float32)
detail = sample-cv2.GaussianBlur(sample,(0,0),30)
h,w = portrait.shape
texture = cv2.copyMakeBorder(detail,0,h-detail.shape[0],0,w-detail.shape[1],cv2.BORDER_REFLECT_101)
yy,xx = np.mgrid[:h,:w]
light = np.exp(-(((xx-w/2)/(w*.6))**2+((yy-h*.4)/(h*.8))**2))
backdrop = np.clip(6+14*light+texture,0,30)
# Only border-connected near-black background is eligible for replacement.
candidate = np.uint8(portrait<=12)
_,labels = cv2.connectedComponents(candidate,connectivity=8)
edge_labels = np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]))
background = np.isin(labels,edge_labels[edge_labels!=0])
distance = cv2.distanceTransform(background.astype(np.uint8),cv2.DIST_L2,5)
blend = np.clip(distance/2,0,1)
blend = blend*blend*(3-2*blend)
if args.lift:
    # Blend the bottom of the raised torso into the wall, below the face.
    fade = np.clip((yy-(h-args.lift-90))/90,0,1)
    fade = fade*fade*(3-2*fade)
    blend = np.maximum(blend,fade)
result = np.round(portrait*(1-blend)+backdrop*blend).astype(np.uint8)
preserved = (~background)&(blend==0)
assert np.array_equal(result[preserved],portrait[preserved])
im = Image.fromarray(result).convert('RGB')
im.save(ROOT/f'output/portraits/latest-portrait-textured-hero{suffix}.png')
# Lossless encoding keeps the retained portrait pixels intact.
im.save(ROOT/f'assets/images/pejman-hero-original-textured{suffix}.webp',lossless=True,method=6)
print('Saved textured portrait; foreground outside the lower fade verified unchanged.')
