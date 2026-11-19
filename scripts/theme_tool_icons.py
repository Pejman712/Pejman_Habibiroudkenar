"""Map SVG logo colors into the portfolio palette, retaining tonal detail."""
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import ImageColor

ROOT = Path(__file__).resolve().parent.parent
ET.register_namespace('', 'http://www.w3.org/2000/svg')
PALETTE = ['#24463d', '#498c7d', '#72d8cb', '#a5e4d5', '#e6fff7']

def theme(value):
    if value.lower()[:7] in PALETTE or value in ('none','currentColor') or value.startswith('url('):
        return value
    try:
        color = ImageColor.getrgb(value)
    except ValueError:
        return value
    r,g,b = color[:3]
    luminance = .2126*r + .7152*g + .0722*b
    index = sum(luminance >= threshold for threshold in (55,95,160,215))
    return PALETTE[index] + (f'{color[3]:02x}' if len(color)==4 else '')

if __name__ == '__main__':
    for path in (ROOT/'assets/icons/tools').glob('*.svg'):
        tree = ET.parse(path)
        for element in tree.getroot().iter():
            for key in ('fill','stroke','stop-color','color'):
                if key in element.attrib:
                    element.set(key,theme(element.get(key)))
        tree.write(path,encoding='unicode')
    print('Applied a consistent charcoal/teal palette while retaining logo shapes and tonal detail.')
