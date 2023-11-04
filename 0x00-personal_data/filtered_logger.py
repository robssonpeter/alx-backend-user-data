#!/usr/bin/env python3
""" The module containing the function filtered logger """
import re
import logging
from typing import List


def filter_datum(fields, redaction, message, separator):
    """ The function for filtering the data from logs """
    for field in fields:
        pattern = f'{field}=[\w\d\s\/\@.-]*{separator}'
        if isinstance(message, str):
            message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
        logging.basicConfig(format=self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        #print(record.msg)
        return filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
