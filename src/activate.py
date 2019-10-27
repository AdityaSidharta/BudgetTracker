from loguru import logger

from src.utils.functions import get_customer, connect_session
from src.utils.config import config


def main():
    customer_id, customer_secret = get_customer(config.CUSTOMER_NAME)
    logger.info("Obtaining Customer ID and Customer Secret for Customer Name : {}".format(config.CUSTOMER_NAME))
    logger.info("Customer ID Obtained : {}".format(customer_id))

    connect_session(customer_id)
    logger.info("Opening New Tab for Authentication. Please complete the authentication process.")


if __name__ == "__main__":
    main()
