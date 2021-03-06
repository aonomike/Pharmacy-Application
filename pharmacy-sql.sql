CREATE DATABASE  IF NOT EXISTS `arvdispenser` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `arvdispenser`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: 127.0.0.1    Database: arvdispenser
-- ------------------------------------------------------
-- Server version	5.6.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointments_tracker`
--

DROP TABLE IF EXISTS `appointments_tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appointments_tracker` (
  `appointment_date` date NOT NULL,
  `slots_taken` int(11) DEFAULT NULL,
  PRIMARY KEY (`appointment_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblartpatientmasterinformation`
--

DROP TABLE IF EXISTS `tblartpatientmasterinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblartpatientmasterinformation` (
  `cccNumber` varchar(45) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `middleName` varchar(45) DEFAULT NULL,
  `surname` varchar(45) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `dateTherapyStarted` datetime DEFAULT NULL,
  `cellPhone` varchar(45) DEFAULT NULL,
  `dateOfBirth` datetime DEFAULT NULL,
  `pregnant` tinyint(1) NOT NULL DEFAULT '0',
  `clientSupportedBy` int(11) DEFAULT NULL,
  `otherDiseaseConditions` longtext,
  `ADRorSideEffects` longtext,
  `otherDrugs` longtext,
  `typeOfService` varchar(15) DEFAULT NULL,
  `currentStatus` int(11) DEFAULT NULL,
  `regimen` varchar(45) DEFAULT NULL,
  `artStartDate` datetime DEFAULT NULL,
  `address` varchar(145) DEFAULT NULL,
  `clientSourceId` int(11) DEFAULT NULL,
  `cotrimoxazole` tinyint(1) NOT NULL DEFAULT '0',
  `TB` tinyint(1) NOT NULL DEFAULT '0',
  `placeOfBirth` varchar(45) DEFAULT NULL,
  `alternateContact` varchar(45) DEFAULT NULL,
  `smokes` tinyint(1) NOT NULL DEFAULT '0',
  `drinks` tinyint(1) NOT NULL DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `cccNumber_UNIQUE` (`cccNumber`),
  KEY `tblartpatientmasterinformation_ce130bfd` (`typeOfService`),
  KEY `tblartpatientmasterinformation_5eef0aa4` (`clientSourceId`),
  KEY `tblartpatientmasterinformation_acf758bc` (`clientSupportedBy`),
  KEY `tblartpatientmasterinformation_6e0950c6` (`currentStatus`),
  KEY `regimen_refs_regimen_idx` (`regimen`),
  CONSTRAINT `clientSourceId_refs_id_a8d0477e` FOREIGN KEY (`clientSourceId`) REFERENCES `tblclientsource` (`id`) ON DELETE CASCADE ON UPDATE SET NULL,
  CONSTRAINT `clientSupportedBy_refs_clientSupportId_4183fbb6` FOREIGN KEY (`clientSupportedBy`) REFERENCES `tblclientsupportdetails` (`clientSupportId`),
  CONSTRAINT `currentStatus_refs_currentStatusID_c0cb0d3b` FOREIGN KEY (`currentStatus`) REFERENCES `tblcurrentstatus` (`currentStatusID`),
  CONSTRAINT `regimen_refs_regimencode` FOREIGN KEY (`regimen`) REFERENCES `tblregimen` (`regimenCode`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7728 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblclientsource`
--

