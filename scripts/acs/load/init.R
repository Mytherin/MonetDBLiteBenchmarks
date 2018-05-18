
library(DBI)
library(survey)
library(convey)
library(lodown)
library(RSQLite)
library(MonetDBLite)
library(RMySQL)
library(RPostgreSQL)

# MonetDB, MonetDBLite, SQLite, MySQL, PostgreSQL

dbtype <- Sys.getenv('ACS_DATABASE_TYPE')
port <- as.numeric(Sys.getenv('DBINFO_PORT'))
host <- Sys.getenv('DBINFO_HOST')
database <- Sys.getenv('DBINFO_DATABASE')
user <- Sys.getenv('DBINFO_USER')
password <- Sys.getenv('DBINFO_PASSWORD')
socket <- Sys.getenv('DBINFO_SOCKET')

if (dbtype == "SQLite") {
    con <- dbConnect(RSQLite::SQLite(), database)
} else if (dbtype == "MonetDBLite") {
    con <- dbConnect(MonetDBLite::MonetDBLite(), database)
} else if (dbtype == "MySQL") {
    con <- dbConnect(RMySQL::MySQL(), dbname=database, host=host, port=port, user=user, password=password, unix.socket=socket)
} else if (dbtype == "PostgreSQL") {
    drv <- dbDriver("PostgreSQL")
    con <- dbConnect(drv, dbname=database, host=host, port=port, user=user, password=password)
    
    assignInNamespace("checkConnection", function (dbconnection, error = TRUE) 
    {
        if (is(dbconnection, "DBIConnection") && !is(con, "PostgreSQLConnection")) {
            if (!DBI::dbIsValid(dbconnection)) 
                if (error) 
                    stop("Database connection is closed")
                else return(FALSE)
        }
        else {
        }
        invisible(TRUE)
    }, "survey")
} else if (dbtype == "MonetDB") {
    con <- dbConnect(MonetDBLite::MonetDB(), dbname=database, host=host, port=port, user=user, password=password)
}

acs_df <- readRDS(file.path( path.expand( "~" ) , "ACS", "acs2016_1yr.rds"))


