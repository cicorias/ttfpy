from typing import List

import inflection
import numpy as np
import pandas as pd
from dateutil import parser as date_parser

from metadata_embedding_explorer.models import Metadata


def _normalize_slashes(fpath):
    fpath = fpath[1:].replace('/', '__').replace('.thumb', '')
    return fpath


def _parse_date(date):
    try:
        return date_parser.parse(str(date))
    except (TypeError, ValueError):
        return date_parser.parse('01.01.2017')


def _clean_data(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    df = df.replace('N.A.', np.nan)
    df.columns = [inflection.underscore(column) for column in df.columns]
    # TODO: using a random date to make sqlite happy. Once xl data cleaned, remove this.
    df['date_of_birth'] = df['date_of_birth'].fillna('01.01.2017')
    df['date_of_birth'] = df['date_of_birth'].apply(_parse_date)
    df['image_path'] = df['image_path'].apply(_normalize_slashes)
    return df


def compute_metadata(file_name: str, sheet_name: str) -> List[Metadata]:
    xl = pd.ExcelFile(file_name)
    df = xl.parse(sheet_name)
    df = _clean_data(df)
    return [Metadata(**row.to_dict()) for _, row in df.iterrows()]
