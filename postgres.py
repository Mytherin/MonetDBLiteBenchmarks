

import os
import sys
import time

POSTGRES_VERSION = '9.6.1'
CURRENTDIR = os.getcwd()
PGDATA=os.path.join(CURRENTDIR, 'pgdata')
INSTALLDIR = os.path.join(CURRENTDIR, 'postgresql-build-${VERSION}'.replace('${VERSION}', POSTGRES_VERSION))
CONFIGURATION_PARAMETERS = ''#'--with-blocksize=1 --with-segsize=1'


optimal_configuration = {
	'shared_buffers': '10GB',
	'effective_cache_size': '14GB',
	'maintenance_work_mem': '4GB',
	'work_mem': '10GB',
	'autovacuum': 'off',
	'random_page_cost': '3.5',
	'geqo_threshold': '15',
	'from_collapse_limit': '14',
	'join_collapse_limit': '14',
	'default_statistics_target': '10000',
	'constraint_exclusion': 'on',
	'wal_buffers': '32MB',
	'max_connections': '10',
	'checkpoint_completion_target': '0.9',
	'temp_buffers': '1GB'
}

def install(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	print("[POSTGRES] Installing database")
	CURRENTDIR = os.getcwd()
	os.system('mkdir -p ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))
	if not os.path.isfile('postgresql-${VERSION}.tar.gz'.replace('${VERSION}', POSTGRES_VERSION)):
		print("[POSTGRES] Downloading...")
		if os.system('wget https://ftp.postgresql.org/pub/source/v${VERSION}/postgresql-${VERSION}.tar.gz ${PIPE}'.replace("${VERSION}", POSTGRES_VERSION).replace("${PIPE}", pipe)):
			raise Exception('Failed to download')
	if os.system('tar xvf postgresql-${VERSION}.tar.gz ${PIPE}'.replace("${VERSION}", POSTGRES_VERSION).replace("${PIPE}", pipe)):
		raise Exception("Failed to unzip")
	print("[POSTGRES] Configuring")
	#os.system('rm postgresql-${VERSION}.tar.gz'.replace("${VERSION}", POSTGRES_VERSION))
	os.chdir('postgresql-${VERSION}'.replace("${VERSION}", POSTGRES_VERSION).replace("${PIPE}", pipe))
	if os.system('./configure --prefix="${BUILD_DIR}" ${EXTRA_CONFIGURATION} --disable-debug --disable-cassert CFLAGS="-O3" ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${EXTRA_CONFIGURATION}", CONFIGURATION_PARAMETERS).replace("${PIPE}", pipe)):
		raise Exception("Failed to configure")
	print("[POSTGRES] Compiling")
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
	os.system('rm postgresql-${VERSION}.tar.gz'.replace("${VERSION}", POSTGRES_VERSION))
	os.system('rm -r postgresql-${VERSION}'.replace("${VERSION}", POSTGRES_VERSION))
	os.system('rm -r ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))

def init_db(SILENT=True):
	print("[POSTGRES] Initializing database")
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.environ['PGDATA'] = PGDATA
	os.system('${BUILD_DIR}/bin/initdb ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${PIPE}", pipe))
	set_configuration(optimal_configuration)

def execute_query(query, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/bin/psql -d postgres -c "${QUERY}" ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${QUERY}", query).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute query \"${QUERY}\"".replace("${QUERY}", query))

def execute_file(fpath, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/bin/psql -d postgres -f ${FILE} ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${FILE}", fpath).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute file \"${FILE}\"".replace("${FILE}", fpath))

def start_database(SILENT=True):
	print("[POSTGRES] Starting database")
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.environ['PGDATA'] = PGDATA
	os.system("${BUILD_DIR}/bin/pg_ctl -l logfile start ${PIPE}".replace("${BUILD_DIR}", INSTALLDIR).replace("${PIPE}", pipe))
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

def stop_database(process=None, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	os.environ['PGDATA'] = PGDATA
	os.system("${BUILD_DIR}/bin/pg_ctl stop ${PIPE}".replace("${BUILD_DIR}", INSTALLDIR).replace("${PIPE}", pipe))

def delete_database():
	os.system('rm -rf "${DBDIR}"'.replace("${DBDIR}", PGDATA))

def dbname():
	return 'postgres'

def set_configuration(dict):
	os.system('cp ${BUILD_DIR}/share/postgresql.conf.sample ${DBDIR}/postgresql.conf'.replace("${BUILD_DIR}", INSTALLDIR).replace("${DBDIR}", PGDATA))
	with open('${DBDIR}/postgresql.conf'.replace("${DBDIR}", PGDATA), 'a') as f:
		for entry in dict.keys():
			f.write('${PROPERTY} = ${VALUE}\n'.replace('${PROPERTY}', str(entry)).replace('${VALUE}', dict[entry]))

