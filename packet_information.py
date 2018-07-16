# Nicholas Joslyn
# Breakthrough Listen UC Berkeley SETI Intern 2018

# Program to produce plots regarding NETBUFST, NDROP, and PKTIDX from reduced files

## /usr/bin/fold -w80 blc24_guppi_*0026.gpuspec..headers | grep PKTIDX | awk '{print $3-p;p=$3}' | sort | uniq -c | tail -n +3 | awk '{sum+= $1 * ($2/16384-1)}END{print sum}'

## for i in *.gpuspec..headers; do /usr/bin/fold -w80 $i | grep PKTIDX | awk '{print $3-p;p=$3}' | sort | uniq -c | tail -n +3 | awk '{sum+= $1 * ($2/16384-1)}END{print sum}' ; done
## for i in *.gpuspec..headers; do echo "$i" ; /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print $2}' | awk '{print substr($1,2,1)}' | sort | uniq -c; done
## for i in *.gpuspec..headers; do echo "$i" ; /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print $2}' | awk '{if(substr($1,2,1) ~ /^[2-9]+$/) print substr($1,2,1)}' | sort | uniq -c | awk '{print $1}'; done
## for i in *.gpuspec..headers; do echo "$i" ; /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print $2}' | awk '{if(substr($1,2,1) == 0 || substr($1,2,1) == 1) print substr($1,2,1)}' | sort | uniq -c | awk '{print $1}'; done

import numpy as np
import matplotlib.pyplot as plt
import subprocess
