
library(RSQLite)

dbdir <- Sys.getenv('SQLITE_DBDIR')
con <- dbConnect(RSQLite::SQLite(), dbdir)
