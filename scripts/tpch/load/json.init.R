
library(jsonlite)

fn <- "test.json"
if (file.exists(fn)) file.remove(fn)

write_json(lineitem, fn)
