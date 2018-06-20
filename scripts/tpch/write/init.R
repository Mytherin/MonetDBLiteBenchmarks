
sf <- as.numeric(Sys.getenv('TPCHSF'))

library(tpchr)
library(DBI)

tbls <- tpchr::dbgen(sf)

lineitem <- tbls$lineitem

rm(tbls)
