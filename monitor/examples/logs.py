import logging
from loguru import logger

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    logger.info("My system is running correctly!")
    logging.debug("This code snippet's result is 10!")
    logging.info("My system is running correctly!")
    logging.warning("My system has some outdated libs which can cause security issues!")
    logging.error("A logical error has occurred!")
    logging.critical("This is a critical error, please fix it ASAP!")
