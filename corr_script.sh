#!/bin/sh

qsub -R y -P geos_tc_seis -q ecdf@tc02 -l s_rt=06:00:00 /exports/home/s1016630/run_cor_script.sh
