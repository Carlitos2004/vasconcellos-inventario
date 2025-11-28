-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: inventario_automotriz
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `total_compra` decimal(10,2) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (52,1,21,400.00,8400.00,'2025-11-28 01:43:49');
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lavados`
--

DROP TABLE IF EXISTS `lavados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lavados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(255) NOT NULL,
  `precio` int NOT NULL,
  `fecha` datetime NOT NULL,
  `detalles` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lavados`
--

LOCK TABLES `lavados` WRITE;
/*!40000 ALTER TABLE `lavados` DISABLE KEYS */;
INSERT INTO `lavados` VALUES (12,'lavado full',434000,'2025-11-28 01:44:24','don juan');
/*!40000 ALTER TABLE `lavados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos`
--

DROP TABLE IF EXISTS `movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos`
--

LOCK TABLES `movimientos` WRITE;
/*!40000 ALTER TABLE `movimientos` DISABLE KEYS */;
INSERT INTO `movimientos` VALUES (48,1,'COMPRA',5,'2025-11-14 12:09:08'),(49,1,'VENTA',2,'2025-11-14 12:09:49');
/*!40000 ALTER TABLE `movimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(255) NOT NULL,
  `etiqueta` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'HYUNDAI Teer G700 SP 10W-40','Aceite Motor',2000.00,9),(2,'HYUNDAI Teer D700 C2/C3 5W-30','Aceite Motor',0.00,0),(3,'MORE Ciclón SAE 20W/50','Aceite Motor',0.00,0),(4,'LUBRAX Tecno Si 10W-40','Aceite Motor',0.00,0),(5,'Shell Helix HX7 10W-40','Aceite Motor',0.00,0),(6,'Shell Helix HX8 Profesional 5W-30','Aceite Motor',0.00,0),(7,'Quartz 7000 10W-40','Aceite Motor',0.00,0),(8,'Quartz Ineo MCS 5W-30','Aceite Motor',0.00,0),(9,'Mobil Super 2000 10W-40','Aceite Motor',0.00,0),(10,'Mobil Super 3000 5W-30','Aceite Motor',0.00,0),(11,'Energy Premium 7908 SAE 5W-30','Aceite Motor',0.00,0),(12,'Energy Premium 7508 Mannol 5W-30','Aceite Motor',0.00,0),(13,'Classic 7501 Mannol 10W-40','Aceite Motor',0.00,0),(14,'Motul 6100 Syn-clean FE 5W-30','Aceite Motor',0.00,0),(15,'Liqui Moly 10W-40 Super Leichtlauf','Aceite Motor',0.00,0),(16,'Engine Oil 9976 Senfineco','Aceite Motor',0.00,0),(17,'DEXRON /// LUBRAX ATF TDX','Transmisión',0.00,0),(18,'VISTONY GEAR OIL Synthetic 75W-90','Transmisión',0.00,0),(19,'Fuel Injector Cleaner Senfineco','Aditivo',0.00,0),(20,'Brake Fluid DOT 3 Synthetic','Aditivo',0.00,0),(21,'DPF Foam Cleaner','Aditivo',0.00,0),(22,'Anticongelante Refrigerante 50/50 Ciclón','Refrigerante',0.00,0),(23,'Ice Freeze 33% Orgánico Vistony','Refrigerante',0.00,0),(24,'Anticongelante Ciclón 33%','Refrigerante',0.00,0),(25,'Coolant 715 Anticongelante','Refrigerante',0.00,0),(26,'Ciclón Coolant B-712','Refrigerante',0.00,0),(27,'Coolant Diesel Anticongelante','Refrigerante',0.00,0),(28,'Líquido para radiador verde','Refrigerante',0.00,0),(29,'Líquido para radiador rojo','Refrigerante',0.00,0),(30,'Agua desmineralizada','Refrigerante',0.00,0),(31,'Tapia Lavado en seco','Limpieza Exterior',0.00,0),(32,'Tapia Shampoo cera con carnauba','Limpieza Exterior',0.00,0),(33,'MAGIO COLOR CAR WASH WAX WATER','Limpieza Exterior',0.00,0),(34,'Cera Carnauba','Limpieza Exterior',0.00,0),(35,'Black Ciclón','Limpieza Exterior',0.00,0),(36,'Frutes Ciclón','Limpieza Exterior',0.00,0),(37,'Ice Blue Ciclón','Limpieza Exterior',0.00,0),(38,'Shampoo concentrado','Limpieza Exterior',0.00,0),(39,'Arlon Pintura Spray','Pintura',0.00,0),(40,'Strong Ultra Seal','Protección',0.00,0),(41,'GUYS HIGH GLOSS','Cera Detailing',0.00,0),(42,'CHEMICAL GUYS ACTIVE FUSION SHINE','Cera Detailing',0.00,0),(43,'EMICA CIELOM GUYS SHINE SPEED WIPE','Cera Detailing',0.00,0),(44,'Fabric Clean','Limpieza Interior',0.00,0),(45,'INNER CLEAN Interior Quick Detailer','Limpieza Interior',0.00,0),(46,'Tapia Plastic Restorer','Limpieza Interior',0.00,0),(47,'Tapia Protection Pro','Limpieza Interior',0.00,0),(48,'CHEMICAL GUYS Leather Cleaner/Conditioner','Limpieza Interior',0.00,0),(49,'Arlon limpia tapiz espuma','Limpieza Interior',0.00,0),(50,'AllClean All Purpose Cleaner Degreaser','Limpieza Interior',0.00,0),(51,'Water Stain Cleaner Deep Cleaner','Limpieza Interior',0.00,0),(52,'Water Spot Remover','Limpieza Interior',0.00,0),(53,'STRONG R GLASS CLEANER','Vidrios',0.00,0),(54,'Anti empañante','Vidrios',0.00,0),(55,'Limpia parabrisas','Vidrios',0.00,0),(56,'Desengrasante de motor','Motor',0.00,0),(57,'Limpia contactos eléctricos','Motor',0.00,0),(58,'Renovador de neumáticos','Renovadores',0.00,0),(59,'Silicona para tableros','Renovadores',0.00,0),(60,'Silicona aromática','Renovadores',0.00,0),(61,'Desodorante neutralizador tabaco','Aromas',0.00,0),(62,'Little Trees','Aromas',0.00,0),(63,'Limpiador de llantas','Llantas',0.00,0),(64,'Wheel Hub Cleaner STRONG CLEANER','Llantas',0.00,0),(65,'POLISHING AGENT W21','Pulido',0.00,0),(66,'STRONG FINAL TOUGH','Pulido',0.00,0),(67,'HEAVY D METAL POLISH','Pulido',0.00,0),(68,'Batería Platin Silver','Accesorio',0.00,0),(69,'BRM Plumilla Universal','Accesorio',0.00,0),(70,'Pinturas colores','Pintura',0.00,0),(71,'HYUNDAI Teer G700 SP 10W-40','Aceite Motor',0.00,0),(72,'HYUNDAI Teer D700 C2/C3 5W-30','Aceite Motor',0.00,0),(73,'MORE Ciclón SAE 20W/50','Aceite Motor',0.00,0),(74,'LUBRAX Tecno Si 10W-40','Aceite Motor',0.00,0),(75,'Shell Helix HX7 10W-40','Aceite Motor',0.00,0),(76,'Shell Helix HX8 Profesional 5W-30','Aceite Motor',0.00,0),(77,'Quartz 7000 10W-40','Aceite Motor',0.00,0),(78,'Quartz Ineo MCS 5W-30','Aceite Motor',0.00,0),(79,'Mobil Super 2000 10W-40','Aceite Motor',0.00,0),(80,'Mobil Super 3000 5W-30','Aceite Motor',0.00,0),(81,'Energy Premium 7908 SAE 5W-30','Aceite Motor',0.00,0),(82,'Energy Premium 7508 Mannol 5W-30','Aceite Motor',0.00,0),(83,'Classic 7501 Mannol 10W-40','Aceite Motor',0.00,0),(84,'Motul 6100 Syn-clean FE 5W-30','Aceite Motor',0.00,0),(85,'Liqui Moly 10W-40 Super Leichtlauf','Aceite Motor',0.00,0),(86,'Engine Oil 9976 Senfineco','Aceite Motor',0.00,0),(87,'DEXRON /// LUBRAX ATF TDX','Transmisión',0.00,0),(88,'VISTONY GEAR OIL Synthetic 75W-90','Transmisión',0.00,0),(89,'Fuel Injector Cleaner Senfineco','Aditivo',0.00,0),(90,'Brake Fluid DOT 3 Synthetic','Aditivo',0.00,0),(91,'DPF Foam Cleaner','Aditivo',0.00,0),(92,'Anticongelante Refrigerante 50/50 Ciclón','Refrigerante',0.00,0),(93,'Ice Freeze 33% Orgánico Vistony','Refrigerante',0.00,0),(94,'Anticongelante Ciclón 33%','Refrigerante',0.00,0),(95,'Coolant 715 Anticongelante','Refrigerante',0.00,0),(96,'Ciclón Coolant B-712','Refrigerante',0.00,0),(97,'Coolant Diesel Anticongelante','Refrigerante',0.00,0),(98,'Líquido para radiador verde','Refrigerante',0.00,0),(99,'Líquido para radiador rojo','Refrigerante',0.00,0),(100,'Agua desmineralizada','Refrigerante',0.00,0),(101,'Tapia Lavado en seco','Limpieza Exterior',0.00,0),(102,'Tapia Shampoo cera con carnauba','Limpieza Exterior',0.00,0),(103,'MAGIO COLOR CAR WASH WAX WATER','Limpieza Exterior',0.00,0),(104,'Cera Carnauba','Limpieza Exterior',0.00,0),(105,'Black Ciclón','Limpieza Exterior',0.00,0),(106,'Frutes Ciclón','Limpieza Exterior',0.00,0),(107,'Ice Blue Ciclón','Limpieza Exterior',0.00,0),(108,'Shampoo concentrado','Limpieza Exterior',0.00,0),(109,'Arlon Pintura Spray','Pintura',0.00,0),(110,'Strong Ultra Seal','Protección',0.00,0),(111,'GUYS HIGH GLOSS','Cera Detailing',0.00,0),(112,'CHEMICAL GUYS ACTIVE FUSION SHINE','Cera Detailing',0.00,0),(113,'EMICA CIELOM GUYS SHINE SPEED WIPE','Cera Detailing',0.00,0),(114,'Fabric Clean','Limpieza Interior',0.00,0),(115,'INNER CLEAN Interior Quick Detailer','Limpieza Interior',0.00,0),(116,'Tapia Plastic Restorer','Limpieza Interior',0.00,0),(117,'Tapia Protection Pro','Limpieza Interior',0.00,0),(118,'CHEMICAL GUYS Leather Cleaner/Conditioner','Limpieza Interior',0.00,0),(119,'Arlon limpia tapiz espuma','Limpieza Interior',0.00,0),(120,'AllClean All Purpose Cleaner Degreaser','Limpieza Interior',0.00,0),(121,'Water Stain Cleaner Deep Cleaner','Limpieza Interior',0.00,0),(122,'Water Spot Remover','Limpieza Interior',0.00,0),(123,'STRONG R GLASS CLEANER','Vidrios',0.00,0),(124,'Anti empañante','Vidrios',0.00,0),(126,'Desengrasante de motor','Motor',0.00,0),(127,'Limpia contactos eléctricos','Motor',0.00,0),(128,'Renovador de neumáticos','Renovadores',0.00,0),(129,'Silicona para tableros','Renovadores',0.00,0),(130,'Silicona aromática','Renovadores',0.00,0),(131,'Desodorante neutralizador tabaco','Aromas',0.00,0),(132,'Little Trees','Aromas',0.00,0),(133,'Limpiador de llantas','Llantas',0.00,0),(134,'Wheel Hub Cleaner STRONG CLEANER','Llantas',0.00,0),(135,'POLISHING AGENT W21','Pulido',0.00,0),(136,'STRONG FINAL TOUGH','Pulido',0.00,0),(137,'HEAVY D METAL POLISH','Pulido',0.00,0),(138,'Batería Platin Silver','Accesorio',0.00,0),(139,'BRM Plumilla Universal','Accesorio',0.00,0),(140,'Pinturas colores','Pintura',0.00,0);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (31,1,12,2000.00,24000.00,'2025-11-28 01:44:02');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28  1:49:15
