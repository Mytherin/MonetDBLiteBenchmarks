-- TPCH schema postgres 9.x
-- hannes@cwi.nl, 2014-04-04

create table nation  ( n_nationkey  INTEGER NOT NULL,
                            n_name       CHAR(25) NOT NULL,
                            n_regionkey  INTEGER NOT NULL,
                            n_comment    VARCHAR(152));

create table region  ( r_regionkey  INTEGER NOT NULL,
                            r_name       CHAR(25) NOT NULL,
                            r_comment    VARCHAR(152));

create table part  ( p_partkey     INTEGER NOT NULL,
                          p_name        VARCHAR(55) NOT NULL,
                          p_mfgr        CHAR(25) NOT NULL,
                          p_brand       CHAR(10) NOT NULL,
                          p_type        VARCHAR(25) NOT NULL,
                          p_size        INTEGER NOT NULL,
                          p_container   CHAR(10) NOT NULL,
                          p_retailprice DECIMAL(15,2) NOT NULL,
                          p_comment     VARCHAR(23) NOT NULL );

create table supplier ( s_suppkey     INTEGER NOT NULL,
                             s_name        CHAR(25) NOT NULL,
                             s_address     VARCHAR(40) NOT NULL,
                             s_nationkey   INTEGER NOT NULL,
                             s_phone       CHAR(15) NOT NULL,
                             s_acctbal     DECIMAL(15,2) NOT NULL,
                             s_comment     VARCHAR(101) NOT NULL);

create table partsupp ( Ps_partkey     INTEGER NOT NULL,
                             Ps_suppkey     INTEGER NOT NULL,
                             Ps_availqty    INTEGER NOT NULL,
                             Ps_supplycost  DECIMAL(15,2)  NOT NULL,
                             Ps_comment     VARCHAR(199) NOT NULL );

create table customer ( c_custkey     INTEGER NOT NULL,
                             c_name        VARCHAR(25) NOT NULL,
                             c_address     VARCHAR(40) NOT NULL,
                             c_nationkey   INTEGER NOT NULL,
                             c_phone       CHAR(15) NOT NULL,
                             c_acctbal     DECIMAL(15,2)   NOT NULL,
                             c_mktsegment  CHAR(10) NOT NULL,
                             c_comment     VARCHAR(117) NOT NULL);

create table orders  ( o_orderkey       INTEGER NOT NULL,
                           o_custkey        INTEGER NOT NULL,
                           o_orderstatus    CHAR(1) NOT NULL,
                           o_totalprice     DECIMAL(15,2) NOT NULL,
                           o_orderdate      DATE NOT NULL,
                           o_orderpriority  CHAR(15) NOT NULL,  
                           o_clerk          CHAR(15) NOT NULL, 
                           o_shippriority   INTEGER NOT NULL,
                           o_comment        VARCHAR(79) NOT NULL);

create table lineitem ( l_orderkey    INTEGER NOT NULL,
                             l_partkey     INTEGER NOT NULL,
                             l_suppkey     INTEGER NOT NULL,
                             l_linenumber  INTEGER NOT NULL,
                             l_quantity    DECIMAL(15,2) NOT NULL,
                             l_extendedprice  DECIMAL(15,2) NOT NULL,
                             l_discount    DECIMAL(15,2) NOT NULL,
                             l_tax         DECIMAL(15,2) NOT NULL,
                             l_returnflag  CHAR(1) NOT NULL,
                             l_linestatus  CHAR(1) NOT NULL,
                             l_shipdate    DATE NOT NULL,
                             l_commitdate  DATE NOT NULL,
                             l_receiptdate DATE NOT NULL,
                             l_shipinstruct CHAR(25) NOT NULL,
                             l_shipmode     CHAR(10) NOT NULL,
                             l_comment      VARCHAR(44) NOT NULL);

