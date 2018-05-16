library(DBI)
library(RSQLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)

run_statement <- function(statement) {
  print(statement)
  dbExecute(con, statement)
}

run_file <- function(fname) {
  statements <- head(strsplit(read_file(fname), ';')[[1]], -1)
  print(statements)
  lapply(statements, run_statement)
}

run_file('scripts/tpch/sqlite/schema.sql')
run_file('scripts/tpch/sqlite/load.sql.tmp')
run_file('scripts/tpch/sqlite/constraints.sql')
run_file('scripts/tpch/sqlite/analyze.sql')


run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
