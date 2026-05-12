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

    if not p_pdf.is_file():
        pdf = depasswd_pdf(p, password='sWl23g')
        pdf.save(p_pdf)

    if not all([
        p_json.is_file(),
        p_txt.is_file()
    ]):
        info, text = parse_content(p_pdf)
        with open(p_pdf.with_suffix('.json'), 'w') as fp:
            json.dump(info, fp, ensure_ascii=False)
        with open(p_pdf.with_suffix('.txt'), 'w', encoding=encoding) as fp:
            squeezed = ''.join([e.strip() for e in text.split() if e.strip()])
            fp.write(squeezed)

logger.info('Done.')

# %% ---- 2026-05-12 ------------------------
# Pending

# %% ---- 2026-05-12 ------------------------
# Pending

# %%
