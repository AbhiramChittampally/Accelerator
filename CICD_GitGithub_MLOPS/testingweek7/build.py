
from pathlib import Path

import zipfile
import hashlib

ROOT = Path(__file__).parent
SOURCE = ROOT / "src"
DIST = ROOT / "dist"
ARTIFACT = DIST / "week7-app-v1.0.0.zip"

DIST.mkdir(exist_ok=True)

with zipfile.ZipFile(ARTIFACT, "w") as archive:
    for file in SOURCE.glob("*.py"):
        archive.write(file, arcname=f"src/{file.name}")

file_hash = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()

print(f"Build completed: {ARTIFACT}")
print(f"SHA-256: {file_hash}")
