"""
File: read-files.py
Author: Chuncheng Zhang
Date: 2026-05-12
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Read pdf files.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2026-05-12 ------------------------
# Requirements and constants
import json
from rich import print
from pathlib import Path
from tqdm.auto import tqdm
from PyPDF2 import PdfReader

from util.depasswd import depasswd_pdf
from util.logging import logger

# %%
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

encoding = 'utf-8'

# %% ---- 2026-05-12 ------------------------
# Function and class


def parse_content(path: Path):
    reader = PdfReader(path)

    # --------------------
    num_pages = len(reader.pages)
    txt = reader.pages[0].extract_text().replace(
        'Applicant name', '申 请 人：').replace('Project title', '项目名称：')
    split = txt.split('\n')
    print(split)

    # --------------------
    full_text = b'\n'.join([
        reader.pages[i].extract_text().encode(encoding, errors='ignore')
        for i in range(num_pages)])

    title = [
        e for e in split
        if e.startswith('项目名称：')][0][5:].strip()
    title = title.replace('/', ' ')

    name = [
        e for e in split
        if e.startswith('申 请 人：')][0][7:].split()[0].strip()

    info = {
        'title': title,
        'name': name,
        'fname': path.name,
        'head': '\n'.join(split)
    }

    text = full_text.decode(encoding)

    return info, text


# %% ---- 2026-05-12 ------------------------
# Play ground
pdf_files = sorted(Path('20260512').glob('*.pdf'))

for p in tqdm(pdf_files):
    p_pdf = OUTPUT_DIR / p.name
    p_json = p_pdf.with_suffix('.json')
    p_txt = p_pdf.with_suffix('.txt')
    d_further = OUTPUT_DIR / p.stem

    if not p_pdf.is_file():
        pdf = depasswd_pdf(p, password='sWl23g')
        pdf.save(p_pdf)

    if not all([
        p_json.is_file(),
        p_txt.is_file()
    ]):
        info, text = parse_content(p_pdf)
        squeezed = ''.join([e.strip() for e in text.split() if e.strip()])
        with open(p_json, 'w', encoding=encoding) as fp:
            json.dump(info, fp, ensure_ascii=False)
        with open(p_txt, 'w', encoding=encoding) as fp:
            fp.write(squeezed)

    squeezed = open(p_txt, 'r', encoding=encoding).read()
    print('--')
    abstract = squeezed.split('中文摘要', 1)[1].split('英文摘要')[0]
    cv = squeezed.split(
        '4.申请人和主要参与者同年以不同专业技术职务（职称）申请或参与申请科学基金项目的情况（应详细说明原因）。', 1)[1].split('附件信息')[0]
    info = {'abstract': abstract, 'cv': cv}
    d_further.mkdir(parents=True, exist_ok=True)
    with open(d_further / 'abstract.txt', 'w', encoding=encoding) as fp:
        fp.write(info['abstract'])
    with open(d_further / 'cv.txt', 'w', encoding=encoding) as fp:
        fp.write(info['cv'])
    print(info)


logger.info('Done.')

# %% ---- 2026-05-12 ------------------------
# Pending

# %% ---- 2026-05-12 ------------------------
# Pending

# %%
