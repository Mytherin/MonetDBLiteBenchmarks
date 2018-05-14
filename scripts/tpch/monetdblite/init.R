library(DBI)
library(MonetDBLite)
library(tpchr)

dbdir <- tempdir()
con <- dbConnect(MonetDBLite::MonetDBLite())

sf <- as.numeric(Sys.getenv('TPCHSF'))
tbls <- tpchr::dbgen(sf)
lapply(names(tbls), function(n) {dbWriteTable(con, n, tbls[[n]])})

run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
