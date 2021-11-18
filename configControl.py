#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для управления конфигурационным файлом
"""

import os
import configparser

import sys
# import config
from pathlib import Path

# file = Path(__file__).resolve()
# sys.path.append(str(file.parents[1]))

import settings
# from settings import *


__version__ = "1.0.0"


class Config:
    """ Управление конфигурацией программы """
    check_file_config: bool  # Наличие файла конфига

    def __new__(cls, *args, **kwargs):  # Создание singleton класса
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.path_config = os.path.join(Path.home(), settings.PATH)  # Путь до места хранения конфигураций
        self.file_config = os.path.join(self.path_config, settings.FILE)  # Путь до файла конфигурации

        self.config = configparser.ConfigParser()
        self.config.read(self.file_config)

        self.check_file_config = True if os.path.exists(self.file_config) else False

    def check_config(self):
        """ Проверка и создание необходимых папок и файлов для работы файла конфигурации """

        if not os.path.isdir(self.path_config):
            os.mkdir(self.path_config)

        if not os.path.isfile(self.file_config):
            with open(self.file_config, "w") as config_file:
                config_file.write("")

    def check_parameters(self):
        """ Проверка на наличие всех параметров и создание их при отсутствии"""

        for section, value in settings.MAIN.items():
            if not self.config.has_section(section):
                self.config.add_section(section)

            for item, key in value.items():
                if not self.config.has_option(section, item):
                    self.config.set(section, item, str(key))

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)

        self.config.read(self.file_config)

    def update(self, selection, option, value):
        """ Обновление файла конфигурации """
        self.config.set(selection, option, str(value))

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)

    def get(self, selection, option, array=False):
        """ Получение параметра конфигурации """
        if self.check_file_config:
            try:
                if array:
                    return [x for x in self.config.get(selection, option).split(";")]
                else:
                    return self.config.get(selection, option)
            except configparser.NoOptionError:
                print(f"configparser.NoOptionError: Нет такого параметра в файле конфигов: {selection} - {option}")
                return False
            except configparser.NoSectionError:
                print(f"configparser.NoOptionError: Нет такой секции в файле конфигов: {selection}")
                return False
        else:
            return False
