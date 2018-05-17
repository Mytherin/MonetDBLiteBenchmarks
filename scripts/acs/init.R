
library(DBI)
library(survey)
library(convey)
library(lodown)

acs_cat <- get_catalog("acs" ,	output_dir = file.path( path.expand( "~" ) , "ACS" ))

acs_cat <- subset(acs_cat, year == 2011 & time_period == '1-Year')
acs_cat <- lodown("acs" , acs_cat)

acs_design <- readRDS(file.path( path.expand( "~" ) , "ACS" , "acs2011_1yr.rds" ))
