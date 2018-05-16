library(DBI)
library(RSQLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)

dbExecute(con, read_file('scripts/tpch/sqlite/schema.sql'))
dbExecute(con, read_file('scripts/tpch/sqlite/load.sql.tmp'))
dbExecute(con, read_file('scripts/tpch/sqlite/constraints.sql'))
dbExecute(con, read_file('scripts/tpch/sqlite/analyze.sql'))


run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
