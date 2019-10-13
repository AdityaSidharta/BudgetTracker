import numpy as np
from loguru import logger

saltedge_columns = [
    "id",
    "account_id",
    "duplicated",
    "mode",
    "status",
    "made_on",
    "amount",
    "currency_code",
    "description",
    "category",
    "type",
    "account_balance_snapshot",
    "created_at",
    "updated_at",
    "extra",
]


def add_column_if_not_exists(df, columns):
    for column in columns:
        if column not in df.columns.tolist():
            logger.info("Adding column {}".format(column))
            df[column] = np.nan
    return df
