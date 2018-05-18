export ACS_DATABASE_TYPE=MySQL
export DBINFO_HOST=`python -c "import mariadb as db; print(db.get_connection_parameters()['host'])"`
export DBINFO_PORT=`python -c "import mariadb as db; print(db.get_connection_parameters()['port'])"`
export DBINFO_DATABASE=`python -c "import mariadb as db; print(db.get_connection_parameters()['database'])"`
export DBINFO_USER=`python -c "import mariadb as db; print(db.get_connection_parameters()['user'])"`
export DBINFO_PASSWORD=`python -c "import mariadb as db; print(db.get_connection_parameters()['password'])"`
export DBINFO_SOCKET=`python -c "import mariadb as db; print(db.get_connection_parameters()['socket'])"`


