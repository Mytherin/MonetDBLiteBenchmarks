library(DBI)
library(MonetDBLite)
library(tpchr)

dbdir <- Sys.getenv('MONETDBLITE_DBDIR')
con <- dbConnect(MonetDBLite::MonetDBLite(), dbdir)

sf <- as.numeric(Sys.getenv('TPCHSF'))
tbls <- tpchr::dbgen(sf)
lapply(names(tbls), function(n) {dbWriteTable(con, n, tbls[[n]])})

run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
