--List all upcoming flights in the system
SELECT *
FROM flight
WHERE `status` = 'upcoming';

--List all delayed flights
SELECT *
FROM flight
WHERE `status` = 'delayed';

-- Show the names of customers who purchased tickets via a booking agent
SELECT `customer`.`name`
FROM `purchases`
LEFT JOIN `customer`
ON `purchases`.`customer_email` = `customer`.`email`
WHERE `purchases`.`booking_agent_email` IS NOT NULL;

--Given an airline name as a parameter, list all airplanes owned by that airline
SELECT `airplane`.`airplane_id`
FROM `airline`
LEFT JOIN `airplane`
ON `airline`.`airline_name` = `airplane`.`airline_name`
WHERE `airline`.`airline_name` = '{airline_name}';