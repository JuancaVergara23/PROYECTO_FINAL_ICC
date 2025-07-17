-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE DATABASE IF NOT EXISTS `db_agro` DEFAULT CHARACTER SET utf8 ;
USE `db_agro` ;

-- -----------------------------------------------------
-- Table `mydb`.`Tipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Tipo` (
  `idTipo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`idTipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Usuarios` (
  `idUsuarios` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `correo` VARCHAR(45) NULL,
  `contrasena` VARCHAR(45) NULL,
  `Tipo_idTipo` INT NOT NULL,
  PRIMARY KEY (`idUsuarios`),
    FOREIGN KEY (`Tipo_idTipo`)
    REFERENCES `db_agro`.`Tipo` (`idTipo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Clientes` (
  `idClientes` INT NOT NULL AUTO_INCREMENT,
  `n_dataloggers` INT NULL,
  `Usuarios_idUsuarios` INT NOT NULL,
  PRIMARY KEY (`idClientes`),
    FOREIGN KEY (`Usuarios_idUsuarios`)
    REFERENCES `db_agro`.`Usuarios` (`idUsuarios`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Datalogger`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Datalogger` (
  `idDatalogger` INT NOT NULL AUTO_INCREMENT,
  `ubicacion` VARCHAR(45) NULL,
  `nivel_bateria` FLOAT NULL,
  `Clientes_idClientes` INT NOT NULL,
  PRIMARY KEY (`idDatalogger`, `Clientes_idClientes`),
    FOREIGN KEY (`Clientes_idClientes`)
    REFERENCES `db_agro`.`Clientes` (`idClientes`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Sensores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Sensores` (
  `idSensores` INT NOT NULL AUTO_INCREMENT,
  `tipo` INT NULL,
  `lugar` VARCHAR(45) NULL,
  `Datalogger_idDatalogger` INT NOT NULL,
  PRIMARY KEY (`idSensores`, `Datalogger_idDatalogger`),
    FOREIGN KEY (`Datalogger_idDatalogger`)
    REFERENCES `db_agro`.`Datalogger` (`idDatalogger`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Mediciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_agro`.`Mediciones` (
  `idMediciones` INT NOT NULL AUTO_INCREMENT,
  `humedad` FLOAT NULL,
  `ce` FLOAT NULL,
  `temperatura` FLOAT NULL,
  `n` FLOAT NULL,
  `k` FLOAT NULL,
  `p` FLOAT NULL,
  `fechatiempo` DATETIME NULL,
  `Sensores_idSensores` INT NOT NULL,
  `Sensores_Datalogger_idDatalogger` INT NOT NULL,
  PRIMARY KEY (`idMediciones`, `Sensores_idSensores`, `Sensores_Datalogger_idDatalogger`),
    FOREIGN KEY (`Sensores_idSensores` , `Sensores_Datalogger_idDatalogger`)
    REFERENCES `db_agro`.`Sensores` (`idSensores` , `Datalogger_idDatalogger`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Creando los tipos 
-- -----------------------------------------------------

insert into tipo(nombre) values('admin');
insert into tipo(nombre) values('cliente');

-- -----------------------------------------------------
-- Creando los admins
-- -----------------------------------------------------

insert into usuarios(nombre,correo,contrasena,Tipo_idTipo) values('Juan Vergara','jvergara@gmail.com','ju@nv',1);
insert into usuarios(nombre,correo,contrasena,Tipo_idTipo) values('Piero Pittman','ppittman@gmail.com','pi3rop',1);
