
using DataFrames, CSV
ne = false

tpchdir = ENV["TPCHDIR"]
region = CSV.read(joinpath(tpchdir, "region.tbl"), delim='|', header=["r_regionkey", "r_name", "r_comment"], nullable=ne)
nation = CSV.read(joinpath(tpchdir, "nation.tbl"), delim='|', header=["n_nationkey", "n_name", "n_regionkey", "n_comment"],  nullable=ne)
supplier = CSV.read(joinpath(tpchdir, "supplier.tbl"), delim='|', header=["s_suppkey","s_name","s_address","s_nationkey","s_phone","s_acctbal","s_comment"], nullable=ne)
customer = CSV.read(joinpath(tpchdir, "customer.tbl"), delim='|', header=["c_custkey","c_name","c_address","c_nationkey","c_phone","c_acctbal","c_mktsegment","c_comment"], nullable=ne)
part = CSV.read(joinpath(tpchdir, "part.tbl"), delim='|', header=["p_partkey","p_name","p_mfgr","p_brand","p_type","p_size","p_container","p_retailprice","p_comment"], nullable=ne)
partsupp = CSV.read(joinpath(tpchdir, "partsupp.tbl"), delim='|', header=["ps_partkey","ps_suppkey","ps_availqty","ps_supplycost","ps_comment"], nullable=ne)
orders = CSV.read(joinpath(tpchdir, "orders.tbl"), delim='|', header=["o_orderkey","o_custkey","o_orderstatus","o_totalprice","o_orderdate","o_orderpriority","o_clerk","o_shippriority","o_comment"], nullable=ne)
lineitem = CSV.read(joinpath(tpchdir, "lineitem.tbl"), delim='|', header=["l_orderkey","l_partkey","l_suppkey","l_linenumber","l_quantity","l_extendedprice","l_discount","l_tax","l_returnflag","l_linestatus","l_shipdate","l_commitdate","l_receiptdate","l_shipinstruct","l_shipmode","l_comment"], nullable=ne)

function q1()
	gc_enable(false)
	res = sort!(by(lineitem[lineitem[:l_shipdate] .<= Date("1998-09-01"), [:l_returnflag, :l_linestatus, :l_quantity, :l_extendedprice, :l_discount, :l_tax]], [:l_returnflag, :l_linestatus], df -> DataFrame(
		sum_qty        = sum(df[:l_quantity]), 
		sum_base_price = sum(df[:l_extendedprice]),
		sum_disc_price = sum(df[:l_extendedprice] .* (1 - df[:l_discount])),
		sum_charge     = sum(df[:l_extendedprice] .* (1 - df[:l_discount]) .* (1 + df[:l_tax])),
		avg_qty        = mean(df[:l_quantity]),
		avg_price      = mean(df[:l_extendedprice]),
		avg_disc       = mean(df[:l_discount]),
		count_order    = nrow(df)
	)), cols=[:l_returnflag, :l_linestatus])
	gc_enable(true)
	res
end

function q2()
	gc_enable(false)
	ps     = partsupp[[:ps_partkey, :ps_suppkey, :ps_supplycost]]
	p      = part[part[:p_size] .== 15 .& map(x->ismatch(r".*BRASS$", x), part[:p_type]), [:p_partkey, :p_mfgr]]
	psp    = join(ps, p, on = :ps_partkey => :p_partkey)
	sp     = supplier[[:s_suppkey, :s_nationkey, :s_acctbal, :s_name, :s_address, :s_phone, :s_comment]]
	psps   = join(psp, sp, on = :ps_suppkey => :s_suppkey) 
	nr     = join(nation, region, on = :n_regionkey => :r_regionkey)[[:n_nationkey, :n_name]]
	pspsnr = join(psps, nr, on = :s_nationkey => :n_nationkey)[[:ps_partkey, :ps_supplycost, :p_mfgr, :n_name, :s_acctbal, :s_name, :s_address, :s_phone, :s_comment]]
	aggr   = by(pspsnr, :ps_partkey, df -> DataFrame(ps_supplycost = minimum(df[:ps_supplycost])))
	sj     = join(pspsnr, aggr, on = [:ps_partkey, :ps_supplycost])
	res    = head(sort(sj[[:s_acctbal, :s_name, :n_name, :ps_partkey, :p_mfgr, :s_address, :s_phone, :s_comment]], 
		cols=[order(:s_acctbal, rev=true), :n_name, :s_name, :ps_partkey]), 100)
	gc_enable(true)
	res
end

function q3()
	gc_enable(false)
	o    = orders[orders[:o_orderdate] .<= Date("1995-03-15"), [:o_orderkey, :o_custkey, :o_orderdate, :o_shippriority]]
	c    = customer[customer[:c_mktsegment] .== "BUILDING", [:c_custkey, :c_mktsegment]]
	oc   = join(o, c, on = :o_custkey => :c_custkey)[[:o_orderkey, :o_orderdate, :o_shippriority]]
	l    = lineitem[lineitem[:l_shipdate] .> Date("1995-03-15"), [:l_orderkey, :l_extendedprice, :l_discount]]
	loc  = join(oc, l, on = :o_orderkey => :l_orderkey)
	aggr = by(loc, [:o_orderkey, :o_orderdate, :o_shippriority], df -> DataFrame(
		revenue = sum(df[:l_extendedprice] .* (1 - df[:l_discount]))
	))
	res  = head(sort(aggr[[:o_orderkey, :revenue, :o_orderdate, :o_shippriority]], 
		cols=[order(:revenue, rev=true), :o_orderkey]), 10)
	gc_enable(true)
	res
