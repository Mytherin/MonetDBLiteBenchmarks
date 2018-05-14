library(DBI)
library(RSQLite)
library(tpchr)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)

sf <- as.numeric(Sys.getenv('TPCHSF'))
tbls <- tpchr::dbgen(sf)
lapply(names(tbls), function(n) {dbWriteTable(con, n, tbls[[n]])})

run_query <- function(i) {
  dbGetQuery(con, tpchr:::get_query(i))
}
