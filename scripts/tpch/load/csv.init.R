
library(data.table)

fn <- "test.csv"
if (file.exists(fn)) file.remove(fn)

fwrite(lineitem, fn)