end

function q4()
	gc_enable(false)
	l   = lineitem[lineitem[:l_commitdate] .< lineitem[:l_receiptdate], [:l_orderkey]]
	o   = orders[(orders[:o_orderdate] .>= Date("1993-07-01")) .& 
		(orders[:o_orderdate] .< Date("1993-10-01")) , [:o_orderkey, :o_orderpriority]]
	lo  = unique(join(o, l, on = :o_orderkey => :l_orderkey))[[:o_orderpriority]]
	res = sort(by(lo, :o_orderpriority, df -> DataFrame(order_count=nrow(df))), cols=[:o_orderpriority])
	gc_enable(true)
	res
end

function q5()
	gc_enable(false)
	nr = join(nation, region[region[:r_name] .== "ASIA", :], 
		on = :n_regionkey => :r_regionkey)[[:n_nationkey, :n_name]]
	snr = join(supplier[[:s_suppkey, :s_nationkey]], nr, on = :s_nationkey => :n_nationkey)[[:s_suppkey, :s_nationkey, :n_name]]
	lsnr = join(snr, lineitem[[:l_suppkey, :l_orderkey, :l_extendedprice, :l_discount]], on = :s_suppkey => :l_suppkey)[[:l_orderkey, :l_extendedprice, :l_discount, :n_name, :s_nationkey]]
	o = orders[(orders[:o_orderdate] .>= Date("1994-01-01")) .& 
		(orders[:o_orderdate] .< Date("1995-01-01")), [:o_orderkey, :o_custkey]]
	oc = join(o, customer[[:c_custkey, "c_nationkey"]], on = :o_custkey => :c_custkey)[[:o_orderkey, :c_nationkey]]
	lsnroc = join(oc, lsnr, on = [:o_orderkey => :l_orderkey, :c_nationkey => :s_nationkey])[[:l_extendedprice, :l_discount, :n_name]]
	res = sort(by(lsnroc, :n_name, df -> DataFrame(
		revenue = sum(df[:l_extendedprice] .* (1 - df[:l_discount]))
	)), cols=[order(:revenue, rev=true)])
	gc_enable(true)
	res
end

function q6()
	gc_enable(false)
	l = lineitem[(lineitem[:l_shipdate] .>= Date("1994-01-01")) .& 
		(lineitem[:l_shipdate] .< Date("1995-01-01")) .& 
		(lineitem[:l_discount] .>= 0.05) .& 
		(lineitem[:l_discount] .<= 0.07) .& 
		(lineitem[:l_quantity] .< 24), [:l_extendedprice, :l_discount]]
	res = sum(l[:l_extendedprice] .* l[:l_discount])
	gc_enable(true)
	res
end

function q7()
	gc_enable(false)
	n = nation[(nation[:n_name] .== "GERMANY") .| (nation[:n_name] .== "FRANCE"), [:n_nationkey, :n_name]]
	sn = rename(join(supplier[[:s_nationkey, :s_suppkey]], n, on = :s_nationkey => :n_nationkey), :n_name => :n1_name)[[:s_suppkey, :n1_name]]
	cn = rename(join(customer[[:c_custkey, :c_nationkey]], n, 
		on = :c_nationkey => :n_nationkey), :n_name => :n2_name)
	cno = join(orders, cn, on = :o_custkey => :c_custkey)[[:o_orderkey, :n2_name]]
	l = lineitem[(lineitem[:l_shipdate] .>= Date("1995-01-01")) .& 
		(lineitem[:l_shipdate] .<= Date("1995-12-31")), [:l_orderkey, :l_suppkey, :l_shipdate, :l_extendedprice, :l_discount]]
	cnol = join(cno, l, on=:o_orderkey => :l_orderkey)[[:l_suppkey, :l_shipdate, :l_extendedprice, :l_discount, :n2_name]]
	cnolsn = join(cnol,  sn, on=:l_suppkey => :s_suppkey)
	cnolsnf = cnolsn[((cnolsn[:n1_name] .== "FRANCE") .& 
			(cnolsn[:n2_name] .== "GERMANY")) .| 
		((cnolsn[:n1_name] .== "GERMANY") .& 
			(cnolsn[:n2_name] .== "FRANCE")), :]
	cnolsnf[:l_year] = map(x -> Dates.year(x), cnolsnf[:l_shipdate])
	res = sort(by(cnolsnf, [:n1_name, :n2_name, :l_year],  df -> DataFrame(
		revenue = sum(df[:l_extendedprice] .* (1 - df[:l_discount]))
	)), cols=[:n1_name, :n2_name, :l_year])
	gc_enable(true)
	res
end

