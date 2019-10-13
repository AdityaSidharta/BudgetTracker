import datetime as dt
import os

import fire
import pandas as pd
from loguru import logger

from src.saltedge.functions import get_customer, get_connections, get_transactions, get_accounts
from src.utils.common import get_filename
from src.utils.config import config
from src.utils.directory import RAW_PATH
from src.utils.logger import log_dictionary


def main(year: int = None, month: int = None):
    today = dt.datetime.now()
    today_year = today.year
    today_month = today.month

    if (year is None) and (month is None):
        year = today_year
        month = today_month - 1
    else:
        raise ValueError("year and month must be specified together")
    if year > today_year:
        raise AssertionError("Could not get information for the current month / future")
    elif year == today_year:
        assert month <= today_month - 1, "Could not get information for the current month / future"
    else:
        assert month <= 12

    customer_id, customer_secret = get_customer(config.CUSTOMER_NAME)
    logger.info("Obtaining Customer ID and Customer Secret for Customer Name : {}".format(config.CUSTOMER_NAME))
    logger.info("Customer ID Obtained : {}".format(customer_id))

    connection_id, connection_info = get_connections(customer_id)
    logger.info("Connection ID Obtained : {}".format(connection_id))
    logger.info("Connection Info Obtained")
    log_dictionary(connection_info)

    accounts_id, accounts_info = get_accounts(connection_id)
    logger.info("Number of Accounts obtained : {}".format(len(accounts_id)))
    logger.info("Accounts ID Obtained : {}".format(accounts_id))
    logger.info("Accounts Info Obtained")
    for account_info in accounts_info:
        log_dictionary(account_info)

    n_accounts = len(accounts_id)
    accounts_name = [x["name"] for x in accounts_info]

    for idx in range(n_accounts):
        account_id = accounts_id[idx]
        account_name = accounts_name[idx]
        account_transaction = get_transactions(connection_id, account_id)
        logger.info("Number of Transaction loaded : {}".format(len(account_transaction)))

        year_transaction = pd.to_datetime(account_transaction["made_on"]).dt.year.values
        month_transaction = pd.to_datetime(account_transaction["made_on"]).dt.month.values

        account_transaction = (
            account_transaction[(year_transaction == year) & (month_transaction == month)].copy().reset_index()
        )

        logger.info(
            "Number of Transaction for {} in {}-{} : {}".format(account_name, year, month, len(account_transaction))
        )
        if len(account_transaction) == 0:
            logger.warning("Number of Transaction is zero. Please check whether there is any error in the input.")

        path = os.path.join(RAW_PATH, get_filename(account_name, year, month))
        account_transaction.to_csv(path, index=False)
        logger.info("Successfully saving the dataframe at {}".format(path))


if __name__ == "__main__":
    fire.Fire(main)
