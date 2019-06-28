import os


class BaseConfig:
    """Base Configuration"""

    TESTING = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""

    SQL_ALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Testing Configuration"""

    TESTING = True
    SQL_ALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Production Configuration"""

    SQL_ALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

