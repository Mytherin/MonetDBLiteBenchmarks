
packages = c("dplyr", "data.table", "dbplyr", "MonetDBLite", "RPostgreSQL", "RMySQL", "RSQLite", "readr", "convey", "srvyr", "feather", "jsonlite")

r = getOption("repos") # hard code the cloud repo for CRAN
r["CRAN"] = "https://cloud.r-project.org"
options(repos = r)
rm(r)

install.packages("devtools")
devtools::install_github("ajdamico/lodown", dependencies = TRUE)
install.packages(packages)
devtools::install_github("hannesmuehleisen/tpchr")

source("http://bioconductor.org/biocLite.R")
biocLite("rhdf5")

