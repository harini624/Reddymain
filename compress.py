import os
from PIL import Image

for root, _, files in os.walk("media"):
    for f in files:
        p = os.path.join(root, f)
        if f.lower().endswith((".jpg", ".jpeg")) and os.path.getsize(p) > 500_000:
            img = Image.open(p)
            img.thumbnail((1200, 1200))
            img.convert("RGB").save(p, quality=75, optimize=True)
            print("done", p, round(os.path.getsize(p) / 1024), "KB")