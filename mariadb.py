

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

USER='root'
PORT = '3306'
SOCKET = '/tmp/mysql.sock'
DBNAME = 'test'

FNULL = open(os.devnull, 'w')

DBPROCESS = None

optimal_configuration = {
	'client': {
		'user': USER,
		'port': PORT,
		'socket': SOCKET,
		'database': DBNAME
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
	os.system('rm -rf mariadb-${VERSION}'.replace("${VERSION}", MARIADB_VERSION))
	os.system('rm -rf ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))

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
	if os.system('${BUILD_DIR}/usr/local/mysql/bin/mysql --batch -e "${QUERY}" ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${QUERY}", query).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute query \"${QUERY}\"".replace("${QUERY}", query))

def execute_file(fpath, SILENT=True):
	execute_query('source ' + fpath, SILENT)

def start_database(SILENT=True):
	global DBPROCESS
	process_path = ["${BUILD_DIR}/usr/local/mysql/bin/mysqld".replace("${BUILD_DIR}", INSTALLDIR)]
	if SILENT:
		DBPROCESS = subprocess.Popen(process_path, stdout=FNULL, stderr=subprocess.STDOUT)
	else:
		DBPROCESS = subprocess.Popen(process_path)
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

def stop_database(SILENT=True):
	global DBPROCESS
	DBPROCESS.terminate()

def delete_database():
	os.system('rm -rf "${DBDIR}"'.replace("${DBDIR}", PGDATA))

def dbname():
	return 'mariadb'

def get_connection_parameters():
	return {
		'host': 'localhost',
		'port': PORT,
		'database': DBNAME,
		'user': USER,
		'password': '',
		'socket': SOCKET
	}

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


def cflags():
	return '-I${BUILD_DIR}/usr/local/mysql/include/mysql'.replace("${BUILD_DIR}", INSTALLDIR)

def ldflags():
	return '-L${BUILD_DIR}/usr/local/mysql/lib'.replace("${BUILD_DIR}", INSTALLDIR)

def path():
	return '${BUILD_DIR}/usr/local/mysql/bin'.replace("${BUILD_DIR}", INSTALLDIR)

def force_shutdown():
	os.system('killall -9 mysqld >/dev/null 2>/dev/null')
