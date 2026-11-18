
from pathlib import Path
import shutil
import hashlib

ROOT = Path(__file__).parent
ARTIFACT = ROOT / "dist" / "week7-app-v1.0.0.zip"

ENVIRONMENTS = ["development", "staging", "production"]

original_hash = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()

for environment in ENVIRONMENTS:
    destination = ROOT / "deployments" / environment
    destination.mkdir(parents=True, exist_ok=True)

    deployed_artifact = destination / ARTIFACT.name
    shutil.copy2(ARTIFACT, deployed_artifact)

    deployed_hash = hashlib.sha256(
        deployed_artifact.read_bytes()
    ).hexdigest()

    print(f"{environment}: {deployed_hash}")
    assert deployed_hash == original_hash

print("All environments use the exact same artifact.")
