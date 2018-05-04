

import os

def generate_tpch(SILENT=True, sf=1):
	CURRENTDIR = os.getcwd()
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	tpchdir = os.path.join(CURRENTDIR, 'tpch-${SF}'.replace('${SF}', str(sf)))
	if os.path.exists(tpchdir):
		return tpchdir
	if not os.path.exists('tpch-dbgen'):
		print("[TPCH] Downloading and building project")
		os.system('git clone https://github.com/eyalroz/tpch-dbgen ${PIPE}'.replace("${PIPE}", pipe))
		os.chdir('tpch-dbgen')
		os.system('cmake -G "Unix Makefiles" . ${PIPE}'.replace("${PIPE}", pipe))
		os.system('make ${PIPE}'.replace("${PIPE}", pipe))
	else:
		os.chdir('tpch-dbgen')
	print("[TPCH] Generating data of SF${SF}".replace('${SF}', str(sf)))
	os.system('./dbgen -s ${SF} ${PIPE}'.replace("${SF}", str(sf)).replace("${PIPE}", pipe))
	print("[TPCH] Perform post-processing")
	# remove trailing |
	for f in os.listdir('.'):
		if len(f) < 4 or f[-4:] != '.tbl': continue
		os.system('rm -f ${FILE}.tmp'.replace("${FILE}", f))
		os.system("sed 's/.$//' ${FILE} > ${FILE}.tmp".replace("${FILE}", f))
		os.system('mv ${FILE}.tmp ${FILE}'.replace("${FILE}", f))
	os.system('rm -rf ../${TPCHDIR}'.replace('${TPCHDIR}', tpchdir))
	os.system('mkdir -p ../${TPCHDIR}'.replace('${TPCHDIR}', tpchdir))
	os.system('mv *.tbl ../${TPCHDIR}'.replace('${TPCHDIR}', tpchdir))
	os.chdir(CURRENTDIR)
	return tpchdir

