import os

import fire
import pandas as pd

from src.utils.directory import RAW_PATH


def main(year: int = None, month: int = None):
    list_df = []
    for filename in os.listdir(RAW_PATH):
        if filename.endswith("_{}_{}.csv".format(year, month)):
            list_df.append(pd.read_csv(os.path.join(RAW_PATH, filename)))
    full_df = pd.concat(list_df, axis=0, ignore_index=True)
    expense_df = full_df[full_df["amount"] < 0.0].copy()
    income_df = full_df[full_df["amount"] > 0].copy()


if __name__ == "__main__":
    fire.Fire(main)
