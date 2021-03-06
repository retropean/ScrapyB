cd..
cd..
cd python27/scrapyB
echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime  ^| find "."') do set "dt=%%a"

set "YY=%dt:~2,2%"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "Min=%dt:~10,2%"
set "Sec=%dt:~12,2%"

set datestamp=%YYYY%%MM%%DD%
set timestamp=%HH%%Min%%Sec%
set fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%

ren "0.csv" "BB0day - %fullstamp%.csv"
ren "1.csv" "BB1day - %fullstamp%.csv"
ren "14.csv" "BB14day - %fullstamp%.csv"
ren "40.csv" "BB40day - %fullstamp%.csv"