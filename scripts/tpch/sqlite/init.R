library(DBI)
library(RSQLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)

run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
