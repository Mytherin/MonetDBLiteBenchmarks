-- TPCH integry constraints for postgres 9.x
-- hannes@cwi.nl, 2014-04-04

-- For table REGION
ALTER TABLE region ADD PRIMARY KEY (r_regionkey);

-- For table NATION
ALTER TABLE nation ADD PRIMARY KEY (n_nationkey);
ALTER TABLE nation ADD CONSTRAINT NATION_FK1 FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey);

-- For table PART
ALTER TABLE part ADD PRIMARY KEY (p_partkey);

-- For table SUPPLIER
ALTER TABLE supplier ADD PRIMARY KEY (s_suppkey);
ALTER TABLE supplier ADD CONSTRAINT SUPPLIER_FK1 FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey);

-- For table PARTSUPP
ALTER TABLE partsupp ADD PRIMARY KEY (ps_partkey,ps_suppkey);

-- For table CUSTOMER
ALTER TABLE customer ADD PRIMARY KEY (c_custkey);
ALTER TABLE customer ADD CONSTRAINT CUSTOMER_FK1 FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey);

-- For table LINEITEM
ALTER TABLE lineitem ADD PRIMARY KEY (l_orderkey,l_linenumber);

-- For table ORDERS
ALTER TABLE orders ADD PRIMARY KEY (o_orderkey);

-- For table PARTSUPP
ALTER TABLE partsupp ADD CONSTRAINT PARTSUPP_FK1 FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey);
ALTER TABLE partsupp ADD CONSTRAINT PARTSUPP_FK2 FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey);

-- For table ORDERS
ALTER TABLE orders ADD CONSTRAINT ORDERS_FK1 FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey);

-- For table LINEITEM
ALTER TABLE lineitem ADD CONSTRAINT LINEITEM_FK1 FOREIGN KEY (l_orderkey)  REFERENCES orders (o_orderkey);
ALTER TABLE lineitem ADD CONSTRAINT LINEITEM_FK2 FOREIGN KEY (l_partkey,l_suppkey) REFERENCES partsupp (ps_partkey,ps_suppkey);




