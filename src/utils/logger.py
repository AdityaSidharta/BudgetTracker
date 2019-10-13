from loguru import logger


def log_dictionary(input_dict):
    logger.info("=" * 10)
    for key, value in input_dict.items():
        logger.info("{} : {}".format(key, value))
    logger.info("=" * 10)
