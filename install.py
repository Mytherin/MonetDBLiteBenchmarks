
import mariadb
import monetdb
import postgres
import julia

mariadb.cleanup_install()
mariadb.delete_database()
monetdb.cleanup_install()
monetdb.delete_database()
postgres.cleanup_install()
postgres.delete_database()


mariadb.install()
monetdb.install()
postgres.install()
julia.install()
