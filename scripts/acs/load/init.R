
library(survey)
library(convey)
library(lodown)

# MonetDB, MonetDBLite, SQLite, MySQL, PostgreSQL

dbtype <- Sys.getenv('ACS_DATABASE_TYPE')
port <- as.numeric(Sys.getenv('DBINFO_PORT'))
host <- Sys.getenv('DBINFO_HOST')
database <- Sys.getenv('DBINFO_DATABASE')
user <- Sys.getenv('DBINFO_USER')
password <- Sys.getenv('DBINFO_PASSWORD')
socket <- Sys.getenv('DBINFO_SOCKET')

if (dbtype == "SQLite") {
    con <- DBI::dbConnect(RSQLite::SQLite(), database)
} else if (dbtype == "MonetDBLite") {
    con <- DBI::dbConnect(MonetDBLite::MonetDBLite(), database)
} else if (dbtype == "MySQL") {
    con <- DBI::dbConnect(RMySQL::MySQL(), dbname=database, host=host, port=port, user=user, password=password, unix.socket=socket)
} else if (dbtype == "PostgreSQL") {
    con <- DBI::dbConnect(RPostgreSQL::PostgreSQL(), dbname=database, host=host, port=port, user=user, password=password)
} else if (dbtype == "MonetDB") {
    con <- DBI::dbConnect(MonetDBLite::MonetDB(), dbname=database, host=host, port=port, user=user, password=password)
}

assignInNamespace("dbConnect", function(drv, ...) 
{
    con
}, "DBI")

assignInNamespace("dbDisconnect", function(conn) 
{
    invisible(TRUE)
}, "DBI")

assignInNamespace("dbIsValid", function(conn) 
{
    TRUE
}, "DBI")

acs_df <- readRDS(file.path( path.expand( "~" ) , "ACS", "acs2016_1yr.rds"))


