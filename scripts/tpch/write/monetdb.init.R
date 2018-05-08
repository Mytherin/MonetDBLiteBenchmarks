
library(MonetDBLite)

port <- as.numeric(Sys.getenv('DBINFO_PORT'))
host <- Sys.getenv('DBINFO_HOST')
database <- Sys.getenv('DBINFO_DATABASE')
user <- Sys.getenv('DBINFO_USER')
password <- Sys.getenv('DBINFO_PASSWORD')

con <- dbConnect(MonetDBLite::MonetDB(), dbname=database, host=host, port=port, user=user, password=password)
