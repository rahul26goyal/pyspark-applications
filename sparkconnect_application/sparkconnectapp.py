import logging

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


class MySparkConnectApplication:

    @staticmethod
    def create_spark_session(endpoint_url: str) -> SparkSession:
        logger.info(f"Creating Spark Connect application..: ${endpoint_url}")
        spark = (SparkSession.builder
                 .remote(endpoint_url)
                 .getOrCreate())
        logger.info("Spark Connect session created..")
        return spark


