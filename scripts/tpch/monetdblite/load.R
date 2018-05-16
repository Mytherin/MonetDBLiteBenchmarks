library(DBI)
library(MonetDBLite)
library(tpchr)
library(readr)

dbdir <- Sys.getenv('MONETDBLITE_DBDIR')
con <- dbConnect(MonetDBLite::MonetDBLite(), dbdir)

run_statement <- function(statement) {
	print(statement)
	dbExecute(con, statement)
}

run_file <- function(fname) {
	statements <- head(strsplit(read_file(fname), ';')[[1]], -1)
	print(statements)
	lapply(statements, run_statement)
}

run_file('scripts/tpch/monetdb/schema.sql')
run_file('scripts/tpch/monetdb/load.sql.tmp')
run_file('scripts/tpch/monetdb/constraints.sql')
run_file('scripts/tpch/monetdb/analyze.sql')
