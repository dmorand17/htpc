import unittest
from unittest import TestCase, mock
import os
import json
import sys
import logging
from pathlib import Path

from htpc.lambda_function import *

# Enable this section to show logger debug output
#logger = logging.getLogger()
#logger.level = logging.DEBUG
#stream_handler = logging.StreamHandler(sys.stdout)
#logger.addHandler(stream_handler)

class FunctionTest(TestCase):
    def setUp(self):
        from dotenv import load_dotenv

        basedir = Path(__file__).resolve().parent.parent
        # basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(basedir / ".env")
        # sys.path.insert(0, "../project")
        # from project import item
        # further setup using this import
        # printing environment variables

    def test_server_down(self):
        with Path("test/sns-alarm-down-notification.json").open(
            encoding="UTF-8"
        ) as source:
            event = json.load(source)
            response = lambda_handler(event, {})

        self.assertEqual(response, {"status": "ok"})

    def test_server_down2(self):
        with Path("test/sns-alarm-down-notification.json").open(
            encoding="UTF-8"
        ) as source:
            event = json.load(source)
            response = lambda_handler(event, {})

        self.assertEqual(response, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
