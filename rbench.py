

import os

R_INITFILE_PARAM = 'INITFILE'
R_TIMEFILE_PARAM = 'TIMEFILE'
R_NRUNS_PARAM = 'NRUNS'

R_RESULT_FILE = 'tmp_r_results.csv'

def init(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.system('R -f scripts/rpackages.R ${PIPE}'.replace('${PIPE}', pipe))

def run_script(init_script, bench_scripts, nruns, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.environ[R_INITFILE_PARAM] = init_script
	os.environ[R_TIMEFILE_PARAM] = ','.join(bench_scripts)
	os.environ[R_NRUNS_PARAM] = str(nruns)
	os.system('R -f time.R ${PIPE}'.replace('${PIPE}', pipe))
	del os.environ[R_INITFILE_PARAM]
	del os.environ[R_TIMEFILE_PARAM]
	del os.environ[R_NRUNS_PARAM]
	timings = {}
	indices = []
	for entry in bench_scripts:
		timings[entry] = []
	header = True
	with open(R_RESULT_FILE, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			entries = line.split(',')
			if header:
				indices = entries
				header = False
			else:
				index = 0
				for entry in entries:
					if indices[index] != 'id':
						timings[indices[index]].append(float(entry))
					index += 1
	os.remove(R_RESULT_FILE)
	for entry in bench_scripts:
		if len(timings[entry]) != nruns:
			raise Exception("Something went wrong in the R script.")
	return timings
