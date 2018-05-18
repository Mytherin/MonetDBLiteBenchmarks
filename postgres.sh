export ACS_DATABASE_TYPE=PostgreSQL
export DBINFO_HOST=`python -c "import postgres as db; print(db.get_connection_parameters()['host'])"`
export DBINFO_PORT=`python -c "import postgres as db; print(db.get_connection_parameters()['port'])"`
export DBINFO_DATABASE=`python -c "import postgres as db; print(db.get_connection_parameters()['database'])"`
export DBINFO_USER=`python -c "import postgres as db; print(db.get_connection_parameters()['user'])"`
export DBINFO_PASSWORD=`python -c "import postgres as db; print(db.get_connection_parameters()['password'])"`