function q8()
	gc_enable(false)
	nr  = join(nation, region[region[:r_name] .== "AMERICA", :], on = :n_regionkey => :r_regionkey)[[:n_nationkey]]
	cnr = join(customer[[:c_custkey, :c_nationkey]], nr, on=:c_nationkey => :n_nationkey)[[:c_custkey]]
	o = orders[(orders[:o_orderdate] .>= Date("1995-01-01")) .& 
		(orders[:o_orderdate] .<= Date("1996-12-31")) ,[:o_orderkey, :o_orderdate, :o_custkey]]
	ocnr = join(o, cnr, on=:o_custkey => :c_custkey)[[:o_orderkey, :o_orderdate]]
	locnr = join(lineitem[[:l_orderkey, :l_partkey, :l_suppkey, :l_extendedprice, :l_discount]], ocnr, 
		on = :l_orderkey => :o_orderkey)[[:l_partkey, :l_suppkey, :l_extendedprice, :l_discount, :o_orderdate]]
	p = part[part[:p_type] .== "ECONOMY ANODIZED STEEL", [:p_partkey]]
	locnrp = join(locnr, p, on=:l_partkey => :p_partkey)[[:l_suppkey, :l_extendedprice, :l_discount, :o_orderdate]]
	locnrps = join(supplier[[:s_suppkey, :s_nationkey]], locnrp, 
		on=:s_suppkey => :l_suppkey)[[:l_extendedprice, :l_discount, :o_orderdate, :s_nationkey]]
	locnrpsn = join(locnrps,  nation[[:n_nationkey, :n_name]], on=:s_nationkey => :n_nationkey)
	locnrpsn[:o_year] = map(x -> Dates.year(x), locnrpsn[:o_orderdate])
	locnrpsn[:volume] = locnrpsn[:l_extendedprice] .* (1 - locnrpsn[:l_discount])

	res = sort(by(locnrpsn, :o_year, df -> DataFrame(
		mkt_share = sum(ifelse.(df[:n_name] .== "BRAZIL", df[:volume], 0)) / 
			sum(df[:volume])
	)), cols=:o_year)
	gc_enable(true)
	res
end

function q9()
	gc_enable(false)
	p = part[map(x->ismatch(r".*green.*", x), part[:p_name]), [:p_partkey]]
	psp = join(partsupp[[:ps_suppkey, :ps_partkey, :ps_supplycost]], p, on=:ps_partkey => :p_partkey)
	sn = join(supplier[[:s_suppkey, :s_nationkey]], nation[[:n_nationkey, :n_name]], on=:s_nationkey => :n_nationkey)[[:s_suppkey, :n_name]]
	pspsn = join(psp, sn, on=:ps_suppkey => :s_suppkey)
	lpspsn = join(lineitem[[:l_suppkey, :l_partkey, :l_orderkey, :l_extendedprice, :l_discount, :l_quantity]], pspsn, 
		on=[:l_suppkey => :ps_suppkey, :l_partkey => :ps_partkey])[[:l_orderkey, :l_extendedprice, :l_discount, :l_quantity, :ps_supplycost, :n_name]]
	lpspsno = join(lpspsn, 	orders[[:o_orderkey, :o_orderdate]], 
		on=:l_orderkey => :o_orderkey)[[:l_extendedprice, :l_discount, :l_quantity, :ps_supplycost, :n_name, :o_orderdate]]
	lpspsno[:o_year] = map(x -> Dates.year(x), lpspsno[:o_orderdate])
	lpspsno[:amount] = lpspsno[:l_extendedprice] .* (1 .- lpspsno[:l_discount]) .- 
		lpspsno[:ps_supplycost] .* lpspsno[:l_quantity]
	res = sort(by(lpspsno[[:n_name, :o_year, :amount]], [:n_name, :o_year], df -> DataFrame(
		sum_profit = sum(df[:amount])
	)), cols = [:n_name, order(:o_year, rev = true)])
	gc_enable(true)
	res
end

function q10()
	gc_enable(false)
	l = lineitem[lineitem[:l_returnflag] .== "R", [:l_orderkey, :l_extendedprice, :l_discount]]
	o = orders[(orders[:o_orderdate] .>= Date("1993-10-01")) .& 
		(orders[:o_orderdate] .< Date("1994-01-01")) ,[:o_orderkey, :o_custkey]]
	lo = join(o, l, on = :o_orderkey => :l_orderkey)
	lo[:volume] = lo[:l_extendedprice] .* (1 - lo[:l_discount])
	lo_aggr = by(lo, :o_custkey, df -> DataFrame(revenue = sum(df[:volume])))
	c = customer[[:c_custkey, :c_nationkey, :c_name, :c_acctbal, :c_phone, :c_address, :c_comment]]
	loc = join(lo_aggr, c, on = :o_custkey => :c_custkey)
	locn = join(loc, nation[[:n_nationkey, :n_name]], on = :c_nationkey => :n_nationkey)
	res = head(sort(locn[[:o_custkey, :c_name, :revenue, :c_acctbal, :n_name, :c_address, :c_phone, :c_comment]], cols = order(:revenue, rev = true)), 20)
	gc_enable(true)
	res
end
