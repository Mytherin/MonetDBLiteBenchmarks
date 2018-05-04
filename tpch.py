

def generate_tpch(sf=1):
	CURRENTDIR = os.getcwd()
	if not os.path.exists('tpch-dbgen'):
		os.system('git clone https://github.com/eyalroz/tpch-dbgen')
		os.chdir('tpch-dbgen')
		os.system('cmake -G "Unix Makefiles" .')
		os.system('make')
	else:
		os.chdir('tpch-dbgen')
	os.system('./dbgen -s ${SF}'.replace("${SF}", str(sf)))
	# remove trailing |
	for f in os.listdir('.'):
		if len(f) < 4 or f[-4:] != '.tbl': continue
		os.system('rm -f ${FILE}.tmp'.replace("${FILE}", f))
		os.system("sed 's/.$//' ${FILE} > ${FILE}.tmp".replace("${FILE}", f))
		os.system('mv ${FILE}.tmp ${FILE}'.replace("${FILE}", f))
	os.system('rm -rf ../tpch-${SF}'.replace('${SF}', str(sf)))
	os.system('mkdir -p ../tpch-${SF}'.replace('${SF}', str(sf)))
	os.system('mv *.tbl ../tpch-${SF}'.replace('${SF}', str(sf)))
	os.chdir(CURRENTDIR)

