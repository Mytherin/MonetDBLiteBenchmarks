
library(DBI)
library(survey)
library(convey)
library(lodown)

acs_cat <-
    get_catalog( "acs" ,
        output_dir = file.path( path.expand( "~" ) , "ACS" ) )


# 2016 alabama single-year only. remove ` & stateab == 'al'` for a nationwide table
acs_cat <- subset( acs_cat , year == 2016 & time_period == '1-Year' & stateab %in% c('al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il') )
# download the microdata to your local computer
acs_cat <- lodown( "acs" , acs_cat )
