

import os

R_INITFILE_PARAM = 'INITFILE'
R_TIMEFILE_PARAM = 'TIMEFILE'
R_NRUNS_PARAM = 'NRUNS'

R_RESULT_FILE = 'tmp_r_results.csv'

def run_script(init_script, bench_script, nruns, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.environ[R_INITFILE_PARAM] = init_script
	os.environ[R_TIMEFILE_PARAM] = bench_script
	os.environ[R_NRUNS_PARAM] = str(nruns)
	os.system('R -f time.R ${PIPE}'.replace('${PIPE}', pipe))
	del os.environ[R_INITFILE_PARAM]
	del os.environ[R_TIMEFILE_PARAM]
	del os.environ[R_NRUNS_PARAM]
	timings = []
	with open(R_RESULT_FILE, 'r') as f:
		for line in f:
			try:
				timings.append(float(line))
			except:
				pass
	os.remove(R_RESULT_FILE)
	if len(timings) != nruns:
		raise Exception("Something went wrong in the R script.")
	return timings
