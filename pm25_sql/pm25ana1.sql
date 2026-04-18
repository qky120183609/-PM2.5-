truncate table tb_daily_stats;
insert into tb_daily_stats
(city_id, stat_date, avg_pm_cn1, avg_pm_cn2, avg_pm_cn3, avg_pm_us, avg_pm, max_pm, min_pm, aqi_level)
select
    city_id,
    datefromparts(year, month, day) as stat_date,
    avg(1.0 * pm_cn1) as avg_pm_cn1,
    avg(1.0 * pm_cn2) as avg_pm_cn2,
    avg(1.0 * pm_cn3) as avg_pm_cn3,
    avg(1.0 * pm_us) as avg_pm_us,
    --平均值（不用美国站）
    (
        isnull(avg(1.0 * pm_cn1), 0) + 
        isnull(avg(1.0 * pm_cn2), 0) + 
        isnull(avg(1.0 * pm_cn3), 0)
    ) / 
    (
        case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
        case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
        case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
    ) as avg_pm,
    -- 最大值
    (
        select max(v)
        from (values 
            (avg(1.0 * pm_cn1)), 
            (avg(1.0 * pm_cn2)), 
            (avg(1.0 * pm_cn3)), 
            (avg(1.0 * pm_us))
        ) as value(v)
    ) as max_pm,
    -- 最小值
    (
        select min(v)
        from (values 
            (avg(1.0 * pm_cn1)), 
            (avg(1.0 * pm_cn2)), 
            (avg(1.0 * pm_cn3)), 
            (avg(1.0 * pm_us))
        ) as value(v)
    ) as min_pm,
    -- aqi等级（官方方法：用所有国控站点的平均值，不用美国站）
    case
        when (
            isnull(avg(1.0 * pm_cn1), 0) + 
            isnull(avg(1.0 * pm_cn2), 0) + 
            isnull(avg(1.0 * pm_cn3), 0)
        ) / (
            case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
        ) <= 35 then 1
        when (
            isnull(avg(1.0 * pm_cn1), 0) + 
            isnull(avg(1.0 * pm_cn2), 0) + 
            isnull(avg(1.0 * pm_cn3), 0)
        ) / (
            case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
        ) <= 75 then 2
        when (
            isnull(avg(1.0 * pm_cn1), 0) + 
            isnull(avg(1.0 * pm_cn2), 0) + 
            isnull(avg(1.0 * pm_cn3), 0)
        ) / (
            case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
        ) <= 115 then 3
        when (
            isnull(avg(1.0 * pm_cn1), 0) + 
            isnull(avg(1.0 * pm_cn2), 0) + 
            isnull(avg(1.0 * pm_cn3), 0)
        ) / (
            case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
        ) <= 150 then 4
        when (
            isnull(avg(1.0 * pm_cn1), 0) + 
            isnull(avg(1.0 * pm_cn2), 0) + 
            isnull(avg(1.0 * pm_cn3), 0)
        ) / (
            case when avg(1.0 * pm_cn1) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn2) is not null then 1 else 0 end +
            case when avg(1.0 * pm_cn3) is not null then 1 else 0 end
        ) <= 250 then 5
        else 6
    end as aqi_level
from tb_pm25_raw
where pm_cn1 is not null or pm_cn2 is not null or pm_cn3 is not null
group by city_id, year, month, day;