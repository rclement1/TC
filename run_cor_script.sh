#!/bin/sh
#log="log"
set -x
. /etc/profile
. /etc/profile.d/modules.sh

module load anaconda

cd /exports/home/s1016630/

python corr_wavform.py

