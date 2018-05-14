
library(MonetDBLite)

dbdir <- Sys.getenv('MONETDBLITE_DBDIR')
con <- dbConnect(MonetDBLite::MonetDBLite(), dbdir)
dbWriteTable(con, "lineitem", lineitem)