
initfile <- Sys.getenv('INITFILE')
timefiles <- strsplit(Sys.getenv('TIMEFILE'), ",")[[1]]
nruns <- as.integer(Sys.getenv('NRUNS'))

for(j in 1:length(timefiles)) {
	timefile = timefiles[j]
	if(!file.exists(timefile)){
		stop("Timing file not found")
	}
}

if(file.exists(initfile)){
	source(initfile)
}


df <- data.frame(id=as.integer(1:nruns))
for(j in 1:length(timefiles)) {
	timefile = timefiles[j]
	results <- numeric(nruns)
	for(i in 1:nruns + 1) {
		if (i > 1) {
			results[i - 1] <- system.time(source(timefile))[3]
		}
	}
	df[timefile] <- results
}

print(df)
write.csv(df, 'tmp_r_results.csv', quote=FALSE, row.names=FALSE)
