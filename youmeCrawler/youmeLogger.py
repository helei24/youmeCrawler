# -*- coding: utf-8 -*-

import logging  
import logging.config 

#log config part
CONF_LOG = "logging.conf"
logging.config.fileConfig(CONF_LOG)

logger = logging.getLogger('youme_pipeline')
logger.setLevel(logging.INFO)  