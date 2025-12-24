-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: teachmap_db
-- ------------------------------------------------------
-- Server version	8.0.44

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

--
-- Current Database: `teachmap_db`
--

/*!40000 DROP DATABASE IF EXISTS `teachmap_db`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `teachmap_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `teachmap_db`;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `day` varchar(10) NOT NULL,
  `start_time` varchar(10) NOT NULL,
  `end_time` varchar(10) DEFAULT NULL,
  `duration` decimal(3,1) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `course_code` varchar(20) DEFAULT NULL,
  `classroom` varchar(50) DEFAULT NULL,
  `color` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (9,2,'Tue','09:00',NULL,1.5,'Organic Chemistry',NULL,NULL,'#F4B400'),(10,2,'Thu','11:00',NULL,1.5,'Lab Work',NULL,NULL,'#4285F4'),(14,1,'Mon','08:30','11:30',3.0,'คณิตศาสตร์คอมพิวเตอร์','21910-2009','927','#4285f4'),(15,1,'Mon','12:30','17:30',5.0,'โปรแกรมมัลติมีเดียเพื่อการนำเสนอ','20216-2110','927','#DB4437'),(16,1,'Tue','08:30','12:30',4.0,'โปรแกรมมัลติมีเดีย','21910-2015','927','#F4B400'),(17,1,'Tue','13:30','17:30',4.0,'โปรแกรมมัลติมีเดีย','21910-2015','927','#F4B400'),(18,1,'Wed','08:30','12:30',4.0,'การใช้เทคโนโลยีดิจิทัลเพื่ออาชีพ','20001-1005','927','#0F9D58'),(19,1,'Wed','14:30','15:30',1.0,'Home Rome','','927','#673AB7'),(20,1,'Wed','15:30','17:30',2.0,'กิจกรรมสถานประกอบการ','20000-2001','','#E91E63'),(21,1,'Thu','08:30','12:30',4.0,'การใช้เทคโนโลยีดิจิทัลเพื่ออาชีพ','20001-1005','927','#0F9D58'),(22,1,'Thu','13:30','17:30',4.0,'การสร้างเว็บไซต์สำหรับธุรกิจดิจิทัล','21910-2016','927','#E91E63'),(23,1,'Fri','08:30','12:30',4.0,'โปรแกรมมัลติมีเดีย','21910-2015','927','#F4B400'),(24,1,'Fri','13:30','17:30',4.0,'โปรแกรมสร้างภาพเคลื่อนไหว','21910-2014','','#FF5722');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (2,'66202040113','1219901066596','พีรพัฒน์ เกาะลอย','2025-11-27 09:11:34'),(4,'dbt','1234','test','2025-11-28 07:06:07');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'teacher1','1234','นางสาวศิริรัตน์ เชื้อแก้ว','เทคโนโลยีธุรกิจดิจิทัล','089-000-1236','ห้อง 927','2025-11-26 13:37:14'),(2,'teacher2','1234','Prof. Emily Johnson','Chemistry','089-000-1237','Room 202','2025-11-26 13:37:14');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-07 14:38:24
