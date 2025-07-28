import logging
import os

from pyspark.sql import SparkSession
import pyspark

logger = logging.getLogger(__name__)

class MySparkApplication:

    @staticmethod
    def create_spark_Session(app_name: str  = "ClassPySparkApp") -> SparkSession:
        logger.info("Creating Spark application..")
        spark = (SparkSession.builder
                .appName(app_name)
                .getOrCreate())
        logger.info("Spark Session is created now.")
        MySparkApplication.print_spark_details(spark)
        return spark


    @staticmethod
    def print_spark_details(spark):
        spark_home = os.environ.get("SPARK_HOME", "SPARK_HOME not set")
        logger.info(f"SPARK_HOME: {spark_home}")

        #logger.info("PySpark installed at:", os.path.dirname(pyspark.__file__))
        logger.info("Spark configs..")
        logger.info(spark.sparkContext.getConf().getAll())


