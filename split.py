#!/usr/bin/env python3
"""
split_for_stitch.py

Split an input image into 2-5 overlapping parts suitable for stitching.
- Chooses number of parts based on the longer image dimension.
- Splits along the longer axis (left→right for wide images, top→bottom for tall images).
- Adds configurable overlap fraction (default 20% of part size).
- Saves parts as <out_dir>/part_00.jpg, part_01.jpg, ...

Usage:
    python3 split_for_stitch.py --input /path/to/image.jpg --outdir /path/to/out --overlap 0.2

Requirements:
    pip install opencv-python numpy
"""
import os
import cv2
import math
import argparse
import numpy as np

def choose_num_parts(long_dim):
    """
    Heuristic mapping from longest image dimension (px) to number of parts (2-5).
    Modify thresholds if you want different behavior.
    """
    if long_dim >= 5000:
        return 5
    if long_dim >= 3500:
        return 4
    if long_dim >= 2200:
        return 3
    if long_dim >= 1000:
        return 2
    # For very small images, still return 2 to keep at least overlap-based stitching possible
    return 2

def split_image_with_overlap(img, num_parts, overlap_frac=0.2, axis=1):
    """
    Split image into num_parts along axis, returning list of (y0,y1,x0,x1) crop boxes.
    axis=1 -> split along width (vertical cuts: left->right).
    axis=0 -> split along height (horizontal cuts: top->bottom).
    overlap_frac is fraction of part size to overlap (0..0.5).
    """
    h, w = img.shape[:2]
    if axis == 1:
        total = w
    else:
        total = h

    # size of each nominal part without overlap
    part_nominal = total / num_parts
    # actual step between starts of consecutive parts (smaller than nominal due to overlap)
    step = int(round(part_nominal * (1 - overlap_frac)))
    if step < 1:
        step = 1

    boxes = []
    start = 0
    for i in range(num_parts):
        end = start + int(round(part_nominal))
        # ensure last part reaches the end
        if i == num_parts - 1:
            if axis == 1:
                end = total
            else:
                end = total
        # clamp
        start_clamped = max(0, min(total - 1, start))
        end_clamped = max(1, min(total, end))
        if axis == 1:
            boxes.append((0, h, start_clamped, end_clamped))  # y0,y1,x0,x1
        else:
            boxes.append((start_clamped, end_clamped, 0, w))
        start += step

        # avoid infinite loop if step small
        if start >= total:
            break

    # if we produced fewer boxes (due to clamping), merge / ensure exactly num_parts by adjusting
    if len(boxes) < num_parts:
        # rebuild by evenly spacing starts
        boxes = []
        for i in range(num_parts):
            s = int(round(i * (total / num_parts)))
            e = int(round((i+1) * (total / num_parts)))
            if axis == 1:
                boxes.append((0, h, s, e))
            else:
                boxes.append((s, e, 0, w))

    # final ensure boxes are within bounds and non-empty
    final_boxes = []
    for (y0,y1,x0,x1) in boxes:
        y0 = int(max(0, min(h-1, y0)))
        y1 = int(max(y0+1, min(h, y1)))
        x0 = int(max(0, min(w-1, x0)))
        x1 = int(max(x0+1, min(w, x1)))
        final_boxes.append((y0,y1,x0,x1))
    return final_boxes

def save_parts(img_path, out_dir, overlap_frac=0.2):
    os.makedirs(out_dir, exist_ok=True)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {img_path}")
    h, w = img.shape[:2]
    longer = max(h, w)
    # decide axis: split along width if image is wider, else split along height
    axis = 1 if w >= h else 0
    num_parts = choose_num_parts(longer)
    # ensure between 2 and 5
    num_parts = max(2, min(5, num_parts))

    boxes = split_image_with_overlap(img, num_parts, overlap_frac=overlap_frac, axis=axis)
    saved_paths = []
    for idx, (y0,y1,x0,x1) in enumerate(boxes):
        part = img[y0:y1, x0:x1].copy()
        fname = os.path.join(out_dir, f"part_{idx:02d}.jpg")
        cv2.imwrite(fname, part)
        saved_paths.append(fname)
        print(f"[SAVED] part {idx}: coords y({y0},{y1}) x({x0},{x1}) -> {fname}")
    return saved_paths

def parse_args():
    parser = argparse.ArgumentParser(description="Split image into overlapping parts for stitching.")
    parser.add_argument("--input", "-i", required=True, help="Input image path")
    parser.add_argument("--outdir", "-o", default="splits", help="Output directory for parts")
    parser.add_argument("--overlap", type=float, default=0.20, help="Overlap fraction (0.0 - 0.5), default 0.2")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if not (0.0 <= args.overlap <= 0.5):
        raise SystemExit("Overlap must be between 0.0 and 0.5")
    parts = save_parts(args.input, args.outdir, overlap_frac=args.overlap)
    print("\n[DONE] Generated parts:")
    for p in parts:
        print("  ", p)
    print("\nNow you can run your stitcher on these parts (in left-to-right or top-to-bottom order).")
