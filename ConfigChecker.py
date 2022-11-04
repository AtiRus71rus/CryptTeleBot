#!/usr/bin/env python
# coding: utf-8

# In[3]:


import copy
import os
import shutil
import json


# In[6]:


class ConfigurationManager:
    def __init__(self):
        self.configuration_elements = {}

    def add_element(self, key, element, has_dict=False):
        self.configuration_elements[key] = ConfigurationElement(element, has_dict)

    def get_edited_config(self, key, dict_only):
        config_element = self.configuration_elements[key]
        if dict_only and config_element.has_dict:
            return config_element.edited_config.config
        return self.configuration_elements[key].edited_config

    def set_edited_config(self, key, config):
        self.configuration_elements[key].edited_config = config

    def get_startup_config(self, key, dict_only):
        config_element = self.configuration_elements[key]
        if dict_only and config_element.has_dict:
            return config_element.startup_config.config
        return self.configuration_elements[key].startup_config


class ConfigurationElement:
    def __init__(self, element, has_dict):
        self.config = element
        self.has_dict = has_dict
        self.startup_config = copy.deepcopy(element)
        self.edited_config = copy.deepcopy(element)


def config_health_check(config: configuration.Configuration, in_backtesting: bool) -> configuration.Configuration:
    logger = logging.get_logger(LOGGER_NAME)
    # 1 ensure api key encryption
    should_replace_config = False
    if common_constants.CONFIG_EXCHANGES in config.config:
        for exchange, exchange_config in config.config[common_constants.CONFIG_EXCHANGES].items():
            for key in common_constants.CONFIG_EXCHANGE_ENCRYPTED_VALUES:
                try:
                    if not configuration.handle_encrypted_value(key, exchange_config, verbose=True):
                        should_replace_config = True
                except Exception as e:
                    logger.exception(e, True,
                                     f"Ошибка сущности: {e}")

    # 2 ensure single trader activated
    try:
        trader_enabled = trading_api.is_trader_enabled_in_config(config.config)
        if trader_enabled:
            simulator_enabled = trading_api.is_trader_simulator_enabled_in_config(config.config)
            if simulator_enabled:
                logger.error(f"Активация невозможна.")
                config.config[common_constants.CONFIG_SIMULATOR][common_constants.CONFIG_ENABLED_OPTION] = False
                should_replace_config = True
    except KeyError as e:
        logger.exception(e, True,
                         f"Ошибка введения ключа: {e}.")
        config.config[common_constants.CONFIG_SIMULATOR][common_constants.CONFIG_ENABLED_OPTION] = True
        config.config[common_constants.CONFIG_TRADER][common_constants.CONFIG_ENABLED_OPTION] = False
        should_replace_config = True

    # 3 inform about configuration issues
    if not (in_backtesting or
            trading_api.is_trader_enabled_in_config(config.config) or
            trading_api.is_trader_simulator_enabled_in_config(config.config)):
        logger.error(f"Произошло отключение от сервера.")

    # 4 save fixed config if necessary
    if should_replace_config:
        try:
            config.save()
            return config
        except Exception as e:
            logger.error(f"Сохранение вида health-check было отключено: {e}, "
                         f"Введите фай конфигурации заново")
            config.read(should_raise=False, fill_missing_fields=True)
            return config


# In[ ]:




