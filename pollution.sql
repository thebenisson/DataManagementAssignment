-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema pollution
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `pollution` ;

-- -----------------------------------------------------
-- Schema pollution
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution` DEFAULT CHARACTER SET utf8mb4 ;
USE `pollution` ;

-- -----------------------------------------------------
-- Table `pollution`.`instruments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution`.`instruments` ;

CREATE TABLE IF NOT EXISTS `pollution`.`instruments` (
  `Instrument Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Instrument Type`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `Instrument_Type_UNIQUE` ON `pollution`.`instruments` (`Instrument Type` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `pollution`.`stations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution`.`stations` ;

CREATE TABLE IF NOT EXISTS `pollution`.`stations` (
  `SiteID` INT NOT NULL,
  `Location` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`SiteID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution`.`records`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution`.`records` ;

CREATE TABLE IF NOT EXISTS `pollution`.`records` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Date Time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NOx` FLOAT NULL,
  `NO2` FLOAT NULL,
  `NO` FLOAT NULL,
  `PM10` FLOAT NULL,
  `NVPM10` FLOAT NULL,
  `VPM10` FLOAT NULL,
  `NVPM2.5` FLOAT NULL,
  `PM2.5` FLOAT NULL,
  `VPM2.5` FLOAT NULL,
  `CO` FLOAT NULL,
  `O3` FLOAT NULL,
  `SO2` FLOAT NULL,
  `Temperature` FLOAT NULL,
  `RH` FLOAT NULL,
  `Air Pressure` FLOAT NULL,
  `DateStart` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `DateEnd` DATETIME NULL,
  `Current` TINYINT NOT NULL,
  `SiteID` INT NOT NULL,
  `Instrument Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `instrument_type`
    FOREIGN KEY (`Instrument Type`)
    REFERENCES `pollution`.`instruments` (`Instrument Type`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `station`
    FOREIGN KEY (`SiteID`)
    REFERENCES `pollution`.`stations` (`SiteID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `station_idx` ON `pollution`.`records` (`SiteID` ASC) VISIBLE;

CREATE INDEX `instrument_idx` ON `pollution`.`records` (`Instrument Type` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `pollution`.`geopoints`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution`.`geopoints` ;

CREATE TABLE IF NOT EXISTS `pollution`.`geopoints` (
  `siteid` INT NOT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  PRIMARY KEY (`siteid`),
  CONSTRAINT `siteid`
    FOREIGN KEY (`siteid`)
    REFERENCES `pollution`.`stations` (`SiteID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
