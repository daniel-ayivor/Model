r"""
audit_dataset.py

Scans a training image dataset laid out as:

    dataset_root/
        ClassName1/
            img1.jpg
            img2.jpg
        ClassName2/
            ...

...and reports:
  - every class folder + image count
  - likely DUPLICATE classes (same disease, different naming style)
  - BARE CROP folders (crop name with no disease, e.g. "Rice", "Maize")
  - folders with artifact suffixes (" copy", "(1)", etc.)

Usage:
   python audit_dataset.py "C:\Users\Daniel Kofi Ayivor\Documents\Mine\WarmiGro\backend\Model\plant_datasets\processed\train"
"""

import sys
import os
import re
from collections import defaultdict

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Known bare-crop names (no disease attached) that indicate an
# unsorted / leftover top-level folder rather than a real class.
BARE_CROP_NAMES = {
    "cashew", "cassava", "maize", "corn", "rice", "tomato", "potato",
    "pepper", "apple", "cocoa", "plantain", "yam", "onion", "bean",
    "groundnut", "sweet_potato", "sweetpotato"
}

ARTIFACT_PATTERNS = [
    re.compile(r"\bcopy\b", re.IGNORECASE),
    re.compile(r"\(\d+\)$"),          # "(1)", "(2)"
    re.compile(r"[_\-]?\d+$"),        # trailing "_2", "-3" (be careful, can false-positive)
]


def normalize(name: str) -> str:
    """Normalize a class name for duplicate detection."""
    n = name.lower()
    n = n.replace("___", "_").replace("__", "_")
    n = n.replace("(", "").replace(")", "")
    n = n.replace(" ", "_")
    n = re.sub(r"\bcopy\b", "", n, flags=re.IGNORECASE)
    n = re.sub(r"_+", "_", n)
    n = n.strip("_").strip()
    return n


def count_images(folder_path: str) -> int:
    count = 0
    try:
        for f in os.listdir(folder_path):
            if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
                count += 1
    except NotADirectoryError:
        return -1
    return count


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_dataset.py <path_to_dataset_root>")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"ERROR: '{root}' is not a directory.")
        sys.exit(1)

    class_folders = sorted(
        d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))
    )

    if not class_folders:
        print("No subfolders found. Is this the right dataset root?")
        sys.exit(1)

    print(f"Found {len(class_folders)} class folders under: {root}\n")

    # ---- 1. Per-folder counts ----
    print("=" * 70)
    print("CLASS FOLDER COUNTS")
    print("=" * 70)
    counts = {}
    total_images = 0
    for folder in class_folders:
        path = os.path.join(root, folder)
        n = count_images(path)
        counts[folder] = n
        total_images += max(n, 0)
        flag = ""
        if n == 0:
            flag = "  <-- EMPTY, no images found"
        elif n < 20:
            flag = f"  <-- LOW COUNT ({n}), may be too few to train well"
        print(f"  {folder:<55} {n:>5} images{flag}")
    print(f"\nTotal images across all folders: {total_images}\n")

    # ---- 2. Duplicate detection ----
    print("=" * 70)
    print("LIKELY DUPLICATE CLASSES (same normalized name)")
    print("=" * 70)
    groups = defaultdict(list)
    for folder in class_folders:
        groups[normalize(folder)].append(folder)

    dup_found = False
    for norm_name, originals in sorted(groups.items()):
        if len(originals) > 1:
            dup_found = True
            total = sum(max(counts[o], 0) for o in originals)
            print(f"  '{norm_name}' <- {originals}  (combined {total} images)")
    if not dup_found:
        print("  None found.")
    print()

    # ---- 3. Bare crop-name folders ----
    print("=" * 70)
    print("BARE CROP-NAME FOLDERS (no disease attached — likely unsorted data)")
    print("=" * 70)
    bare_found = False
    for folder in class_folders:
        norm = normalize(folder)
        if norm in BARE_CROP_NAMES:
            bare_found = True
            print(f"  {folder}  ({counts[folder]} images) <-- review/reclassify these")
    if not bare_found:
        print("  None found.")
    print()

    # ---- 4. Artifact-suffix folders ----
    print("=" * 70)
    print("FOLDERS WITH SUSPICIOUS SUFFIXES ('copy', '(1)', trailing numbers)")
    print("=" * 70)
    artifact_found = False
    for folder in class_folders:
        for pat in ARTIFACT_PATTERNS[:2]:  # skip the trailing-number one, too noisy alone
            if pat.search(folder):
                artifact_found = True
                print(f"  {folder}  ({counts[folder]} images) <-- likely a duplicate/leftover folder")
                break
    if not artifact_found:
        print("  None found.")
    print()

    # ---- 5. Suggested merge map ----
    print("=" * 70)
    print("SUGGESTED MERGE MAP (review before applying!)")
    print("=" * 70)
    for norm_name, originals in sorted(groups.items()):
        if len(originals) > 1:
            # Prefer the "cleanest" looking name as canonical: lowercase,
            # single underscores, no "copy"/parens — falls back to first alphabetically.
            canonical = sorted(originals, key=lambda o: (len(o), o))[0]
            others = [o for o in originals if o != canonical]
            print(f"  MERGE INTO '{canonical}':  {others}")
    print()

    print("Next steps:")
    print("  1. Review the duplicate groups above — confirm they really are the same disease.")
    print("  2. Merge duplicate folders' images into one canonical folder per class.")
    print("  3. Manually review bare crop-name folders and sort images into correct")
    print("     disease/healthy subfolders (or discard if unusable).")
    print("  4. Add a 'not_a_plant' folder with non-plant images (random objects,")
    print("     indoor scenes, etc.) so the model can learn to reject non-plant input.")
    print("  5. Re-run this script on the cleaned dataset to confirm zero duplicates")
    print("     before retraining.")


if __name__ == "__main__":
    main()