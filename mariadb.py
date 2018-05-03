

import os
import sys
import time
import subprocess

MARIADB_VERSION = '10.2.14'
CURRENTDIR = os.getcwd()
PGDATA=os.path.join(CURRENTDIR, 'mariadbdata')
CMAKEDIR = os.path.join(CURRENTDIR, "mariadb-${VERSION}".replace("${VERSION}", MARIADB_VERSION), "TEMP_BUILD")
INSTALLDIR = os.path.join(CURRENTDIR, 'mariadb-build-${VERSION}'.replace('${VERSION}', MARIADB_VERSION))
CONFIGURATION_PARAMETERS = ''#'--with-blocksize=1 --with-segsize=1'

USER='mysql'
PASSWORD='my_password'
PORT = '3306'
SOCKET = '/tmp/mysql.sock'

FNULL = open(os.devnull, 'w')

optimal_configuration = {
	'client': {
		'password': 'my_password',
		'port': PORT,
		'socket': SOCKET
	},
	'mysqld': {
		'port': PORT,
		'socket': SOCKET,
		'datadir': PGDATA,
		'language': os.path.join(CURRENTDIR, '${CMAKEDIR}/sql/share/english'.replace("${CMAKEDIR}", CMAKEDIR))
	},
	'mysqldump': {
		'quick': None,
		'set-variable': 'max_allowed_packet=16M'
	},
	'mysql': {
		'no-auto-rehash': None
	},
	'myisamchk': {
		'set-variable': 'key_buffer=128M'
	}
}

def install(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	print("[MARIADB] Installing database")
	CURRENTDIR = os.getcwd()
	if not os.path.isfile('mariadb-${VERSION}.tar.gz'.replace('${VERSION}', MARIADB_VERSION)):
		print("[MARIADB] Downloading...")
		if os.system('wget https://downloads.mariadb.org/f/mariadb-${VERSION}/source/mariadb-${VERSION}.tar.gz ${PIPE}'.replace("${VERSION}", MARIADB_VERSION).replace("${PIPE}", pipe)):
			raise Exception('Failed to download')
	if os.system('tar xvf mariadb-${VERSION}.tar.gz ${PIPE}'.replace("${VERSION}", MARIADB_VERSION).replace("${PIPE}", pipe)):
		raise Exception("Failed to unzip")
	print("[MARIADB] Configuring")
	os.system('mkdir -p ${CMAKEDIR}'.replace("${CMAKEDIR}", CMAKEDIR))
	os.chdir(CMAKEDIR)
	if os.system('cmake -G "Unix Makefiles" .. ${PIPE}'.replace("${VERSION}", MARIADB_VERSION).replace("${PIPE}", pipe)):
		raise Exception("Failed CMake")
	print("[MARIADB] Compiling")
	if os.system('make ${PIPE}'.replace("${PIPE}", pipe)):
		raise Exception("Failed to make")
	if os.system('make install DESTDIR="${BUILD_DIR}"'.replace("${BUILD_DIR}", INSTALLDIR)):
		raise Exception("Failed to install")
	os.chdir(CURRENTDIR)

def is_installed():
	if os.path.exists(INSTALLDIR):
		return True
	return False

def cleanup_install():
	os.system('rm mariadb-${VERSION}.tar.gz'.replace("${VERSION}", MARIADB_VERSION))
	os.system('rm -r mariadb-${VERSION}'.replace("${VERSION}", MARIADB_VERSION))
	os.system('rm -r ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))

def init_db(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	CURRENTDIR = os.getcwd()
	os.system('mkdir -p ${DBDIR}'.replace("${DBDIR}", PGDATA))
	set_configuration(optimal_configuration)
	os.chdir('${BUILD_DIR}/usr/local/mysql'.replace("${BUILD_DIR}", INSTALLDIR))
	os.system('scripts/mysql_install_db ${PIPE}'.replace("${PIPE}", pipe))
	os.chdir(CURRENTDIR)

def execute_query(query, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/usr/local/mysql/bin/mysql -e "${QUERY}" ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${QUERY}", query).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute query \"${QUERY}\"".replace("${QUERY}", query))

def execute_file(fpath, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/usr/local/mysql/bin/mysql ${FILE} ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${FILE}", fpath).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute file \"${FILE}\"".replace("${FILE}", fpath))

def start_database(SILENT=True):
	process_path = ["${BUILD_DIR}/usr/local/mysql/bin/mysqld".replace("${BUILD_DIR}", INSTALLDIR)]
	if SILENT:
		process = subprocess.Popen(process_path, stdout=FNULL, stderr=subprocess.STDOUT)
	else:
		process = subprocess.Popen(process_path)
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
	return process

def stop_database(process, SILENT=True):
	process.terminate()

def delete_database():
	os.system('rm -rf "${DBDIR}"'.replace("${DBDIR}", PGDATA))

def load_tpch():
	CURRENTDIR = os.getcwd()
	os.chdir('scripts')
	print("[MARIADB] Creating schema")
	execute_file('mariadb.schema.sql')
	with open('mariadb.load.sql', 'r') as f:
		data = f.read()
		data = data.replace('DIR', os.path.join(CURRENTDIR, 'tpch-dbgen'))
	with open('mariadb.load.sql.tmp', 'w') as f:
		f.write(data)
	print("[MARIADB] Loading TPCH")
	execute_file('mariadb.load.sql.tmp')
	os.system('rm mariadb.load.sql.tmp')
	print("[MARIADB] Analyzing and building constraints")
	execute_file('mariadb.analyze.sql')
	execute_file('mariadb.constraints.sql')
	os.chdir(CURRENTDIR)

def benchmark_query(fpath, NRUNS):
	# hot run
	print("[MARIADB] Performing cold run...")
	execute_file(fpath)
	results = []
	for i in range(NRUNS):
		print("[MARIADB] Query %d/%d" % ((i + 1), NRUNS))
		start = time.time()
		execute_file(fpath)
		end = time.time()
		results.append(end - start)
	return results


def set_configuration(dict):
	HOME = os.environ['HOME']
	with open(os.path.join(HOME, '.my.cnf'), 'w+') as f:
		for entry in dict.keys():
			f.write("[%s]\n" % entry)
			for key,value in dict[entry].items():
				if value == None:
					f.write("%s\n" % (key,))
				else:
					f.write("%s=%s\n" % (key, value))
			f.write("\n")





