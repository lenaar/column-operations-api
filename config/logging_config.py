import logging
from .environment import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)