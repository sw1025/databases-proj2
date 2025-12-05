CREATE DATABASE IF NOT EXISTS air_reservation;

USE air_reservation;


CREATE TABLE `airline` (
    `airline_name` varchar(50) NOT NULL,
    PRIMARY KEY(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `airline_staff` (
    `username` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `first_name` varchar(50) NOT NULL,
    `last_name` varchar(50) NOT NULL,
    `date_of_birth` date NOT NULL,
    `airline_name` varchar(50) NOT NULL,
    `role` ENUM('admin', 'operator', 'both') DEFAULT 'admin',
    PRIMARY KEY(`username`),
    FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `airplane` (
 `airline_name` varchar(50) NOT NULL,
 `airplane_id` int(11) NOT NULL,
 `seat_capacity` int(11) NOT NULL,
 PRIMARY KEY(`airline_name`, `airplane_id`),
 FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE
CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `airport` (
 `airport_name` varchar(50) NOT NULL,
 `airport_city` varchar(50) NOT NULL,
 PRIMARY KEY(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `booking_agent` (
 `email` varchar(50) NOT NULL,
 `password` varchar(50) NOT NULL,
 PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `agent_airline_authorization` (
 `agent_email` varchar(50) NOT NULL,
 `airline_name` varchar(50) NOT NULL,
 PRIMARY KEY(`agent_email`,`airline_name`),
 FOREIGN KEY(`agent_email`) REFERENCES `booking_agent`(`email`) ON DELETE
CASCADE,
 FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE
CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `customer` (
    `email` varchar(50) NOT NULL,
    `name` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `building_number` varchar(30) NOT NULL,
    `street` varchar(30) NOT NULL,
    `city` varchar(30) NOT NULL,
    `state` varchar(30) NOT NULL,
    `phone_number` varchar(20) NOT NULL,
    `passport_number` varchar(30) NOT NULL,
    `passport_expiration` date NOT NULL,
    `passport_country` varchar(50) NOT NULL,
    `date_of_birth` date NOT NULL,
    PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `flight` (
    `airline_name` varchar(50) NOT NULL,
    `flight_num` int(11) NOT NULL,
    `departure_airport` varchar(50) NOT NULL,
    `departure_time` datetime NOT NULL,
    `arrival_airport` varchar(50) NOT NULL,
    `arrival_time` datetime NOT NULL,
    `price` decimal(10,0) NOT NULL,
    `status` ENUM('upcoming', 'in-progress', 'delayed') DEFAULT 'upcoming',
    `airplane_id` int(11) NOT NULL,
    PRIMARY KEY(`airline_name`, `flight_num`),
    FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`,`airplane_id`),
    FOREIGN KEY(`departure_airport`) REFERENCES `airport`(`airport_name`),
    FOREIGN KEY(`arrival_airport`) REFERENCES `airport`(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ticket` (
    `ticket_id` int(11) NOT NULL,
    `airline_name` varchar(50) NOT NULL,
    `flight_num` int(11) NOT NULL,
    PRIMARY KEY(`ticket_id`),
    FOREIGN KEY(`airline_name`, `flight_num`) REFERENCES `flight`(`airline_name`,`flight_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `purchases` (
    `ticket_id` int(11) NOT NULL,
    `customer_email` varchar(50) NOT NULL,
    `booking_agent_email` varchar(50),
    `purchase_date` date NOT NULL,
    PRIMARY KEY(`ticket_id`, `customer_email`),
    FOREIGN KEY(`ticket_id`) REFERENCES `ticket`(`ticket_id`),
    FOREIGN KEY(`booking_agent_email`) REFERENCES `booking_agent`(`email`),
    FOREIGN KEY(`customer_email`) REFERENCES `customer`(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--remove attribute seat_capacity from airplane
ALTER TABLE `airplane` DROP COLUMN `seat_capacity`;

--new table seat_class
CREATE TABLE `seat_class` (
    `airline_name` varchar(50) NOT NULL,
    `airplane_id` int(11) NOT NULL,
    `seat_class_id` int(11) NOT NULL,
    `seat_capacity` int(11) NOT NULL,
    PRIMARY KEY(`airline_name`, `airplane_id`, `seat_class_id`),
    FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`,`airplane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--rename attribute price to base_price to flight
ALTER TABLE `flight`RENAME COLUMN price to base_price;

--add constraint of ticket
ALTER TABLE `ticket`

ADD COLUMN `airplane_id` int(11) NOT NULL,
ADD COLUMN `seat_class_id` int(11) NOT NULL,
ADD CONSTRAINT FOREIGN KEY (`airline_name`, `airplane_id`, `seat_class_id`)
REFERENCES `seat_class`(`airline_name`, `airplane_id`, `seat_class_id`);

--add attribute purchase_price to purchases
ALTER TABLE `purchases` ADD COLUMN `purchase_price` decimal(10,0) NOT NULL;