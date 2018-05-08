
# script used for installing everything

python install.py
source env.sh
R -f scripts/packages.R
julia scripts/packages.jl