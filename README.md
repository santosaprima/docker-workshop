# docker-workshop
Workshop Codespaces

Solutions
1. 25.3
$ docker run -it --rm --entrypoint=bash python:3.13
$ pip --version
Output: pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

2. db:5433

3. 8007
SELECT 
	COUNT(*)
FROM green_taxi_trips
WHERE
    DATE(lpep_pickup_datetime) >= '2025-11-01' AND
    DATE(lpep_pickup_datetime) < '2025-12-01' AND
	trip_distance <= 1

4. 2025-11-14
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

5. East Harlem North
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

6. Yorkville West
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

7. terraform init, terraform apply -auto-approve, terraform destroy