
initfile <- Sys.getenv('INITFILE')
timefile <- Sys.getenv('TIMEFILE')
nruns <- as.integer(Sys.getenv('NRUNS'))

if(!file.exists(timefile)){
	stop("Timing file not found")
}

if(file.exists(initfile)){
	source(initfile)
}

results <- numeric(nruns)
for(i in 1:nruns + 1) {
	if (i > 1) {
		results[i - 1] <- system.time(source(timefile))[3]
	}
}
print(results)
write.csv(results, 'tmp_r_results.csv', quote=FALSE, row.names=FALSE)
