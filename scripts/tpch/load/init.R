
library(tpchr)
library(DBI)

sf <- as.numeric(Sys.getenv('TPCHSF'))
tbls <- tpchr::dbgen(sf)

lineitem <- tbls$lineitem

rm(tbls)