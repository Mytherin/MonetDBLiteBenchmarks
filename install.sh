
# script used for installing everything

python install.py
source env.sh
julia scripts/packages.jl

export PKG_CFLAGS=$CFLAGS
export LIB_DIR=`python -c "import mariadb; print(mariadb.ldflags()[2:])"`
export LIB_DIR="$LIB_DIR `mariadb_config --libs`"
R -f scripts/packages.R