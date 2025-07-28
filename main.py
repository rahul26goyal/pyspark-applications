
import  logging
from time import sleep

from classic_application.sparkapp import  MySparkApplication

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Launching main application...")
    spark = MySparkApplication.create_spark_Session("My Spark Logging App")
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

