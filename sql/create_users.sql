create table users (id int(6) UNSIGNED AUTO_INCREMENT primary key, 
    fullName varchar(30),
    email varchar(30),
    password varchar(40),
    avatar varchar(50),
    isActive boolean,
    role_id int(6));