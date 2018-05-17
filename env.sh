
EXTRA_CFLAGS=`python -c 'import mariadb, postgres, monetdb; print(mariadb.cflags() +  " " + postgres.cflags() + " " + monetdb.cflags())'`
EXTRA_LDFLAGS=`python -c 'import mariadb, postgres, monetdb; print(mariadb.ldflags() +  " " + postgres.ldflags() + " " + monetdb.ldflags())'`
EXTRA_PATH=`python -c 'import mariadb, postgres, monetdb, julia; print(mariadb.path() +  ":" + postgres.path() + ":" + monetdb.path() + ":" + julia.path())'`

export CFLAGS="$EXTRA_CFLAGS $CFLAGS"
export LDFLAGS="$EXTRA_LDFLAGS $LDFLAGS"
export PATH="$EXTRA_PATH:$PATH"

export PKG_CFLAGS=$CFLAGS
export INCLUDE_DIR='.'
export LIB_DIR=`python -c "import mariadb; print(mariadb.ldflags()[2:])"`
export LIB_DIR="$LIB_DIR `mariadb_config --libs`"
export LD_LIBRARY_PATH=`python -c "import mariadb; print(mariadb.ldflags()[2:])"`
