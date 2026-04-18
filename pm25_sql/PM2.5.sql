-- 1. 删除旧表（如有）
drop table if exists tb_daily_stats;
drop table if exists tb_pm25_raw;
drop table if exists tb_cities;

-- 2. 创建数据库（如有）
if not exists (select * from sys.databases where name = 'pm25_analysis')
create database pm25_analysis;
go

use pm25_analysis;
go

-- 3. 城市表（不变）
create table tb_cities(
    city_id int primary key identity(1,1),
    city_name varchar(20) not null unique,
    city_code varchar(10) not null,
    data_start_date date not null,
    data_end_date date not null
);
go

-- 4. 核心：pm25原始数据表（适配所有城市）
-- 设计思路：用「通用pm列+城市专属标识」，避免空字段浪费
create table tb_pm25_raw(
    record_id int primary key identity(1,1),
    city_id int not null foreign key references tb_cities(city_id),
    year int not null,
    month int not null,
    day int not null,
    hour int not null,
    season int not null,
    -- 通用pm列：存当前城市有的监测点数据（空=无该监测点）
    pm_cn1 int,           -- 城市专属监测点1（如北京=dongsi，上海=jingan）
    pm_cn2 int,           -- 城市专属监测点2（如北京=dongsihuan，上海=xuhui）
    pm_cn3 int,           -- 城市专属监测点3（仅北京有=nongzhanguan）
    pm_us int,            -- 美国使馆（所有城市都有）
    -- 气象列（所有城市完全一致）
    dewp int,             -- 露点温度
    humi float,           -- 湿度
    pressure int,         -- 气压
    temp int,             -- 温度
    cbwd char(2),         -- 风向
    iws float,            -- 风速
    precipitation float,  -- 降水量
    iprec float           -- 降水标识
);
go

-- 5. 日报表（不变，后续可通过sql计算填充）
create table tb_daily_stats(
    stat_id int primary key identity(1,1),
    city_id int not null foreign key references tb_cities(city_id),
    stat_date date not null,
    avg_pm_cn1 float,     -- 对应pm_cn1的日均值
    avg_pm_cn2 float,     -- 对应pm_cn2的日均值
    avg_pm_cn3 float,     -- 对应pm_cn3的日均值
    avg_pm_us float,      -- 美国使馆日均值
    avg_pm float,         -- 当日所有pm均值  
    max_pm float,         -- 当日所有pm最大值
    min_pm float,         -- 当日所有pm最小值
    aqi_level int not null,-- aqi等级（后续计算）
    unique(city_id,stat_date) -- 避免重复日期
);
go

-- 6. 插入城市数据（与你的CSV完全对应）
insert into tb_cities(city_name,city_code,data_start_date,data_end_date)
values
('北京','BJ','2010-01-01','2015-12-31'),
('上海','SH','2010-01-01','2015-12-31'),
('成都','CD','2010-01-01','2015-12-31'),
('广州','GZ','2010-01-01','2015-12-31'),
('沈阳','SY','2010-01-01','2015-12-31');
go