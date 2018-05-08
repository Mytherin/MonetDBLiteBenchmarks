
EXTRA_CFLAGS=`python -c 'import mariadb, postgres, monetdb; print(mariadb.cflags() +  " " + postgres.cflags() + " " + monetdb.cflags())'`
EXTRA_LDFLAGS=`python -c 'import mariadb, postgres, monetdb; print(mariadb.ldflags() +  " " + postgres.ldflags() + " " + monetdb.ldflags())'`
EXTRA_PATH=`python -c 'import mariadb, postgres, monetdb; print(mariadb.path() +  ":" + postgres.path() + ":" + monetdb.path())'`

export CFLAGS="$EXTRA_CFLAGS $CFLAGS"
export LDFLAGS="$EXTRA_LDFLAGS $LDFLAGS"
export PATH="$EXTRA_PATH:$PATH"

