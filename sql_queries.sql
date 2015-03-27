SELECT fares.*, ca.amtrakcity as amtrakorig, cd.amtrakcity as amtrakdest FROM fares
INNER JOIN cities ca ON fares.orig = ca.bbcity
INNER JOIN cities cd ON fares.dest = cd.bbcity
order by id

select * from cities
order by bbcity

select * from fares