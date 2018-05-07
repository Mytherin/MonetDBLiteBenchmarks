
library(RPostgreSQL)

port <- as.numeric(Sys.getenv('DBINFO_PORT'))
host <- Sys.getenv('DBINFO_HOST')
database <- Sys.getenv('DBINFO_DATABASE')
user <- Sys.getenv('DBINFO_USER')
password <- Sys.getenv('DBINFO_PASSWORD')

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname=database, host=host, port=port, user=user, password=password)
dbWriteTable(con, "lineitem", lineitem)