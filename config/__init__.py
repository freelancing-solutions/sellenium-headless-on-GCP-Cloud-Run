import os


class Config:
    INVESTAGRAM_HOME_URI = os.environ.get('INVESTAGRAM_HOME_URI')
    DEFAULT_USERNAME = os.environ.get('DEFAULT_USERNAME')
    DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')
