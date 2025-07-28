## Classics Pyspark application 
This is the read me for Classic Spark Application written in python. 
This runs the spark Application in local mode and spins the Spark JVM locally.

## Local Python Env setup
We will use conda to setup the local python isolated environment to manage dependency.

```bash
conda create -n classic-pyspark-app python=3.10
conda activate classic-pyspark-app

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
```

This is great for local development, testing, and CI/CD pipelines.

**This does the following:**
- Downloads Spark binaries (core JARs, launchers, etc.) as part of the package.
- `<PYTHON_HOME>/python3.10/site-packages/pyspark/jars/` -> has the jars
- Provides a Python wrapper (pyspark) which:
- Spawns the JVM using subprocess
- Points the classpath to internal Spark JARs
- Connects your Python code to the JVM using Py4J

**No need to manually set `SPARK_HOME` or `spark-submit`, unless you're doing something custom 
(like Spark on a cluster, or deploying on YARN, etc.)**
- `spark-submit` is not really needed for local-mode development for testing unless we want to use 
some custom spark runtime version. 


### Running the Spark Application Locally
#### Option-1: Run using `python` executable directly.
- The file `main.py` is the entry point for our spark application. 
- We can directly run `python main.py` from the conda environment we had created.
This depends on the local installs of the current package and the `pyspark` which was installed

#### Option-2: Run using `spark-submit` and same conda env
This option is useful, if you have your own spark-runtime setup. I have downloaded a pre-compiled
`spark-4.0.0` runtime from official spark page and have set it up is a differenet location in laopt.

-  we will trigger the spark application using the `spark-submit` executable which will spin the python application.
```bash
conda activcate classic-pyspark-app
export PYSPARK_PYTHON=$(which python)
```
- trigger the `spark-submit` assuming the spark runtime is availabe at `SPARK_HOME` folder. 
```bash
cd <SPARK_HOME>
./bin/spark-submit /Users/rhgoyal/learning/github-repos/pyspark-applications/main.py
```
- the above execution should work fine as spark will be using the current conda env `python` as the python runtime 
which already ahs all the required dependencies installed.

## Using a Dedicated conda env and custom spark runtime 
In this option, we will try to mimic a production scenario where the python runtime environment 
will be different and will be provided by the cluster with minimal dependencies included.

The net Delta / difference is:  
- We have will a different `python environment` which will be used by the spark runtime.  
- The Spark Application entry point file `main.py` will also be supplied without its dependency. Probably as a single file.
- We need to enable `main.py` to resolve the `MySparkApplication` dependency and any other dependency for that matter which is required. 

### step-1: Create a Python Env
```bash
conda create -n pyspark-classic-app-testenv python=3.10
conda activate pyspark-classic-app-testenv
```

### Option-0: This will not work
- Run the application 
```bash
cd <SPARK_HOME>
# copy the main.py file to SPARK_HOME for mimicing the actual prod scenario. 
cp <>/main.py main.py
<SPARK_HOME>./bin/spark-submit main.py

## error 
ModuleNotFoundError: No module named 'classic_application'
```
**Lets see how we can fix this.**

### Option-1: Install the `pyspark_classic_application` wheel / zip file
- Assuming that the dist file for the project was build already in **Building the Package Distribution** step. If not, build it.
```bash
conda activate pyspark-classic-app-testenv
cd SPARK_HOME

# install dependency package
pip install <PROJECT-HOME>/pyspark-applications/dist/pyspark_classic_application-1.0.0-py3-none-any.whl
<<<<<<<<< installs the package along with its dependencies if any >>>>>>>>>>>>>>

# validate
pip list | grep classic
> pyspark-classic-application 1.0.0
```

- Lets run the Spark Application file again 
```bash
cd SPARK_HOME
cp <PROJECT_HOME>/main.py main.py

<SPARK_HOME>./bin/spark-submit main.py 
```
- This should run fine and the application would get executed.


### Option-2: Packaging a Conda env as virtual environment. (Advanced option) 

This is useful in scenarios where you want to have complete control over the dependencies 
of you application and dont want any arbitary version of the dependencies to be installed 
at runtime on the cluster.

There are option provided to create a virtual env and 

```bash
# initialize a python virtual environment
python3 -m venv pyspark_venvsource
source pyspark_venvsource/bin/activate

# optionally, ensure pip is up-to-date
pip3 install --upgrade pip

# install the python packages
pip3 install scipy
pip3 install matplotlib

# package the virtual environment into an archive
pip3 install venv-pack
venv-pack -f -o pyspark_venv.tar.gz

# copy the archive to an S3 location
aws s3 cp pyspark_venv.tar.gz s3://some-s3-demo-bucket/location/<<>>

```

- Use this along with `--conf spark.archives` option to pass the environemnt name and set the 
- python path using the spark configs. 






