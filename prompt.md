## prompt 1: creacion de registros en la tabla users:
    - Quiero que actues como un experto en BBDD mysql, te voy a pasar un sentencia de creacion de tabla de bbdd mysql y necesito que me des 20 registros siguiendo este modelo de datos.
    - CREATE TABLE users (
        id int(11) NOT NULL AUTO_INCREMENT,   name varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,   surname varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,   age int(10) unsigned NOT NULL,   mail varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,   register_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,   status tinyint(4) NOT NULL DEFAULT '1',   password varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,   rol enum('admin','user') COLLATE utf8mb4_unicode_ci DEFAULT 'user', PRIMARY KEY (id), UNIQUE KEY mail_UNIQUE (mail) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

## prompt 2