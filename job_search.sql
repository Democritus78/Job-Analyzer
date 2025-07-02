pragma foreign_keys = on;

create table if not exists programming_language ( -- Skill
    id                  int primary key,
    my_project_id       int not null,
    name                text check (length(name) <= 255) not null,

    foreign key (my_project_id) references my_project(id)
) strict;

-- Framework, Software, or Library used.
create table if not exists framework ( -- Skill
    id                  int primary key,
    my_project_id       int not null,
    name                text check (length(name) <= 255) not null,

    foreign key (my_project_id) references my_project(id)
) strict;

create table if not exists tools ( -- Skill
    id                  int primary key,
    my_project_id       int not null,
    name                text check (length(name) <= 255) not null,

    foreign key (my_project_id) references my_project(id)
) strict;

create table if not exists databases ( -- Skill
    id                  int primary key,
    my_project_id       int not null,
    name                text check (length(name) <= 255) not null,

    foreign key (my_project_id) references my_project(id)
) strict;

create table if not exists cloud_service ( -- Skill
    id                  int primary key,
    my_project_id       int not null,
    name                text check (length(name) <= 255) not null,

    foreign key (my_project_id) references my_project(id)
) strict;

create table if not exists my_project (
    id                          int primary key,
    name                        text check (length(name) <= 255) not null,
    description                 text check (length(description) <= 255) not null,
    date_created                text default current_timestamp not null,
    date_completed              text default current_timestamp,
    status                      text not null
) strict;

create table if not exists job_offer (
    id                      int primary key,
    company                 text check (length(company) <= 255) not null,
    job_id                  int,
    position                text check (length(position) <= 255) not null,
    location                text check (length(location) <= 255) not null,
--    description             text check (length(description) <= 255) not null,
    salary                  text,    
    compensation_range      text check (length(compensation_range) <= 255),
    date_posted             text default current_timestamp,
    date_applied            text default current_timestamp not null,
    application_status      text not null,
    fit_score               int check (fit_score >= 0 and fit_score <= 100) default 0 not null
) strict;

create table if not exists job_description_bullet (
    id                      int primary key,
    job_offer_id            int not null,
    description_bullet      text check (length(bullet) <= 255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table if not exists job_responsibility (
    id                  int primary key,
    job_offer_id        int not null,
    responsibility      text check (length(responsibility) <= 255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table if not exists job_requirement (
    id                  int primary key,
    job_offer_id        int not null,
    type_t              text check (length(type_t) <= 255),
    requirement         text check (length(requirement) <= 255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;

create table if not exists job_benefit (
    id                  int primary key,
    job_offer_id        int not null,
    benefit             text check (length(benefit) <= 255) not null,

    foreign key (job_offer_id) references job_offer(id)
) strict;