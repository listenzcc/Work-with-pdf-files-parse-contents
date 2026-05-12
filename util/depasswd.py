"""
File: depasswd.py
Author: Chuncheng Zhang
Date: 2026-05-12
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    De-password the input .pdf file.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2026-05-12 ------------------------
# Requirements and constants
import pikepdf
from pathlib import Path

from .logging import logger


# %% ---- 2026-05-12 ------------------------
# Function and class
def depasswd_pdf(path, password: str = 'passwd'):
    '''
    Clear the password of the pdf file.

    Args:
        path (Path): the pdf file path.
        password (str): the password.

    Return:
        pdf (Pdf): the depasswd pdf object.
    '''

    path = Path(path)
    try:
        pdf = pikepdf.open(path)
    except pikepdf._core.PasswordError:
        pdf = pikepdf.open(path, password=password)

    logger.info(f'Read pdf file: {path}')

    return pdf

# %% ---- 2026-05-12 ------------------------
# Play ground


# %% ---- 2026-05-12 ------------------------
# Pending


# %% ---- 2026-05-12 ------------------------
# Pending
