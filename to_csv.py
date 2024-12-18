import pandas as pd
from dataclasses import dataclass

from typing import Self


@dataclass(frozen=True)
class DataLoader:
    file: str

    def get_no_columns(self: Self) -> int:
        with open(file=self.file, mode='r') as f:
            first_line: str = f.readlines()[0]
        return len(first_line)

    def get_colspecs(self: Self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for i in range(self.get_no_columns()):
            tpl: tuple[int, int] = (i, i + 1) if i > 0 else (0, 1)
            result.append(tpl)
        return result

    def load_data(self: Self) -> pd.DataFrame:
        colspecs: list[tuple[int, int]] = self.get_colspecs()
        return pd.read_fwf(
            self.file, 
            colspecs=colspecs, 
            names=list(range(self.get_no_columns()))
        )


def main() -> None:
    file = "with_ascii/images/exports/saturn-00.txt"
    data_loader = DataLoader(file=file)
    df: pd.DataFrame = data_loader.load_data()
    print(df.head(n=10))


if __name__ == "__main__":
    main()