DROP TABLE IF EXISTS `tblclientsource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblclientsource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sourceName` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblclientsupportdetails`
--

DROP TABLE IF EXISTS `tblclientsupportdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblclientsupportdetails` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `clientSupportId` int(11) NOT NULL AUTO_INCREMENT,
  `clientSupport` varchar(45) NOT NULL,
  PRIMARY KEY (`clientSupportId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblcurrentstatus`
--

DROP TABLE IF EXISTS `tblcurrentstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblcurrentstatus` (
  `currentStatusID` int(11) NOT NULL AUTO_INCREMENT,
  `currentStatus` varchar(45) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`currentStatusID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldistricts`
--

DROP TABLE IF EXISTS `tbldistricts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldistricts` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `districtCode` int(11) NOT NULL AUTO_INCREMENT,
  `districtName` varchar(45) NOT NULL,
  `regionId` int(11) NOT NULL,
  PRIMARY KEY (`districtCode`),
  KEY `tbldistricts_40ac8943` (`regionId`),
  CONSTRAINT `regionId_refs_regionCode_9e2a7d79` FOREIGN KEY (`regionId`) REFERENCES `tblregion` (`regionCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldosage`
--

DROP TABLE IF EXISTS `tbldosage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldosage` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `dose` varchar(20) NOT NULL,
  `value` double DEFAULT NULL,
  `frequency` int(11) DEFAULT NULL,
  `upsize_ts` datetime DEFAULT NULL,
  PRIMARY KEY (`dose`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugbrandname`
--

DROP TABLE IF EXISTS `tbldrugbrandname`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugbrandname` (
  `arvDrugsID` varchar(200) NOT NULL,
  `brandName` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`arvDrugsID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugdestination`
--

DROP TABLE IF EXISTS `tbldrugdestination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugdestination` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugphysicaltran`
--

