# docker-workshop

Workshop Codespaces

## Solutions

### 1. Pip Version

**Answer:** 25.3

```bash
docker run -it --rm --entrypoint=bash python:3.13
pip --version
```

**Output:**
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

### 2. Database Connection

**Answer:** db:5433

### 3. Trip Count

**Answer:** 8007

```sql
SELECT 
  COUNT(*)
FROM green_taxi_trips
WHERE
  DATE(lpep_pickup_datetime) >= '2025-11-01' AND
  DATE(lpep_pickup_datetime) < '2025-12-01' AND
  trip_distance <= 1
```

### 4. Maximum Distance Date

**Answer:** 2025-11-14

```sql
SELECT 
  DATE(lpep_pickup_datetime) AS "pickup_day",
  MAX(trip_distance) AS "max_distance"
FROM green_taxi_trips
WHERE
  trip_distance < 100
GROUP BY
  DATE(lpep_pickup_datetime)
ORDER BY 
  max_distance DESC
```

### 5. Pickup Zone with Highest Total Amount

**Answer:** East Harlem North

```sql
SELECT 
  z."Zone" AS pickup_zone,
  SUM(t.total_amount) AS total_amount_sum
FROM 
  green_taxi_trips t
JOIN
  zones z ON t."PULocationID" = z."LocationID"
WHERE
  DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY
  z."Zone"
ORDER BY 
  total_amount_sum DESC
```

### 6. Dropoff Zone with Maximum Tip

**Answer:** Yorkville West

```sql
SELECT 
  z_drop."Zone" AS dropoff_zone,
  MAX(t.tip_amount) as max_tip
FROM 
  green_taxi_trips t
JOIN
  zones z_pick ON t."PULocationID" = z_pick."LocationID"
JOIN
  zones z_drop ON t."DOLocationID" = z_drop."LocationID"
WHERE
  z_pick."Zone" = 'East Harlem North' AND
  DATE(lpep_pickup_datetime) >= '2025-11-01' AND 
  DATE(lpep_pickup_datetime) < '2025-12-01'
GROUP BY 
  z_drop."Zone"
ORDER BY 
  max_tip DESC
```

### 7. Terraform Commands

**Answer:** terraform init, terraform apply -auto-approve, terraform destroy

```bash
terraform init
terraform apply -auto-approve
terraform destroy
```