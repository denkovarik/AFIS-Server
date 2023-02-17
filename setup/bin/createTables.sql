-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema db_afis_f20
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_afis_f20
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_afis_f20` DEFAULT CHARACTER SET latin1 ;
USE `db_afis_f20` ;

-- -----------------------------------------------------
-- Table `db_afis_f20`.`Subjects`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_afis_f20`.`Subjects` ;

CREATE TABLE IF NOT EXISTS `db_afis_f20`.`Subjects` (
  `subjectID` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`subjectID`),
  UNIQUE INDEX `subjectID_UNIQUE` (`subjectID` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `db_afis_f20`.`Fingers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_afis_f20`.`Fingers` ;

CREATE TABLE IF NOT EXISTS `db_afis_f20`.`Fingers` (
  `handID` VARCHAR(1) NULL DEFAULT NULL COMMENT 'R = right hand\\nL = left hand\\nNULL = unknown',
  `fingerIndex` INT(10) NULL DEFAULT NULL COMMENT 'ASSUMED AT THIS POINT\\n0 = thumb\\n1 = index\\n2 = middle\\n3 = ring\\n4 = pinky\\nNULL = unknown\\n',
  `fingerID` VARCHAR(45) NOT NULL COMMENT 'Form of:\\nsubjectID.fingerID',
  `subjectID` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Form of:\\nsubjectID',
  PRIMARY KEY (`fingerID`),
  UNIQUE INDEX `fingerID_UNIQUE` (`fingerID` ASC) ,
  INDEX `subjectID_idx` (`subjectID` ASC),
  CONSTRAINT `subjectID`
    FOREIGN KEY (`subjectID`)
    REFERENCES `db_afis_f20`.`Subjects` (`subjectID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `db_afis_f20`.`Images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_afis_f20`.`Images` ;

CREATE TABLE IF NOT EXISTS `db_afis_f20`.`Images` (
  `image_filepath` VARCHAR(100) NULL DEFAULT NULL,
  `imageID` VARCHAR(45) NOT NULL COMMENT 'Form of:\\\\nsubjectID.fingerID.imageID',
  `fingerID` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Form of:\\nsubjectID.fingerID',
  `width` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'width of the image in pixels',
  `height` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'height of the image in pixels',
  `resolution` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'the resulution of the image in dpi',
  PRIMARY KEY (`imageID`),
  INDEX `fingerID_idx` (`fingerID` ASC) ,
  CONSTRAINT `fingerID`
    FOREIGN KEY (`fingerID`)
    REFERENCES `db_afis_f20`.`Fingers` (`fingerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `db_afis_f20`.`Features`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_afis_f20`.`Features` ;

CREATE TABLE IF NOT EXISTS `db_afis_f20`.`Features` (
  `imageID` VARCHAR(45) NULL DEFAULT NULL,
  `featureID` VARCHAR(45) NOT NULL,
  `minutiaesCount` INT(10) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`featureID`),
  INDEX `imageID_idx` (`imageID` ASC) ,
  CONSTRAINT `imageID`
    FOREIGN KEY (`imageID`)
    REFERENCES `db_afis_f20`.`Images` (`imageID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `db_afis_f20`.`Minutiaes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_afis_f20`.`Minutiaes` ;

CREATE TABLE IF NOT EXISTS `db_afis_f20`.`Minutiaes` (
  `minutiaeID` VARCHAR(45) NOT NULL COMMENT 'Form of:\\nsubjectID.fingerID.imageID.featureID.minutiaeID',
  `featureID` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Form of:\\nsubjectID.fingerID.imageID.featureID',
  `xyt_file` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`minutiaeID`),
  INDEX `featureID_idx` (`featureID` ASC) ,
  CONSTRAINT `featureID`
    FOREIGN KEY (`featureID`)
    REFERENCES `db_afis_f20`.`Features` (`featureID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
