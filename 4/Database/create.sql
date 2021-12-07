drop database formula_1;
create database formula_1;

use formula_1;

create table drivers (
	d_id integer not null primary key,
	d_name varchar(30) not null,
	d_country varchar(30) not null,
	c_id integer
);

create table wdc (
	year char(4) not null primary key,
	d_id integer not null,
	foreign key(d_id) references drivers(d_id)
);

create table driver_stats (
	d_id integer not null primary key,
	d_starts integer,
	d_wins integer,
	d_poles integer,
	d_podiums integer,
	d_dnfs integer,
	d_wdcs integer,
	foreign key(d_id) references drivers(d_id)
);

create table constructors (
	c_id integer not null primary key,
	c_name varchar(30),
	engine_id integer,
	tp_eid integer
);

create table wcc (
	year char(4) not null primary key,
	c_id integer not null,
	foreign key(c_id) references constructors(c_id)
);

create table constructor_stats (
	c_id integer not null primary key,
	c_starts integer,
	c_poles integer,
	c_wins integer,
	c_1_2s integer,
	c_wccs integer,
	foreign key(c_id) references constructors(c_id)
);

create table engine_manufacturer (
	eng_id integer not null primary key,
	eng_name varchar(30)
);

create table sponsors (
	s_id integer not null primary key,
	s_name varchar(30)
);

create table sponsored_by (
	s_id integer not null,
	c_id integer not null,
	s_budget integer not null,
	primary key(s_id,c_id),
	foreign key(s_id) references sponsors(s_id),
	foreign key(c_id) references constructors(c_id)
);

create table employee (
	e_id integer not null primary key,
	e_name varchar(30) not null,
	e_age integer,
	e_address varchar(50),
	c_id integer not null,
	foreign key(c_id) references constructors(c_id)
);

create table dependents (
	dep_name varchar(30) not null,
	dep_age integer,
	emp_id integer not null,
	foreign key(emp_id) references employee(e_id),
	primary key(emp_id,dep_name)
);

alter table constructors add constraint engine_id_fkey foreign key(engine_id) references engine_manufacturer(eng_id);
alter table drivers add constraint c_id_fkey foreign key(c_id) references constructors(c_id);