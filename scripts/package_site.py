"""Create a GitHub Pages artifact containing only the public website files."""
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "site-release"
DEST.mkdir(exist_ok=True)
for name in ("index.html", ".nojekyll"):
    shutil.copy2(ROOT / name, DEST / name)
shutil.copytree(ROOT / "assets", DEST / "assets", dirs_exist_ok=True)
archive = ROOT / "pejman-website.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(DEST.rglob("*")):
        if path.is_file():
            bundle.write(path, path.relative_to(DEST))
print(f"Public site: {DEST}")
print(f"ZIP archive: {archive}")
