-- MySQL dump 10.13  Distrib 26.10.0, for macos15 (arm64)
--
-- Host: localhost    Database: RideShare
-- ------------------------------------------------------
-- Server version	26.10.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '80fef934-d25f-11f1-9777-f4af92cd4f23:1-118';

--
-- Current Database: `RideShare`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `RideShare` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `RideShare`;

--
-- Table structure for table `Driver`
--

DROP TABLE IF EXISTS `Driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Driver` (
  `driver_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `driver_mode` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`driver_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Driver`
--

LOCK TABLES `Driver` WRITE;
/*!40000 ALTER TABLE `Driver` DISABLE KEYS */;
INSERT INTO `Driver` VALUES (1,'jsmith','Jordan','Smith',1),(2,'kbrown','Kayla','Brown',1),(3,'lwilson','Luis','Wilson',0),(4,'mtaylor','Maya','Taylor',0);
/*!40000 ALTER TABLE `Driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ride`
--

DROP TABLE IF EXISTS `Ride`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ride` (
  `ride_id` int NOT NULL AUTO_INCREMENT,
  `rider_id` int NOT NULL,
  `driver_id` int NOT NULL,
  `pickup_location` varchar(100) NOT NULL,
  `dropoff_location` varchar(100) NOT NULL,
  `ride_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rating` tinyint DEFAULT NULL,
  PRIMARY KEY (`ride_id`),
  KEY `rider_id` (`rider_id`),
  KEY `driver_id` (`driver_id`),
  CONSTRAINT `ride_ibfk_1` FOREIGN KEY (`rider_id`) REFERENCES `Rider` (`rider_id`),
  CONSTRAINT `ride_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `Driver` (`driver_id`),
  CONSTRAINT `ride_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ride`
--

LOCK TABLES `Ride` WRITE;
/*!40000 ALTER TABLE `Ride` DISABLE KEYS */;
INSERT INTO `Ride` VALUES (1,1,1,'Chapman University','John Wayne Airport','2026-10-01 08:15:00',5),(2,2,1,'Old Towne Orange','Disneyland','2026-10-02 13:40:00',4),(3,3,2,'Irvine Spectrum','Chapman University','2026-10-03 18:05:00',5),(4,4,3,'Fashion Island','Newport Beach Pier','2026-10-04 11:20:00',3),(5,5,2,'Angel Stadium','Honda Center','2026-10-05 19:00:00',4),(6,1,4,'Chapman University','South Coast Plaza','2026-10-07 15:30:00',5),(7,2,4,'Disneyland','Downtown Disney','2026-10-12 21:15:00',NULL),(8,3,1,'Santa Ana Train Station','Chapman University','2026-10-14 07:45:00',2),(9,4,2,'Orange Circle','Tustin District','2026-10-20 10:00:00',NULL),(10,5,3,'The Block at Orange','Angel Stadium','2026-10-25 17:25:00',4);
/*!40000 ALTER TABLE `Ride` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rider`
--

DROP TABLE IF EXISTS `Rider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Rider` (
  `rider_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  PRIMARY KEY (`rider_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rider`
--

LOCK TABLES `Rider` WRITE;
/*!40000 ALTER TABLE `Rider` DISABLE KEYS */;
INSERT INTO `Rider` VALUES (1,'amartinez','Ana','Martinez'),(2,'bchen','Brian','Chen'),(3,'cpatel','Chloe','Patel'),(4,'dnguyen','Daniel','Nguyen'),(5,'ejohnson','Emma','Johnson');
/*!40000 ALTER TABLE `Rider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'RideShare'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-09 21:12:56
