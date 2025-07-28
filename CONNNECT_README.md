## Spark Connect Pyspark application
This is the read me for Classic Spark Application written in python.
This runs the spark Application in local mode and spins the Spark JVM locally.

## Local Python Env setup
We will use conda to setup the local python isolated environment to manage dependency.

```bash
conda create -n sparkconnect-pyspark-app python=3.10
conda activate sparkconnect-pyspark-app

pip install setuptools wheel build
```

## Building the Package Distribution
This is only required when you are done with the changes and want to ship this package for the peoduction deployment / run

```bash
python -m build
```

- It will generate the `zip` and `.wheel` file which can be uploaded to S3  or any other storage and passed as `--py-files` dependency
  while running on remote spark cluster.
- I will not build a FAT python jar. so the dependencies (!= dev) will be installed along with it.
- we will take about this in later section. For now, skip this step and will come bck later.

## Dependencies for Local Development
- Install required dependencies for this pachage
```
pip install '.[dev]'
or
pip install pyspark==4.0.0
pip install pyspark[connect]==4.0.0
```
For running spark connect based python program, we dont have to use `spark-submit` or need any spark runtime available. 
The Spark Connect server needs to be run separately before starting ths python program.


## Running the Spark Application Locally

### Step-1: Start the Spark Connect Sever locally
Before we can run the python program, we need to run the Spark Connect server.
- Follow the official spark documentation to download `spark-4.o.0.` binary and extract it.
- Set up JAva and scala version 
- Run the spark connect server in a different terminal
- We do not have to use any specifi python evn for this. The spark connect server can run in its own python env
```bash
cd SPARK_HOME
./sbin/start-connect-server.sh
<<<<<<<<< this starts the spark connect server >>>>>
----
25/07/27 21:50:12 INFO SparkConnectServer: Spark Connect server started at: 0:0:0:0:0:0:0:0:15002
----
````


### Step-2: Run the SparkApplication using `python` directly.

- The file `main_sparkconnect.py` is the entry point for our spark connect application. Its inside the `sparkconnect_application` package on purpose.
- We can directly run `python main_sparkconnect.py` from the same conda environment we had created earlier.
 This depends on the local installs of the current package and the `pyspark`  and `sparkconnect` dependencies which were installed.

### Option-2: Run using `spark-submit` and same conda env
Not Applicable for running spark-connect based python program. These program run direcly on the client python env and dont need any spark runtime

- you do NOT need spark-submit for Spark Connect-based applications.
Because:
- The client application (your Python or Java code) uses a lightweight Spark Connect client. 
- The Spark driver and executors run remotely on the Spark Connect server. 
- The client just sends logical plans via gRPC and receives results. 
- You only need the Spark Connect client library (like pyspark>=4.0.0) locally.


## Using a Dedicated python runtime for Spark Driver Session
There may be a situation, where we need to provide some specific python libraries to the spark runtime for executing the 
workload. These dependencies needs to be installed on the Spark CLuster where the Spark connect server is running.

The client only needs the dependencies which are required for process the client side logic.  
This is different from the classic mode where the Spark Client application and the Spark Driver runtime shared the same python runtime as the 
application was running in client mode. 

With Spark Connect based application development, the client application and the spark driver application was decoupled eacr residing in its own 
environment. 

With Spark connect, the client compute also needs to be heavy if the worklaod reads too much output from the dataframes as it will be fetched to the 
client side from server. This is one drawback / disadvantage of spark connect application. Its now client heavy too when it comes to result 
process. 

We still have option to push the heavy computation to the server side. I wil write some example for that in future on 
how we can do the processing of `df` on server side .. mostly using UDFs.

- The client may consume more RAM (e.g., due to deserialized Arrow batches, local Python object creation)
- Your client app now bundles more logic/libraries, making it heavier
- network presure:Depending on what data is collect()-ed back, client may pull large results
- You may need to tune Arrow memory limits, JVM flags for compatibility, etc.









