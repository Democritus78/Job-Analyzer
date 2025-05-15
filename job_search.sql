create database job_search;

use job_search;

create table programming_language (
    id                  int primary key,
    software_id         int not null,
    name                varchar(255) not null,

    foreign key (my_profile_id) references my_profile(id)
) strict;

create table software (
    id                  int primary key,
    my_profile_id       int not null,
    name                varchar(255) not null

    foreign key (my_profile_id) references my_profile(id)
) strict;

create table my_project (
    id                          int primary key,
    programming_language_id     int not null,
    name                        varchar(255) not null,
    description                 varchar(255) not null,
    date_created                current_timestamp not null,
    date_completed              current_timestamp,
    status                      varchar(255) not null,

    foreign key (programming_language_id) references programming_language(id)
) strict;

create table job_offer (
    id                      int primary key,
    company                 varchar(255) not null,
    job_id                  int,
    position                varchar(255) not null,
    location                varchar(255) not null,
    description             varchar(255) not null,
    salary                  decimal(10, 2),    
    compensation_range      varchar(255),
    date_posted             current_timestamp,
    date_applied            current_timestamp not null,
    application_status      varchar(1) not null,
) strict;

create table job_responsibility (
    id                  int primary key,
    job_offer_id        int not null,
    responsibility      varchar(255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table job_requirement (
    id                  int primary key,
    job_offer_id        int not null,
    type_t              varchar(255),
    requirement         varchar(255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table job_benefit (
    id                  int primary key,
    job_offer_id        int not null,
    benefit             varchar(255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table job_programming_language (
    id                  int primary key,
    job_offer_id        int not null,
    language            varchar(255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table job_software (
    id                  int primary key,
    job_offer_id        int not null,
    name                varchar(255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;