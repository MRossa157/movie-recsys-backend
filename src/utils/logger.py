import logging
from sys import stderr, stdout
from typing import TextIO

_INFO_FORMAT: str = (
    '%(asctime)s.%(msecs)3d %(levelname)s in %(name)s: %(message)s'
)
_ERROR_FORMAT: str = (
    '%(asctime)s.%(msecs)3d %(levelname)s in %(name)s '
    '(%(pathname)s, line %(lineno)d, %(funcName)s): %(message)s'
)


def get_info_logger(name: str) -> logging.Logger:
    """
    Функция для получения объекта логирования, предназначенного для вывода
    сообщений уровня INFO.

    Args:
        name: имя объекта логирования

    Returns:
        Объект класса Logger из logging
    """
    return _get_logger(name, _INFO_FORMAT, stdout)


def get_error_logger(name: str) -> logging.Logger:
    """
    Функция для получения объекта логирования, предназначенного для вывода
    сообщений уровней WARNING, ERROR и CRITICAL.

    Args:
        name: имя объекта логирования

    Returns:
        Объект класса Logger из logging
    """
    return _get_logger(name, _ERROR_FORMAT, stderr)


def _get_logger(
        name: str,
        log_format: str,
        stream: TextIO,
) -> logging.Logger:
    """
    Функция для получения объекта логирования, настроенного под нужды проекта.

    Args:
        name: имя объекта логирования
        log_format: формат лога
        stream: поток вывода

    Returns:
        Объект класса Logger из logging
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(stream)
    handler.setFormatter(
        logging.Formatter(log_format, '%Y-%m-%d %H:%M:%S'),
    )
    logger.addHandler(handler)

    return logger
