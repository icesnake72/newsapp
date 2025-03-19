-- 주석
-- 데이터베이스 생성
create database newsdb;

-- 데이터베이스 목록 조
show databases;

-- 데이터베이스 사용 명령
use newsdb;

-- table 삭제하기
drop table `sources`, `category`, `articles`;

-- table 목록 조회
show tables;

-- category table 만들기
create table `category`(
`id` bigint not null auto_increment,	-- not null(필),auto_increment(자동증가)
`name` varchar(30) not null,	-- 문자열(30자)
`memo` varchar(300),
`created_at` timestamp not null default current_timestamp,	-- 자동입력 , 현재 시간을 기본값으로 입력함
`updated_at` timestamp not null default current_timestamp,	-- 자동입력 , 현재 시간을 기본값으로 입력함
primary key(`id`)
);

-- category table에 데이터 입력하기
insert into `category`(`name`) values('business');
insert into `category`(`name`,`memo`) values('entertainment', '연예뉴스');

-- category table에 있는 데이터 조회 
select name, memo from `category`;
select * from `category`;


select id from sources where source_id='the-verge';



-- sources table 만들기
create table `sources`(
`id` bigint not null auto_increment,	-- not null(필),auto_increment(자동증가)
`source_id` varchar(20),
`name` varchar(30) not null,	-- 문자열(30자)
`description` varchar(1000),
`url` varchar(2000),
`category` varchar(30),
`language` varchar(10),
`country` varchar(10),
`created_at` timestamp not null default current_timestamp,	-- 자동입력 , 현재 시간을 기본값으로 입력함
`updated_at` timestamp not null default current_timestamp,	-- 자동입력 , 현재 시간을 기본값으로 입력함
primary key(`id`)
);

select * from sources;

--
ALTER TABLE `sources` MODIFY COLUMN `source_id` VARCHAR(50);



-- articles 테이블 생성
create table `articles`(
`id` bigint not null auto_increment,	-- not null(필),auto_increment(자동증가)
`author` varchar(100),
`title` varchar(1000),
`description` varchar(2000),
`url` varchar(2000),
`url_to_image` varchar(2000),
`published_at` varchar(100),
`content` varchar(2000),
`category` bigint not null,
`source` bigint not null,
primary key(`id`),
foreign key(`category`) references `category`(`id`),
foreign key(`source`) references `sources`(`id`));


select * from category;




