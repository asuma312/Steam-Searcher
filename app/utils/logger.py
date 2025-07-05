import logging

logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)

# Ao invés de adicionar um StreamHandler, use um NullHandler
logger.addHandler(logging.NullHandler())