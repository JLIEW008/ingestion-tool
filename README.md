# Data ingestion tool
Simple and easy to use ingestion tool. Can be used in conjunction with scheduling tools like cron or Airflow to ingest data periodically.

Currently, this tool can be used to ingest data from SGX website. It can be easily extended to other sources if necessary. 

Key features:
 - fast [runs in parallel, caching relevant information]
 - relatively robust [timeouts, auto-retries]
 - config-based (easily extensible, refer to config.yaml)
 - automatic - some code running behind the scene to ensure the user does not require additional inputs
 - logging

## Instructions to launch Job
1. Ensure you are at the root of the file
2. Ensure that you are using python 3
3. Create and launch a virtual env using requirements.txt
4. Run python main.py src/config.yaml <--date - optional, will load latest available if not provided>

## Design Overview
### Folder Structure 
```
root
| - requirements.txt   (Used to create virutal env)
| - data                          (Folders with data)
| - logs                           (log files)
| - mapping                  (Used by StrParser - elaborated below)
| - src                             (Code)
    | - execeptions         (Custom exceptions)
    | - sgx                         (SGX related classes - inherited from base classes)
    | - <Code files>
```
### Classes/Files description
#### Runner.py
Main class. Do the relevant calls to setup and runs jobs according to the config provided.

#### config.yaml
 - Configuration file to allow setting of general details like log file output, concurrency, data sources and the corresponding details.
Allows variables in brackets {} which will be converted to actual values by StrParser

#### ConfigParser.py
Parses the configuration and manipulates the data to be easily used by the processes. 
Uses StrParser.

#### StrParser.py
Transforms variables in config to the correct values. Some of the operations are:
 - Time: E.g. %Y-%m-%d -> 2020-01-15
 - Variables: E.g. {SGX_DATE} -> 4510 (Uses InfoGenerator to obtain mapping)

#### InfoGenerator/SGXInfoGenerator
Class to provide mapping for StrParser to understand how to transform config variables to actual values. Generates the mapping and provides them to StrParser.

#### Process/DLProcess
Actual process to run the job. DL Process is used for download operations from the internet. Process can be extended to ingest from other sources. E.g. SQL

#### ProcessFactory/InfoGeneratorFactory
Factory class to return the correct object (Process/InfoGenerator) according to type. 


## Future Work
P0 Add implementations for other sources (SQL etc)
P1 Extend concurrency to handle a distributed environment (Multiple machines)
P1 Migrate to stateless to make it easier to scale
