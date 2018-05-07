

import os
import postgres
import mariadb
import monetdb
import tpch
import scriptbench
import dbbench

database_modules = [postgres, monetdb, mariadb]
scripts = ['datatable', 'dplyr', 'pandas', 'julia']
databases = [dbmodule.dbname() for dbmodule in database_modules]
nruns = 10

queries = [1]#queries = range(1, 11)

# benchmark recipes
def benchmark_tpch_queries(system, nruns, sf=0.01):
	global queries
	tpchdir = tpch.generate_tpch(sf)
	if system in databases:
		dbmodule = database_modules[databases.index(system)]
		dbbench.setup_database(dbmodule)
		dbbench.load_tpch(dbmodule, tpchdir, False)
		queries = ['queries/q%02d.sql' % q for q in queries]
		return dbbench.benchmark_queries(dbmodule, queries, nruns)
	elif system in scripts:
		os.environ['TPCHDIR'] = tpchdir
		os.environ['TPCHSF'] = str(sf)
		#scriptbench.init()
		lang = scriptbench.R
		ext = 'R'
		init_script = ''
		bench_scripts = []
		if system == 'julia':
			lang = scriptbench.Julia
			ext = 'jl'
		elif system == 'pandas':
			lang = scriptbench.Python
			ext = 'py'
		init_script = 'scripts/tpch/%s/init.%s' % (system, ext)
		bench_scripts = ['scripts/tpch/%s/q%02d.%s' % (system, q, ext) for q in queries]
		print(init_script)
		print(bench_scripts)
		return scriptbench.run_script(lang, init_script, bench_scripts, nruns, False)
	else:
		raise Exception("Unrecognized system %s" % (system,))



print(benchmark_tpch_queries('pandas', nruns, 0.01))
#print(benchmark_tpch_queries('datatable', nruns))
