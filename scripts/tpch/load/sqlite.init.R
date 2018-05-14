
library(RSQLite)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)
dbWriteTable(con, "lineitem", lineitem)