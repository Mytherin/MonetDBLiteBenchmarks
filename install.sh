
# script used for installing everything

python install.py
source env.sh
julia scripts/packages.jl
R -f scripts/packages.R