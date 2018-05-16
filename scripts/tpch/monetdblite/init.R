library(DBI)
library(MonetDBLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('MONETDBLITE_DBDIR')
con <- dbConnect(MonetDBLite::MonetDBLite(), dbdir)

run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
