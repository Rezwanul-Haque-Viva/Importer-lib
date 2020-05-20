import mongoengine


class mongo_connection:
    """mongo db connection context manager"""
    def __init__(self, config):
        self._config = config
        self.connector = None

    def __enter__(self):
        self.connector = mongoengine.connect(
            self._config.MONGO_DB,
            host=self._config.MONGO_HOST,
            port=self._config.MONGO_PORT,
            username=self._config.MONGO_USERNAME,
            password=self._config.MONGO_PASSWORD,
            authentication_source=self._config.MONGO_AUTH_DATABASE
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        mongoengine.disconnect()
