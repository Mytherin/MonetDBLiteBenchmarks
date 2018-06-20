
fn <- "test.Rdata"
if (file.exists(fn)) file.remove(fn)
save(lineitem, file=fn, compress=F)
