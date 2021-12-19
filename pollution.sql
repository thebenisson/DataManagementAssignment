-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pollution
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution` DEFAULT CHARACTER SET utf8mb4;
USE `pollution` ;

-- -----------------------------------------------------
-- Table `pollution`.`instrument_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution`.`instrument_types` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution`.`geo_points`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution`.`geo_points` (
  `id` INT NOT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution`.`stations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution`.`stations` (
  `SiteID` INT NOT NULL,
  `Location` VARCHAR(45) NOT NULL,
  `geo_point` INT NOT NULL,
  PRIMARY KEY (`SiteID`, `geo_point`),
  CONSTRAINT `geo_point`
    FOREIGN KEY (`geo_point`)
    REFERENCES `pollution`.`geo_points` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `geo+point_idx` ON `pollution`.`stations` (`geo_point` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `pollution`.`records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution`.`records` (
  `id` INT NOT NULL,
  `Date Time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NOx` FLOAT NULL,
  `NO2` FLOAT NULL,
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
  `date_start` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_end` TIMESTAMP NULL,
  `Current` VARCHAR(8) NOT NULL,
  `station` INT NOT NULL,
  `instrument_type` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `instrument_type`
    FOREIGN KEY (`instrument_type`)
    REFERENCES `pollution`.`instrument_types` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `station`
    FOREIGN KEY (`station`)
    REFERENCES `pollution`.`stations` (`SiteID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `station_idx` ON `pollution`.`records` (`station` ASC) VISIBLE;

CREATE INDEX `instrument_type_idx` ON `pollution`.`records` (`instrument_type` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
