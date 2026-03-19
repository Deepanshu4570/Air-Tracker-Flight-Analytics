CREATE DATABASE flight_db;
USE flight_db;

CREATE TABLE airport (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iata_code VARCHAR(10) UNIQUE,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    timezone VARCHAR(50)
);

CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(20),
    origin VARCHAR(10),
    destination VARCHAR(10),
    departure_time_utc DATETIME,
    arrival_time_utc DATETIME,
    delay_minutes FLOAT,
    status VARCHAR(20),
    aircraft_registration VARCHAR(20),
    airline_iata CHAR(4),
    airline_name VARCHAR(100)
);

CREATE TABLE aircraft (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration VARCHAR(20) UNIQUE,
    model VARCHAR(50)
);
DESCRIBE flights;
DESCRIBE airport;
DESCRIBE aircraft;

select * from airport;
select * from flights;
select * from aircraft;

-- 1. Flights per Aircraft Model

SELECT a.model, COUNT(*) AS total_flights
FROM flights f
JOIN aircraft a 
ON f.aircraft_registration = a.registration
GROUP BY a.model;

-- 2. Aircraft Used More Than 5 Times

SELECT a.registration, a.model, COUNT(*) AS flight_count
FROM flights f
JOIN aircraft a 
ON f.aircraft_registration = a.registration
GROUP BY a.registration, a.model
HAVING COUNT(*) > 5;

-- 3. Outbound Flights per Airport (>5)

SELECT ap.name, COUNT(*) AS total_flights
FROM flights f
JOIN airport ap 
ON f.origin = ap.iata_code
GROUP BY ap.name
HAVING COUNT(*) > 5;

-- 4. Top 3 Destination Airports

SELECT ap.name, ap.city, COUNT(*) AS arrivals
FROM flights f
JOIN airport ap 
ON f.destination = ap.iata_code
GROUP BY ap.name, ap.city
ORDER BY arrivals DESC
LIMIT 3;

-- 5. Domestic vs International
SELECT 
    f.flight_number,
    f.origin,
    f.destination,
    CASE 
        WHEN a1.country = a2.country THEN 'Domestic'
        ELSE 'International'
    END AS flight_type
FROM flights f
JOIN airport a1 ON f.origin = a1.iata_code
JOIN airport a2 ON f.destination = a2.iata_code;

-- 6. 5 Most Recent Arrivals at DEL
SELECT 
    f.flight_number,
    f.aircraft_registration,
    ap.name AS departure_airport,
    f.arrival_time_utc
FROM flights f
JOIN airport ap 
ON f.origin = ap.iata_code
WHERE f.destination = 'DEL'
ORDER BY f.arrival_time_utc DESC
LIMIT 5;

-- 7. Airports with No Arrivals

SELECT a.name
FROM airport a
LEFT JOIN flights f 
ON a.iata_code = f.destination
WHERE f.destination IS NULL;

-- 8. Flights by Status (Airline-wise using CASE)
SELECT 
    airline_name,
    SUM(CASE WHEN status = 'On Time' THEN 1 ELSE 0 END) AS on_time_count,
    SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM flights
GROUP BY airline_name;

-- 9. All Cancelled Flights
SELECT 
    f.flight_number,
    f.aircraft_registration,
    a1.name AS origin_airport,
    a2.name AS destination_airport,
    f.departure_time_utc
FROM flights f
JOIN airport a1 ON f.origin = a1.iata_code
JOIN airport a2 ON f.destination = a2.iata_code
WHERE f.status = 'Canceled'
ORDER BY f.departure_time_utc DESC;

SELECT DISTINCT status FROM flights;

-- Que 10. City Pairs with >2 Aircraft Models
SELECT 
    f.origin,
    f.destination,
    COUNT(DISTINCT a.model) AS aircraft_types
FROM flights f
JOIN aircraft a 
ON f.aircraft_registration = a.registration
GROUP BY f.origin, f.destination
HAVING COUNT(DISTINCT a.model) > 2;

-- Que 11. % of Delayed Flights per Destination
SELECT 
    destination,
    COUNT(CASE WHEN delay_minutes > 0 THEN 1 END) * 100.0 / COUNT(*) AS delay_percentage
FROM flights
GROUP BY destination
ORDER BY delay_percentage DESC;

