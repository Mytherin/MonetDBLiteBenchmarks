

import os
import sys
import time
import subprocess

MONETDB_MAIN_VERSION='Mar2018'
MONETDB_VERSION = '11.29.3'
CURRENTDIR = os.getcwd()
INSTALLDIR = os.path.join(CURRENTDIR, 'monetdb-build-${VERSION}'.replace('${VERSION}', MONETDB_VERSION))
DBDIR=os.path.join(INSTALLDIR, 'var/monetdb5/dbfarm/demo')


FNULL = open(os.devnull, 'w')

DBPROCESS = None

optimal_configuration = {
	'user':'monetdb',
	'password':'monetdb'
}

def install(SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	print("[MONETDB] Installing database")
	CURRENTDIR = os.getcwd()
	os.system('mkdir -p ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))
	if not os.path.isfile('MonetDB-${VERSION}.tar.bz2'.replace('${VERSION}', MONETDB_VERSION)):
		print("[MONETDB] Downloading...")
		if os.system('wget https://www.monetdb.org/downloads/sources/${MAIN_VERSION}/MonetDB-${VERSION}.tar.bz2 ${PIPE}'.replace("${MAIN_VERSION}", MONETDB_MAIN_VERSION).replace("${VERSION}", MONETDB_VERSION).replace("${PIPE}", pipe)):
			raise Exception('Failed to download')
	if os.system('tar xvf MonetDB-${VERSION}.tar.bz2 ${PIPE}'.replace("${VERSION}", MONETDB_VERSION).replace("${PIPE}", pipe)):
	 	raise Exception("Failed to unzip")
	print("[MONETDB] Configuring")
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
	os.system('rm -rf MonetDB-${VERSION}'.replace("${VERSION}", MONETDB_VERSION))
	os.system('rm -rf ${BUILD_DIR}'.replace("${BUILD_DIR}", INSTALLDIR))

def init_db(SILENT=True):
	set_configuration(optimal_configuration)

def execute_query(query, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/bin/mclient -s "${QUERY}" ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${QUERY}", query).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute query \"${QUERY}\"".replace("${QUERY}", query))

def execute_file(fpath, SILENT=True):
	pipe = ">/dev/null 2>/dev/null" if SILENT else ""
	if os.system('${BUILD_DIR}/bin/mclient ${FILE} ${PIPE}'.replace("${BUILD_DIR}", INSTALLDIR).replace("${FILE}", fpath).replace("${PIPE}", pipe)):
		raise Exception("Failed to execute file \"${FILE}\"".replace("${FILE}", fpath))

def start_database(SILENT=True):
	global DBPROCESS
	process_path = ["${BUILD_DIR}/bin/mserver5".replace("${BUILD_DIR}", INSTALLDIR)]
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
	DBPROCESS.terminate()

def delete_database():
	os.system('rm -rf "${DBDIR}"'.replace("${DBDIR}", DBDIR))

def dbname():
	return 'monetdb'

def get_connection_parameters():
	return {
		'host': 'localhost',
		'port': '50000',
		'database': 'demo',
		'user': 'monetdb',
		'password': 'monetdb'
	}

def set_configuration(dict):
	dotmonetdb = os.path.join(os.environ['HOME'], '.monetdb')
	if not os.path.isfile(dotmonetdb):
		with open(dotmonetdb, 'w+') as f:
			for entry in dict.keys():
				f.write('${PROPERTY}=${VALUE}\n'.replace('${PROPERTY}', str(entry)).replace('${VALUE}', dict[entry]))

def cflags():
	return '-I${BUILD_DIR}/include'.replace("${BUILD_DIR}", INSTALLDIR)

def ldflags():
	return '-L${BUILD_DIR}/lib'.replace("${BUILD_DIR}", INSTALLDIR)
