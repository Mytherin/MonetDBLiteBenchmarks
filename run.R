
initfiles <- strsplit(Sys.getenv('INITFILE'), ",")[[1]]
timefiles <- strsplit(Sys.getenv('TIMEFILE'), ",")[[1]]
finalfiles <- strsplit(Sys.getenv('FINALFILE'), ",")[[1]]
nruns <- as.integer(Sys.getenv('NRUNS'))

for(j in 1:length(timefiles)) {
	timefile = timefiles[j]
	if(!file.exists(timefile)){
		stop("Timing file not found")
	}
}

for(j in 1:length(initfiles)) {
	initfile = initfiles[j]
	if(file.exists(initfile)){
		source(initfile)
	}
}

if (length(finalfiles) > 0) {
	if (length(finalfiles) != length(timefiles)) {
		stop("Timing files and final files should have the same length!")
	}
}

df <- data.frame(id=as.integer(1:nruns))
for(j in 1:length(timefiles)) {
	timefile = timefiles[j]
	results <- numeric(nruns)
	for(i in 1:nruns + 1) {
		if (i > 1) {
			results[i - 1] <- system.time(source(timefile))[3]
		} else {
			source(timefile)
			write.csv(df, 'start_experiments.csv', quote=FALSE, row.names = FALSE)
		}
		if (length(finalfiles) > 0) {
			source(finalfiles[j])
		}
	}
	df[timefile] <- results
}

write.csv(df, 'tmp_results.csv', quote=FALSE, row.names=FALSE)
