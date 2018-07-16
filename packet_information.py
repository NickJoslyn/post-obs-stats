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

## Locations == /mnt_blc00/datax/dibas/AGBT18A_999_77/GUPPI/BLP00

numberOfScans = int(subprocess.check_output("ls /mnt_blc00/datax/dibas/AGBT18A_999_77/GUPPI/BLP00/*gpuspec..headers | wc -l",shell=True)[:-1])
numberOfBanks = 3
numberOfNodes = 8
NETBUFST_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))

################################################################################
### NETBUFST

for bank in range(numberOfBanks):
    for node in range(numberOfNodes):
        NETBUFST_command = """for i in /mnt_blc""" + str(bank) + str(node) + """/datax/dibas/AGBT18A_999_77/GUPPI/BLP""" + str(bank) + str(node) + """/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk '{ total += $1} END {print total/NR}'; done"""
        NETBUFST_waterfall[(bank*numberOfNodes + node),:] = subprocess.check_output(NETBUFST_command, shell=True)[:-1].split("\n")

plt.imshow(NETBUFST_waterfall)
plt.colorbar()
plt.clim(0,24)
plt.show()
################################################################################
### NDROP






################################################################################
### PKTIDX
















# Gets the NETBUFST value
#/usr/bin/fold -w80 blc00_guppi_58278_52387_HIP1125_0057.gpuspec..headers | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}'

# Gets the average NETBUFST value
#/usr/bin/fold -w80 blc00_guppi_58278_52387_HIP1125_0057.gpuspec..headers | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk '{ total += $1} END {print total/NR}'

# blc00:
# test = """/usr/bin/fold -w80 /mnt_blc00/datax/dibas/AGBT18A_999_77/GUPPI/BLP00/blc00_guppi_58278_52387_HIP1125_0057.gpuspec..headers | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk '{ total += $1} END {print total/NR}'"""
# float(subprocess.check_output(test, shell = True)[:-1])

### full : for i in /mnt_blc00/datax/dibas/AGBT18A_999_77/GUPPI/BLP00/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk '{ total += $1} END {print total/NR}'; done
