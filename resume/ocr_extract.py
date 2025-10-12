#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OCR extract text from screenshot/*.png into screenshots_ocr.txt"""
import os
from glob import glob
import json

import easyocr


def main():
    ROOT = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(ROOT, 'screenshot')
    paths = sorted(glob(os.path.join(img_dir, '*.png')))
    if not paths:
        print('No PNG files found in resume/screenshot/.')
        return

    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

    all_results = []
    out_lines = []
    for p in paths:
        print(f'Processing {p} ...')
        result = reader.readtext(p, detail=1, paragraph=True)
        # result is list of [bbox, text, confidence]
        texts = [r[1] for r in result if isinstance(r, (list, tuple)) and len(r) >= 2]
        combined = '\n'.join(texts)
        all_results.append({'file': os.path.basename(p), 'text': combined})
        out_lines.append(f'===== {os.path.basename(p)} =====')
        out_lines.append(combined)
        out_lines.append('')

    out_txt = os.path.join(ROOT, 'screenshots_ocr.txt')
    out_json = os.path.join(ROOT, 'screenshots_ocr.json')
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print('OCR completed. Output: screenshots_ocr.txt and screenshots_ocr.json')


if __name__ == '__main__':
    main()

