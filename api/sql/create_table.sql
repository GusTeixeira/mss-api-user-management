CREATE SCHEMA auth;

CREATE TABLE auth.users(
    id serial primary key,
    nome varchar(100) not null,
    documento varchar(100) null,
    username varchar(100) unique not null,
    "password" varchar(255) not null,
    email varchar(255) not null,
    ativo boolean,
    created_at timestamp default now() null,
    updated_at timestamp,
    delete_at timestamp
);

CREATE TABLE auth.permissions(
    id serial primary key,
    nome varchar(100) not null,
    descricao varchar null,
    ativo boolean,
    created_at timestamp default now() null,
    updated_at timestamp
);

CREATE TABLE auth.groups(
    id serial primary key,
    nome varchar(100) not null,
    descricao varchar
    ativo boolean,
    created_at timestamp default now() null,
    updated_at timestamp
);

CREATE TABLE auth.users_permissions(
    id serial primary key,
    permission_id int,
    user_id int,
    created_at timestamp default now() null,
    updated_at timestamp,
    foreign key(permission_id) references auth.permissions(id),
    foreign key(user_id) references auth.users(id)
);

CREATE TABLE auth.group_permissions(
    id serial primary key,
    permission_id int,
    group_id int,
    created_at timestamp default now() null,
    updated_at timestamp,
    foreign key(permission_id) references auth.permissions(id),
    foreign key(group_id) references auth.groups(id)
);

CREATE TABLE auth.users_group(
    id serial primary key,
    user_id int,
    group_id int,
    created_at timestamp default now() null,
    updated_at timestamp,
    foreign key(user_id) references auth.users(id),
    foreign key(group_id) references auth.groups(id)
);