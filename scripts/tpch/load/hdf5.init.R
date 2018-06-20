
library(rhdf5)

fn <- "test.hdf5"
if (file.exists(fn)) file.remove(fn)

h5createFile(fn)
h5write(lineitem, fn, "df")
