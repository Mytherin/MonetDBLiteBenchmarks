
library(MonetDBLite)

dbdir <- tempdir()
con <- dbConnect(MonetDBLite::MonetDBLite())
dbWriteTable(con, "lineitem", lineitem)