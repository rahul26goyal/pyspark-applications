import logging
from time import sleep

from sparkconnect_application.sparkconnectapp import MySparkConnectApplication

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Launching main application...")
    endpoint="sc://localhost:15002"
    spark = MySparkConnectApplication.create_spark_session(endpoint)
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    sleep(10)
    logger.info("Showing DataFrame content:")
    df.show()
    spark.stop()
    logger.info("Spark session stopped.")

if __name__ == "__main__":
    import sys
    python_path = sys.path
    logger.info(f"Syatem python path: {python_path}")
    logger.info("Starting...")
    main()