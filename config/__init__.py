import os
from decouple import config


class Config:
    INVESTAGRAM_HOME_URI = os.environ.get('INVESTAGRAM_HOME_URI') or config('INVESTAGRAM_HOME_URI')
    DEFAULT_USERNAME = os.environ.get('DEFAULT_USERNAME') or config('DEFAULT_USERNAME')
    DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD') or config('DEFAULT_PASSWORD')
