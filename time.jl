

initfile = ENV["INITFILE"]
timefiles = split(ENV["TIMEFILE"], ",")
nruns = parse(Int64, ENV["NRUNS"])

for i = 1:length(timefiles)
	timefile = timefiles[i]
	if !isfile(timefile)
		print("File not found\n")
		quit()
	end
end

if isfile(initfile)
	include(initfile)
end

df = Dict()
for i = 1:length(timefiles)
	timefile = timefiles[i]
	results = Array(Float64, nruns)
	for j in 1:nruns + 1
		tic()
		include(timefile)
		res = toc() 
		if j > 1
			results[j - 1] = res
		end
	end
	df[timefile] = results
end

open("tmp_jl_results.csv", "w+") do f
	for i = 1:length(timefiles)
		write(f, timefiles[i])
		if i < length(timefiles)
			write(f, ",")
		end
	end
	write(f, "\n")
	for j = 1:nruns
		for i = 1:length(timefiles)
			write(f, string(df[timefiles[i]][j]))
			if i < length(timefiles)
				write(f, ",")
			end
		end
		write(f, "\n")
	end

end
