library(DBI)
library(MonetDBLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('MONETDBLITE_DBDIR')
con <- dbConnect(MonetDBLite::MonetDBLite(), dbdir)

dbExecute(con, read_file('scripts/tpch/monetdb/schema.sql'))
dbExecute(con, read_file('scripts/tpch/monetdb/load.sql.tmp'))
dbExecute(con, read_file('scripts/tpch/monetdb/constraints.sql'))
dbExecute(con, read_file('scripts/tpch/monetdb/analyze.sql'))


run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