DROP TABLE IF EXISTS `tbldrugphysicaltran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugphysicaltran` (
  `arvDrugId` varchar(50) NOT NULL,
  `tranBatch` varchar(20) NOT NULL,
  `expiryDate` datetime DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `transactionDate` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `stockTransactionNumber` int(11) NOT NULL AUTO_INCREMENT,
  `transactionType` int(11) NOT NULL DEFAULT '13',
  `remarks` varchar(255) DEFAULT NULL,
  `unitCost` decimal(10,0) DEFAULT NULL,
  `ref_number` varchar(45) DEFAULT NULL,
  `source_or_destination` varchar(100) DEFAULT NULL,
  `packs` int(11) DEFAULT NULL,
  PRIMARY KEY (`stockTransactionNumber`),
  KEY `tbldrugphysicaltran_3fc0fa04` (`arvDrugId`),
  KEY `tbldrugphysicaltran_02d30382` (`transactionType`),
  CONSTRAINT `transactionType_refs_id_2dae875e` FOREIGN KEY (`transactionType`) REFERENCES `tblstocktransactiontype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=238 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugsinregimen`
--

DROP TABLE IF EXISTS `tbldrugsinregimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugsinregimen` (
  `regimenCode` varchar(50) DEFAULT NULL,
  `combinations` varchar(200) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tbldrugsinregimen_704e30e7` (`regimenCode`)
) ENGINE=InnoDB AUTO_INCREMENT=1440 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugsource`
--

DROP TABLE IF EXISTS `tbldrugsource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugsource` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sourceCode` int(11) NOT NULL AUTO_INCREMENT,
  `sourceName` varchar(45) NOT NULL,
  PRIMARY KEY (`sourceCode`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbldrugunit`
--

DROP TABLE IF EXISTS `tbldrugunit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldrugunit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `unitName` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblgenericname`
--

DROP TABLE IF EXISTS `tblgenericname`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblgenericname` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `genericName` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblhealthfacility`
--

DROP TABLE IF EXISTS `tblhealthfacility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblhealthfacility` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `mflCode` int(11) NOT NULL,
  `facilityName` varchar(45) NOT NULL,
  `districtCode` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mflCode` (`mflCode`),
  UNIQUE KEY `mflCode_2` (`mflCode`,`facilityName`),
  KEY `tblhealthfacility_5b3f277e` (`districtCode`),
  CONSTRAINT `districtCode_refs_districtCode_904b29c7` FOREIGN KEY (`districtCode`) REFERENCES `tbldistricts` (`districtCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblindication`
--

DROP TABLE IF EXISTS `tblindication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblindication` (
  `indicationCode` varchar(10) NOT NULL,
  `indicationName` varchar(45) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `indicationCode` (`indicationCode`),
  UNIQUE KEY `indicationCode_2` (`indicationCode`,`indicationName`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblorganization`
--

DROP TABLE IF EXISTS `tblorganization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblorganization` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `organizationCode` int(11) NOT NULL AUTO_INCREMENT,
  `organization` varchar(45) NOT NULL,
  `adultAge` int(11) DEFAULT NULL,
  `maxPatients` int(11) DEFAULT NULL,
  `districtCode` int(11) NOT NULL,
  `gokSupport` tinyint(1) NOT NULL,
  `msfSupport` tinyint(1) NOT NULL,
  `pepfarSupport` tinyint(1) NOT NULL,
  `artServices` tinyint(1) NOT NULL,
  `pmtctServices` tinyint(1) NOT NULL,
  `pepServices` tinyint(1) NOT NULL,
  PRIMARY KEY (`organizationCode`),
  KEY `tblorganization_5b3f277e` (`districtCode`),
  CONSTRAINT `districtCode_refs_districtCode_ff5d6847` FOREIGN KEY (`districtCode`) REFERENCES `tbldistricts` (`districtCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblpatienttransaction`
--

DROP TABLE IF EXISTS `tblpatienttransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblpatienttransaction` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `transactionCode` int(11) NOT NULL AUTO_INCREMENT,
  `visit_id` int(11) NOT NULL,
  `drugId` int(11) NOT NULL,
  `arvQuantity` int(11) DEFAULT NULL,
  `dosage` varchar(20) NOT NULL,
  `duration` varchar(45) NOT NULL,
  `comment` longtext NOT NULL,
  `indicationCode` int(11) DEFAULT NULL,
  `operator` int(11) NOT NULL,
  `pillCount` int(11) DEFAULT NULL,
  `batchNo` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`transactionCode`),
  KEY `tblpatienttransaction_b377a78f` (`visit_id`),
  KEY `tblpatienttransaction_ca734bd5` (`drugId`),
  KEY `tblpatienttransaction_3ac0a762` (`dosage`),
  KEY `tblpatienttransaction_e7f12d3f` (`indicationCode`),
  KEY `tblpatienttransaction_5e7ba3ec` (`operator`),
  CONSTRAINT `drugId_refs_id_cec0cf06` FOREIGN KEY (`drugId`) REFERENCES `tblphysicaldrug` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `indicationCode_refs_id_99c3d889` FOREIGN KEY (`indicationCode`) REFERENCES `tblindication` (`id`),
  CONSTRAINT `operator_refs_id_686cbd85` FOREIGN KEY (`operator`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `visit_id` FOREIGN KEY (`visit_id`) REFERENCES `tblvisits` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblphysicaldrug`
--

DROP TABLE IF EXISTS `tblphysicaldrug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblphysicaldrug` (
  `arvDrug` varchar(50) NOT NULL,
  `drug_category` int(11) DEFAULT NULL,
  `packSize` varchar(45) DEFAULT NULL,
  `drugUnit` varchar(15) NOT NULL,
  `genericName` int(11) DEFAULT NULL,
  `maximumLevel` int(11) DEFAULT '0',
  `minimumLevel` int(11) DEFAULT '0',
  `reorderLEvel` int(11) DEFAULT '0',
  `std_dose` varchar(20) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `arvDrug` (`arvDrug`),
  KEY `tblphysicaldrug_91bc8256` (`drugUnit`),
  KEY `tblphysicaldrug_d0630caa` (`genericName`),
  CONSTRAINT `genericName_refs_id_679be628` FOREIGN KEY (`genericName`) REFERENCES `tblgenericname` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1407 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblregimechangereasons`
--

DROP TABLE IF EXISTS `tblregimechangereasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblregimechangereasons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reasonForChange` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblregimen`
--

DROP TABLE IF EXISTS `tblregimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblregimen` (
  `regimenCode` varchar(10) NOT NULL,
  `regimen` varchar(255) NOT NULL,
  `line` int(11) DEFAULT NULL,
  `remarks` varchar(255) NOT NULL,
  `show` tinyint(1) DEFAULT NULL,
  `regimenCategory` int(11) DEFAULT NULL,
  `type_of_service` int(11) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`regimenCode`),
  KEY `tblregimen_48fb58bb` (`status`),
  KEY `type_of_service_refs_id_idx` (`type_of_service`),
  KEY `regimencat_refs_idx` (`regimenCategory`),
  CONSTRAINT `regimencat_refs` FOREIGN KEY (`regimenCategory`) REFERENCES `tblregimencategory` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblregimencategory`
--

DROP TABLE IF EXISTS `tblregimencategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblregimencategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `categoryName` varchar(45) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblregimenhistory`
--

DROP TABLE IF EXISTS `tblregimenhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblregimenhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `artID` int(11) NOT NULL,
  `tblRegimenId` varchar(10) NOT NULL,
  `eventDate` datetime DEFAULT NULL,
  `reasonForChange` varchar(45) DEFAULT NULL,
  `regimen_change_type` varchar(20) NOT NULL DEFAULT 'Line Change',
  PRIMARY KEY (`id`),
  KEY `tblregimenhistory_68442644` (`artID`),
  KEY `tblregimenhistory_f16db438` (`tblRegimenId`),
  KEY `tblregimenhistory_6f92eb57` (`reasonForChange`),
  CONSTRAINT `artID_refs_id_da73ea16` FOREIGN KEY (`artID`) REFERENCES `tblartpatientmasterinformation` (`id`),
  CONSTRAINT `tblRegimen_refs` FOREIGN KEY (`tblRegimenId`) REFERENCES `tblregimen` (`regimenCode`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=46527 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblregion`
--

DROP TABLE IF EXISTS `tblregion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblregion` (
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `regionCode` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(45) NOT NULL,
  PRIMARY KEY (`regionCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblslot_size`
--

DROP TABLE IF EXISTS `tblslot_size`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblslot_size` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot_size` int(11) NOT NULL,
  `last_updated_on` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblstatus`
--

DROP TABLE IF EXISTS `tblstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `status` varchar(45) NOT NULL,
  `slug` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tblstatus_f52cfca0` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblstocktransactiontype`
--

DROP TABLE IF EXISTS `tblstocktransactiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblstocktransactiontype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(45) NOT NULL,
  `reportTitle` varchar(45) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbltypeofservice`
--

DROP TABLE IF EXISTS `tbltypeofservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbltypeofservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `typeOfService` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblvisits`
--

DROP TABLE IF EXISTS `tblvisits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblvisits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `eventDate` datetime DEFAULT NULL,
  `dateOfNextAppointment` datetime DEFAULT NULL,
  `visitType` int(11) NOT NULL DEFAULT '2',
  `ART_patient_id` int(11) NOT NULL,
  `days_to_TCA` int(10) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tblappointments_d2721039` (`visitType`),
  KEY `ART_patient_id_idx` (`ART_patient_id`),
  CONSTRAINT `ART_patient_id` FOREIGN KEY (`ART_patient_id`) REFERENCES `tblartpatientmasterinformation` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=23285 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblvisittype`
--

DROP TABLE IF EXISTS `tblvisittype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblvisittype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `visitType` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tblweightheightbsahistory`
--

DROP TABLE IF EXISTS `tblweightheightbsahistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblweightheightbsahistory` (
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `bsaCode` int(11) NOT NULL AUTO_INCREMENT,
  `eventDate` datetime DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `height` double DEFAULT NULL,
  `artID` int(11) NOT NULL,
  PRIMARY KEY (`bsaCode`),
  KEY `tblweightheightbsahistory_68442644` (`artID`),
  CONSTRAINT `artID_refs_id_83e23493` FOREIGN KEY (`artID`) REFERENCES `tblartpatientmasterinformation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46378 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `typeofcommodity`
--

DROP TABLE IF EXISTS `typeofcommodity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `typeofcommodity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `commodityName` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-01-09 12:40:39
