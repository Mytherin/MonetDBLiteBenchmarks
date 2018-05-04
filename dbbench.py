

import os
import time

def load_tpch(dbmodule, tpchdir, SILENT=True):
	dbmodule.start_database()
	dbname = dbmodule.dbname()
	CURRENTDIR = os.getcwd()
	os.chdir('scripts')
	print("[${DBNAME}] Creating schema".replace('${DBNAME}', dbname.upper()))
	dbmodule.execute_file('${DBNAME}.schema.sql'.replace('${DBNAME}', dbname), SILENT)
	with open('${DBNAME}.load.sql'.replace('${DBNAME}', dbname), 'r') as f:
		data = f.read()
		data = data.replace('DIR', tpchdir)
	with open('${DBNAME}.load.sql.tmp'.replace('${DBNAME}', dbname), 'w') as f:
		f.write(data)
	print("[${DBNAME}] Loading TPCH".replace('${DBNAME}', dbname.upper()))
	dbmodule.execute_file('${DBNAME}.load.sql.tmp'.replace('${DBNAME}', dbname), SILENT)
	os.system('rm ${DBNAME}.load.sql.tmp'.replace('${DBNAME}', dbname))
	print("[${DBNAME}] Analyzing and building constraints".replace('${DBNAME}', dbname.upper()))
	dbmodule.execute_file('${DBNAME}.analyze.sql'.replace('${DBNAME}', dbname), SILENT)
	dbmodule.execute_file('${DBNAME}.constraints.sql'.replace('${DBNAME}', dbname), SILENT)
	os.chdir(CURRENTDIR)
	dbmodule.stop_database()


def benchmark_query(dbmodule, fpath, NRUNS):
	# cold run
	dbname = dbmodule.dbname()
	print("[${DBNAME}] Benchmarking query ${QUERY}".replace('${DBNAME}', dbname.upper()).replace('${QUERY}', fpath))
	print("[${DBNAME}] Performing cold run...".replace('${DBNAME}', dbname.upper()))
	dbmodule.execute_file(fpath)
	results = []
	for i in range(NRUNS):
		# hot runs
		print("[${DBNAME}] Query %d/%d".replace('${DBNAME}', dbname.upper()) % ((i + 1), NRUNS))
		start = time.time()
		dbmodule.execute_file(fpath)
		end = time.time()
		results.append(end - start)
	return results


def setup_database(dbmodule):
	try:
		dbmodule.stop_database()
	except:
		pass
	if not dbmodule.is_installed():
		dbmodule.install()
	dbmodule.delete_database()
	dbmodule.init_db()

def benchmark_queries(dbmodule, queries, NRUNS):
	dbmodule.start_database()
	results = {}
	for query in queries:
		results[query] = benchmark_query(dbmodule, query, NRUNS)
	dbmodule.stop_database()
	return results

