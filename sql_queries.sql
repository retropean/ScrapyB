SELECT fares.*, ca.amtrakcity as amtrakorig, cd.amtrakcity as amtrakdest FROM fares
INNER JOIN cities ca ON fares.orig = ca.bbcity
INNER JOIN cities cd ON fares.dest = cd.bbcity
order by id

select * from cities
order by bbcity

select * from fares

/*additions*/
where datescraped = '12/15/2016'
limit 10

/*Check number of rows per datescraped and date in database*/
select datescraped, date, count(fare) from fares
group by datescraped, date
order by datescraped, date

/*Check number of rows per datescraped in database*/
select datescraped, count(fare) from fares
group by datescraped
order by datescraped

/*Check number of rows in database*/
select count(*) from fares