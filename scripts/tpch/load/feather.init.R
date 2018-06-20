
library(feather)

fn <- "test.bin"
if (file.exists(fn)) file.remove(fn)

write_feather(lineitem, fn)
