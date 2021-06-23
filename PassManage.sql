-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pass_manage
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pass_manage
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pass_manage` DEFAULT CHARACTER SET utf8 ;
USE `pass_manage` ;

-- -----------------------------------------------------
-- Table `pass_manage`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pass_manage`.`user` (
  `user_id` TINYINT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pass_manage`.`passwords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pass_manage`.`passwords` (
  `pass_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` TINYINT NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `app_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`pass_id`, `user_id`),
  INDEX `fk_passwords_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_passwords_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `pass_manage`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
