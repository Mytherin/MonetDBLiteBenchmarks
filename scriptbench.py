

import os

INITFILE_PARAM = 'INITFILE'
TIMEFILE_PARAM = 'TIMEFILE'
NRUNS_PARAM = 'NRUNS'

RESULT_FILE = 'tmp_results.csv'

R = 1
Julia = 2
Python = 3

def init(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	print("[SCRIPT] Initializing R packages")
	os.system('R -f scripts/packages.R ${PIPE}'.replace('${PIPE}', pipe))
	print("[SCRIPT] Initializing Julia packages")
	os.system('julia scripts/packages.jl ${PIPE}'.replace('${PIPE}', pipe))

def run_script(lang, init_script, bench_scripts, nruns, SILENT=True):
	pipe = ">/dev/null" if SILENT else ""
	os.environ[INITFILE_PARAM] = init_script
	os.environ[TIMEFILE_PARAM] = ','.join(bench_scripts)
	os.environ[NRUNS_PARAM] = str(nruns)
	print("[SCRIPT] Running program")
	if lang == Julia:
		os.system('julia run.jl ${PIPE}'.replace('${PIPE}', pipe))
	elif lang == R:
		os.system('R -f run.R ${PIPE}'.replace('${PIPE}', pipe))
	elif lang == Python:
		os.system('python run.py ${PIPE}'.replace('${PIPE}', pipe))
	else:
		raise Exception("Unrecognized language \"%s\"" % (str(lang)))
	del os.environ[INITFILE_PARAM]
	del os.environ[TIMEFILE_PARAM]
	del os.environ[NRUNS_PARAM]
	timings = {}
	indices = []
	for entry in bench_scripts:
		timings[entry] = []
	header = True
	with open(RESULT_FILE, 'r') as f:
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
	os.remove(RESULT_FILE)
	for entry in bench_scripts:
		if len(timings[entry]) != nruns:
			raise Exception("Something went wrong in the script.")
	return timings
