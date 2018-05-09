
library(RMySQL)

port <- as.numeric(Sys.getenv('DBINFO_PORT'))
host <- Sys.getenv('DBINFO_HOST')
database <- Sys.getenv('DBINFO_DATABASE')
user <- Sys.getenv('DBINFO_USER')
password <- Sys.getenv('DBINFO_PASSWORD')
socket <- Sys.getenv('DBINFO_SOCKET')

con <- dbConnect(MySQL(), dbname=database, host=host, port=port, user=user, password=password, unix.socket=socket)
dbWriteTable(con, "lineitem", lineitem)