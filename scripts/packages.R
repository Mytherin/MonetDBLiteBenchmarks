
packages = c("dplyr", "data.table", "dbplyr", "devtools", "MonetDBLite", "RPostgreSQL", "RMySQL", "RSQLite", "readr")

r = getOption("repos") # hard code the cloud repo for CRAN
r["CRAN"] = "https://cloud.r-project.org"
options(repos = r)
rm(r)


install.packages(packages)
devtools::install_github("hannesmuehleisen/tpchr")