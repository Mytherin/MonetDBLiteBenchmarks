
library(DBI)
library(survey)
library(convey)
library(lodown)
library(RSQLite)
library(MonetDBLite)
library(RMySQL)
library(RPostgreSQL)

# MonetDB, MonetDBLite, SQLite, MySQL, PostgreSQL

dbdir <- Sys.getenv('ACS_DATABASE')
dbtype <- Sys.getenv('ACS_DATABASE_TYPE')

acs_df <- readRDS(file.path( path.expand( "~" ) , "ACS", "acs2016_1yr.rds"))
acs_design <-
    svrepdesign(
        weight = ~pwgtp ,
        repweights = 'pwgtp[0-9]+' ,
        scale = 4 / 80 ,
        rscales = rep( 1 , 80 ) ,
        mse = TRUE ,
        type = 'JK1' ,
        data = acs_df,
        dbtype = dbtype,
        dbname = dbdir
    )


#http://asdfree.com/american-community-survey-acs.html
