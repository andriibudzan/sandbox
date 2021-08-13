# ETL pipeline build with pandas

Processing a large file with pandas

### explore data:

1. read and explore tz_opendata_ua/tz_opendata_z01012021_po01072021.csv data

1. perform some tranformations and mapping if needed

1. split into smaller tables according to [diagram]

1. map aggregated tables with smaller tables

1. currently: save prepared files locally \
plans: write data to DB without local dump

----
### prepare postgresql:

1. create tables according to [diagram]

1. upload prepared data to database


----
[diagram]: https://dbdiagram.io/d/60ecb9434ed9be1c05c96be8
