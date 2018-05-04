

import os
import postgres
import mariadb
import monetdb
import tpch
import rbench
import dbbench

database_modules = [postgres, monetdb, mariadb]
databases = [dbmodule.dbname() for dbmodule in database_modules]
nruns = 10

# benchmark recipes


def benchmark_tpch_queries(system, nruns, sf=1):
	tpchdir = tpch.generate_tpch(sf)
	if system in databases:
		dbmodule = database_modules[databases.index(system)]
		dbbench.setup_database(dbmodule)
		dbbench.load_tpch(dbmodule, tpchdir, False)
		queries = ['queries/q01.sql', 'queries/q02.sql', 'queries/q03.sql']
		return dbbench.benchmark_queries(dbmodule, queries, nruns)
	else:
		raise Exception("Unrecognized system %s" % (system,))



print(benchmark_tpch_queries('postgres', nruns))
