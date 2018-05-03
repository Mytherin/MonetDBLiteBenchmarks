

import os
import sys
import time

MONETDB_MAIN_VERSION='Mar2018'
MONETDB_VERSION = '11.29.3'
CURRENTDIR = os.getcwd()
PGDATA=os.path.join(CURRENTDIR, 'pgdata')
INSTALLDIR = os.path.join(CURRENTDIR, 'monetdb-build-${VERSION}'.replace('${VERSION}', MONETDB_VERSION))




def install(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	print("[MONETDB] Installing database")
	CURRENTDIR = os.getcwd()
	os.system('mkdir -p ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))
	if not os.path.isfile('MonetDB-${VERSION}.tar.bz2'.replace('${VERSION}', MONETDB_VERSION)):
		print("[POSTGRES] Downloading...")
		if os.system('wget https://www.monetdb.org/downloads/sources/${MAIN_VERSION}/MonetDB-${VERSION}.tar.bz2 ${PIPE}'.replace("${MAIN_VERSION}", MONETDB_MAIN_VERSION).replace("${VERSION}", MONETDB_VERSION).replace("${PIPE}", pipe)):
			raise Exception('Failed to download')
	# if os.system('tar xvf MonetDB-${VERSION}.tar.bz2 ${PIPE}'.replace("${VERSION}", MONETDB_VERSION).replace("${PIPE}", pipe)):
	# 	raise Exception("Failed to unzip")
	print("[MONETDB] Configuring")
	#os.system('rm postgresql-${VERSION}.tar.gz'.replace("${VERSION}", POSTGRES_VERSION))
	os.chdir('MonetDB-${VERSION}'.replace("${VERSION}", MONETDB_VERSION))
	if os.system('./configure --prefix="${BUILD_DIR}" --disable-strict --disable-assert --disable-debug --enable-optimize ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${PIPE}", pipe)):
		raise Exception("Failed to configure")
	print("[MONETDB] Compiling")
	if os.system('make ${PIPE}'.replace("${PIPE}", pipe)):
		raise Exception("Failed to make")
	if os.system('make install ${PIPE}'.replace("${PIPE}", pipe)):
		raise Exception("Failed to install")
	os.chdir(CURRENTDIR)

def is_installed():
	if os.path.exists(INSTALLDIR):
		return True
	return False

def cleanup_install():
	os.system('rm MonetDB-${VERSION}.tar.bz2'.replace("${VERSION}", MONETDB_VERSION))
	os.system('rm -r MonetDB-${VERSION}'.replace("${VERSION}", MONETDB_VERSION))
	os.system('rm -r ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))

def init_db():
	pass

def execute_query(query):
	if os.system('${BUILD_DIR}/bin/mclient -s "${QUERY}" >/dev/null 2>/dev/null'.replace("${BUILD_DIR}", INSTALLDIR).replace("${QUERY}", query)):
		raise Exception("Failed to execute query \"${QUERY}\"".replace("${QUERY}", query))

def execute_file(fpath):
	if os.system('${BUILD_DIR}/bin/mclient ${FILE} > /dev/null'.replace("${BUILD_DIR}", INSTALLDIR).replace("${FILE}", fpath)):
		raise Exception("Failed to execute file \"${FILE}\"".replace("${FILE}", fpath))

def start_database():
	os.environ['PGDATA'] = PGDATA
	os.system("${BUILD_DIR}/bin/pg_ctl -l logfile start".replace("${BUILD_DIR}", INSTALLDIR))
	attempts = 0
	while True:
		try:
			attempts += 1
			if attempts > 100:
				break
			execute_query('SELECT 1')
			break
		except:
			time.sleep(0.1)
			pass

def stop_database():
	os.environ['PGDATA'] = PGDATA
	os.system("${BUILD_DIR}/bin/pg_ctl stop 2>/dev/null".replace("${BUILD_DIR}", INSTALLDIR))

def delete_database():
	os.system('rm -rf "${DBDIR}"'.replace("${DBDIR}", PGDATA))

def load_tpch():
	CURRENTDIR = os.getcwd()
	os.chdir('scripts')
	print("[POSTGRES] Creating schema")
	execute_file('postgres.schema.sql')
	with open('postgres.load.sql', 'r') as f:
		data = f.read()
		data = data.replace('DIR', os.path.join(CURRENTDIR, 'tpch-dbgen'))
	with open('postgres.load.sql.tmp', 'w') as f:
		f.write(data)
	print("[POSTGRES] Loading TPCH")
	execute_file('postgres.load.sql.tmp')
	os.system('rm postgres.load.sql.tmp')
	print("[POSTGRES] Analyzing and building constraints")
	execute_file('postgres.analyze.sql')
	execute_file('postgres.constraints.sql')
	os.chdir(CURRENTDIR)

def benchmark_query(fpath, NRUNS):
	# hot run
	print("[POSTGRES] Performing cold run...")
	execute_file(fpath)
	results = []
	for i in range(NRUNS):
		print("[POSTGRES] Query %d/%d" % ((i + 1), NRUNS))
		start = time.time()
		execute_file(fpath)
		end = time.time()
		results.append(end - start)
	return results


def set_configuration(dict):
	os.system('cp ${BUILD_DIR}/share/postgresql.conf.sample ${DBDIR}/postgresql.conf'.replace("${BUILD_DIR}", INSTALLDIR).replace("${DBDIR}", PGDATA))
	with open('${DBDIR}/postgresql.conf'.replace("${DBDIR}", PGDATA), 'a') as f:
		for entry in dict.keys():
			f.write('${PROPERTY} = ${VALUE}\n'.replace('${PROPERTY}', str(entry)).replace('${VALUE}', dict[entry]))

