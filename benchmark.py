

import os
import postgres
import mariadb
import monetdb
import tpch
import scriptbench
import dbbench

database_modules = [postgres, monetdb, mariadb]
scripts = ['datatable', 'dplyr', 'pandas', 'julia', 'monetdblite']
databases = [dbmodule.dbname() for dbmodule in database_modules]
systems = scripts + databases
nruns = 10
sf = 10

queries = queries = range(1, 11)

# benchmark recipes
def benchmark_tpch_queries(system, nruns, sf=0.01):
	tpchdir = tpch.generate_tpch(sf)
	if system in databases:
		dbmodule = database_modules[databases.index(system)]
		dbbench.setup_database(dbmodule)
		dbbench.load_tpch(dbmodule, tpchdir, False)
		query_files = ['queries/q%02d.sql' % q for q in queries]
		return dbbench.benchmark_queries(dbmodule, query_files, nruns)
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
		return scriptbench.run_script(lang, [init_script], bench_scripts, [], nruns)
	else:
		raise Exception("Unrecognized system %s" % (system,))


def benchmark_tpch_readwrite(system, nruns, operation, sf):
	tpchdir = tpch.generate_tpch(sf)
	os.environ['TPCHSF'] = str(sf)
	if system in databases:
		dbmodule = database_modules[databases.index(system)]
		dbbench.setup_database(dbmodule)
		dbmodule.start_database()

		coninfo = dbmodule.get_connection_parameters()
		for entry in coninfo.keys():
			os.environ['DBINFO_' + entry.upper()] = coninfo[entry]
		init_scripts = ['scripts/tpch/%s/init.R' % (operation,), 'scripts/tpch/%s/%s.init.R'  % (operation, system)]
		bench_scripts = ['scripts/tpch/%s/%s.run.R' % (operation, system)]
		final_scripts = ['scripts/tpch/%s/%s.final.R' % (operation, system)]
		results = scriptbench.run_script(scriptbench.R, init_scripts, bench_scripts, final_scripts, nruns, False)
		dbmodule.stop_database()
		return results
	else:
		raise Exception("Unrecognized system %s" % (system,))

def benchmark_tpch_write(system, nruns, sf=0.01):
	return benchmark_tpch_readwrite(system, nruns, 'write', sf)

def benchmark_tpch_load(system, nruns, sf=0.01):
	return benchmark_tpch_readwrite(system, nruns, 'load', sf)

def write_results(f, system, results):
	for key in results.keys():
		file = key
		timings = results[file]
		for i in range(len(timings)):
			f.write(system + ',' + file + "," + str(i) + ',' + str(timings[i]) + '\n')
	f.flush()

dirname = 'results-sf%f' % sf
os.system('mkdir -p "%s"' % dirname)
benchmark_header = 'System,File,Run,Timing\n'

for dbmodule in database_modules:
	dbmodule.force_shutdown()

for system in systems:
	fname = os.path.join(dirname, '%s.csv' % system)
	if os.path.exists(fname): continue
	results = benchmark_tpch_queries(system, nruns, sf)
	with open(fname, 'w+') as f:
		f.write(benchmark_header)
		write_results(f, system, results)

for system in databases + ['monetdblite']:
	fname = os.path.join(dirname, '%s-write.csv' % system)
	if not os.path.exists(fname):
		results = benchmark_tpch_write(system, nruns, sf)
		with open(fname, 'w+') as f:
			f.write(benchmark_header)
			write_results(f, system, results)
	fname = os.path.join(dirname, '%s-load.csv' % system)
	if not os.path.exists(fname):
		results = benchmark_tpch_load(system, nruns, sf)
		with open(fname, 'w+') as f:
			f.write(benchmark_header)
			write_results(f, system, results)

