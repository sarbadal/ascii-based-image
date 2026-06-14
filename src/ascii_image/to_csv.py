import pandas as pd
from pathlib import Path
from dataclasses import dataclass

from typing import Self


@dataclass(frozen=True)
class DataFrameLoader:
    file: str | Path

    def normalize_file(self: Self) -> Path:
        return Path(self.file).resolve()

    def get_no_columns(self: Self) -> int:
        with open(file=self.normalize_file(), mode='r') as f:
            first_line: str = f.readlines()[0]
        return len(first_line)

    def get_colspecs(self: Self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for i in range(self.get_no_columns()):
            tpl: tuple[int, int] = (i, i + 1) if i > 0 else (0, 1)
            result.append(tpl)
        return result

    def to_dataframe(self: Self) -> pd.DataFrame:
        colspecs: list[tuple[int, int]] = self.get_colspecs()
        return pd.read_fwf(
            self.normalize_file(), 
            colspecs=colspecs, 
            names=list(range(self.get_no_columns()))
        )

