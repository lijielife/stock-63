-- 3ヶ月以内
create view stock_view as
select * from stock
where day > date(date('now'), '-30 days');

--現在の終値
create view stock_current as
select code, day, closing from stock_view
group by code
having day = max(day)
;

--(年初来)安値
create view stock_min as
select a.code, min(a.day) as day, a.closing
from stock_view a,
(select code, min(closing) as closingmin from stock_view group by code) mi
where a.code = mi.code
and a.closing = mi.closingmin
group by a.code, a.closing;

--(年初来)高値
create view stock_max as
select a.code, max(a.day) as day, a.closing
from stock_view a,
(select code, max(closing) as closingmax from stock_view group by code) mx
where a.code = mx.code
and a.closing = mx.closingmax
group by a.code, a.closing;
            
--上昇銘柄上昇率
create view rise_rate as
select mx.code as code, 
mx.day as mxday, mx.closing as mxclosing, 
mi.day as miday, mi.closing as miclosing,
(cast((mx.closing - mi.closing) as REAL) / mi.closing) as rate
from stock_min mi, stock_max mx
where (mi.code = mx.code)
and mi.day < mx.day
;

--下落銘柄下落率
create view fall_rate as
select mx.code as code, 
mx.day as mxday, mx.closing as mxclosing, 
mi.day as miday, mi.closing as miclosing,
(cast((mx.closing - mi.closing) as REAL) / mi.closing) as rate
from stock_min mi, stock_max mx
where (mi.code = mx.code)
and mi.day > mx.day
;


