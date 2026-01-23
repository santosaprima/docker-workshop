# docker-workshop

Workshop Codespaces

## Solutions Module 2
Can refer to workflow -> homework-flow.yaml

### 1. Uncompressed file size

**Answer:** 128.3MiB

**Steps:**
```
Kestra -> Flow -> Executions -> Outputs -> extract -> outputFiles -> file size
Make sure to remove these lines:
- id: purge_files
    type: io.kestra.plugin.core.storage.PurgeCurrentExecutionFiles
    description: This will remove output files. If you'd like to explore Kestra outputs, disable it.

taskCache: (if cached already)
      enabled: true
```

### 2. Rendered value

**Answer:** green_tripdata_2020-04.csv

**Explanation:**
```
file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"

inputs.taxi = green
inputs.year = 2020
inputs.month = 04
```

### 3. Rows count for yellow taxi data in the year 2020

**Answer:** 24,648,499

**Steps:**
```
1. Using Kestra with backfill provide start date 2020-01-01 00:00:00 and end date 2021-01-01 00:00:00 and select yellow
2. In pgadmin dashboard do sql query: 
SELECT COUNT(*) FROM yellow_tripdata;
```

### 4. Rows count for green taxi data in the year 2020

**Answer:** 1,734,051

**Steps:**
```
1. Using Kestra with backfill provide start date 2020-01-01 00:00:00 and end date 2021-01-01 00:00:00 and select green
2. In pgadmin dashboard do sql query: 
SELECT COUNT(*) FROM green_tripdata;
```

### 5. Rows count for yellow taxi data for march 2021

**Answer:** 1,925,152

**Steps:**
```
1. Using Kestra with execute flow with input: 
taxi = yellow
year = 2021
month = 03

2. In pgadmin dashboard do sql query: 
SELECT COUNT(*) FROM yellow_tripdata;
```

### 6. Add timezone to New York in schedule trigger

**Answer:** Add a timezone property set to America/New_York in the Schedule trigger configuration

**Example:**
```
- id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    timezone: America/New_York
    inputs:
      taxi: yellow
```
