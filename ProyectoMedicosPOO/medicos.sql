
create database medicos;
use medicos;

CREATE TABLE `medicos` (
    `ID` INT,
    `RFC` VARCHAR(30) NOT NULL,
    `Nombre` VARCHAR(20) NOT NULL,
    `Apellido1` VARCHAR(20) NOT NULL,
    `Apellido2` VARCHAR(20) NOT NULL,
    `Cedula` VARCHAR(30) NOT NULL,
    `Correo` VARCHAR(50) NOT NULL,
    `password` VARCHAR(50) NOT NULL,
    `id_Rol` int  NOT NULL,
    PRIMARY KEY (`RFC`)
);

CREATE TABLE `pacientes` (
    `Id_paciente` INT AUTO_INCREMENT,
    `RFC_MED` VARCHAR(50) NOT NULL,
    `Nombre` VARCHAR(50) NOT NULL,
    `Apellido1` VARCHAR(50) NOT NULL,
    `Apellido2` VARCHAR(50) NOT NULL,
    `Fecha_nacimiento` date NOT NULL,
    `Enfermedades` VARCHAR(50),
    `Alergias` VARCHAR(50),
    `Antecedentes` VARCHAR(50),
    PRIMARY KEY (`Id_paciente`),
    FOREIGN KEY (`RFC_MED`) REFERENCES `medicos`(`RFC`)
);


CREATE TABLE `diagnostico` (
    `Id_exp` INT NOT NULL AUTO_INCREMENT,
    `Id_paciente` INT NOT NULL,
    `Medico_id` VARCHAR(50) NOT NULL,
    `Fecha` date NOT NULL,
    `Peso` VARCHAR(50) NOT NULL,
    `Estatura` VARCHAR(50) NOT NULL,
    `Temperatura` VARCHAR(50) NOT NULL,
    `Edad` VARCHAR(50) NOT NULL,
    `Observaciones` VARCHAR(500) NOT NULL,
    `Tratamiento` VARCHAR(500) NOT NULL,
    PRIMARY KEY (`Id_exp`),
    FOREIGN KEY (`Id_paciente`) REFERENCES `pacientes`(`Id_paciente`),
    FOREIGN KEY (`Medico_id`) REFERENCES `medicos`(`RFC`)
);


insert into `medicos` (`RFC`, `Nombre`, `Apellido1`, `Apellido2`, `Cedula`, `Correo`, `password`,`id_Rol`)
values ('FEFR031030NP4', 'Roman', 'Felipe', 'Ferrusquia', '121040623', 'ferrusquiaroman@gmail.com', '1234', '1');





select * from admin;
select * from registro_paciente;
select * from exploracion_diagnostico;