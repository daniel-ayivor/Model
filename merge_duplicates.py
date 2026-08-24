r"""
merge_duplicates.py

Merges confirmed duplicate class folders (same disease, different naming
convention) into single canonical folders. Does NOT touch your original
dataset — copies everything into a new "train_cleaned" folder next to it,
so you can verify the result before deleting the old one.

Usage:
    python merge_duplicates.py "C:\path\to\plant_datasets\processed\train"

Output:
    Creates a sibling folder: "train_cleaned" containing the merged classes,
    plus any folders NOT listed in MERGE_MAP copied over unchanged (so you
    don't lose the bare-crop folders or the low-count/ambiguous ones --
    they're just passed through as-is for you to handle separately).
"""

import sys
import os
import shutil

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# canonical_name -> [list of source folder names to merge into it]
#
# NOTE: This is the SECOND merge pass. Danny already manually merged the
# apple/potato/tomato "copy" duplicates and the bare crop-name dump folders
# in the first pass. This map only covers the 8 duplicate groups the audit
# script's normalizer couldn't catch (word substitutions like
# "Corn_(maize)" -> "maize" and "Pepper__bell" -> "pepper", which aren't
# punctuation-only differences).
MERGE_MAP = {
    "maize_cercospora_leaf_spot": [
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "maize_cercospora_leaf_spot_gray_leaf_spot",
    ],
    "maize_common_rust": ["Corn_(maize)___Common_rust_", "maize_common_rust"],
    "maize_northern_leaf_blight": [
        "Corn_(maize)___Northern_Leaf_Blight",
        "maize_northern_leaf_blight",
    ],
    "maize_healthy": ["Corn_(maize)___healthy", "maize_healthy"],
    "pepper_bacterial_spot": ["Pepper__bell___Bacterial_spot", "pepper_bacterial_spot"],
    "pepper_healthy": ["Pepper__bell___healthy", "pepper_healthy"],
    "tomato_mosaic_virus": [
        "tomato_tomato_mosaic_virus",
        "tomato_mosaic_virus",
    ],
    "tomato_yellow_leaf_curl_virus": [
        "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "tomato_tomato_yellow_leaf_curl_virus",
        "tomato_yellow_leaf_curl_virus",
    ],
    # tomato_leaf_curl is NOT merged here -- Danny to confirm whether it's
    # the same condition as tomato_yellow_leaf_curl_virus before merging.
}

# Build reverse lookup: source folder name -> canonical name
SOURCE_TO_CANONICAL = {}
for canonical, sources in MERGE_MAP.items():
    for s in sources:
        SOURCE_TO_CANONICAL[s] = canonical


def copy_images(src_folder: str, dst_folder: str, prefix: str):
    """Copy all images from src_folder into dst_folder, prefixing filenames
    to avoid collisions between merged source folders."""
    os.makedirs(dst_folder, exist_ok=True)
    copied = 0
    for fname in os.listdir(src_folder):
        ext = os.path.splitext(fname)[1].lower()
        if ext not in IMAGE_EXTS:
            continue
        src_path = os.path.join(src_folder, fname)
        # Prefix with a short tag derived from the source folder to guarantee
        # uniqueness across merged sources, while keeping the original name
        # for traceability.
        dst_name = f"{prefix}__{fname}"
        dst_path = os.path.join(dst_folder, dst_name)
        # Handle any remaining collision defensively
        counter = 1
        while os.path.exists(dst_path):
            root, e = os.path.splitext(dst_name)
            dst_path = os.path.join(dst_folder, f"{root}_{counter}{e}")
            counter += 1
        shutil.copy2(src_path, dst_path)
        copied += 1
    return copied


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_duplicates.py <path_to_train_folder>")
        sys.exit(1)

    src_root = sys.argv[1]
    if not os.path.isdir(src_root):
        print(f"ERROR: '{src_root}' is not a directory.")
        sys.exit(1)

    parent = os.path.dirname(os.path.normpath(src_root))
    base_name = os.path.basename(os.path.normpath(src_root))
    dst_root = os.path.join(parent, f"{base_name}_cleaned")

    if os.path.exists(dst_root):
        print(f"ERROR: Output folder already exists: {dst_root}")
        print("Delete it or rename it before re-running, to avoid mixing old/new results.")
        sys.exit(1)

    os.makedirs(dst_root)

    all_folders = sorted(
        d for d in os.listdir(src_root) if os.path.isdir(os.path.join(src_root, d))
    )

    print(f"Source: {src_root}")
    print(f"Output: {dst_root}\n")

    handled_sources = set()
    total_copied = 0

    # --- Step 1: process merges ---
    print("=" * 70)
    print("MERGING DUPLICATE CLASSES")
    print("=" * 70)
    for canonical, sources in MERGE_MAP.items():
        existing_sources = [s for s in sources if s in all_folders]
        if not existing_sources:
            print(f"  SKIP '{canonical}': none of {sources} found in source folder")
            continue

        dst_folder = os.path.join(dst_root, canonical)
        merged_count = 0
        for i, source in enumerate(existing_sources):
            src_folder = os.path.join(src_root, source)
            prefix = f"src{i}"
            n = copy_images(src_folder, dst_folder, prefix)
            merged_count += n
            handled_sources.add(source)
        print(f"  {canonical:<35} <- {existing_sources}  ({merged_count} images)")
        total_copied += merged_count

    # --- Step 2: pass through everything else unchanged ---
    print()
    print("=" * 70)
    print("COPYING UNCHANGED FOLDERS (not in merge map -- review these yourself)")
    print("=" * 70)
    for folder in all_folders:
        if folder in handled_sources:
            continue
        src_folder = os.path.join(src_root, folder)
        dst_folder = os.path.join(dst_root, folder)
        n = copy_images(src_folder, dst_folder, "orig")
        total_copied += n
        print(f"  {folder:<55} ({n} images) <-- passed through as-is")

    print()
    print("=" * 70)
    print(f"DONE. Total images copied: {total_copied}")
    print(f"Cleaned dataset written to: {dst_root}")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Spot-check a few merged folders in train_cleaned to confirm images look right.")
    print("  2. Decide what to do with the bare crop-name folders (Cashew, Cassava,")
    print("     Maize, Rice, Tomato) that were passed through unchanged.")
    print("  3. Decide on tomato_leaf_curl, mossaic_virus, yellow_mosaic, southern_blight,")
    print("     and sudden_death_syndrone (also passed through unchanged).")
    print("  4. Add a 'not_a_plant' folder with non-plant images.")
    print("  5. Once happy, point your training script at train_cleaned instead of train.")


if __name__ == "__main__":
    main()