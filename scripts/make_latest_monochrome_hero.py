"""Convert the latest approved portrait to grayscale for the existing hero."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
source = ROOT/'output/portraits/original-photo-black-background-ai.png'
portrait = ImageOps.grayscale(Image.open(source))
# Trim only unused black space above the head; scale the whole photo uniformly.
portrait = portrait.crop((0,85,portrait.width,portrait.height))
scale = 941/portrait.height
portrait = portrait.resize((round(portrait.width*scale),941),Image.LANCZOS)
hero = Image.new('L',(1672,941),0)
hero.paste(portrait,(round(836-600*scale),0))
hero = hero.convert('RGB')
hero.save(ROOT/'output/portraits/latest-portrait-monochrome-hero.png')
hero.save(ROOT/'assets/images/pejman-hero-original-monochrome.webp',quality=94,method=6)
print('Saved latest portrait in grayscale with wide black framing; no generative edits.')
