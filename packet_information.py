# Nicholas Joslyn
# Breakthrough Listen UC Berkeley SETI Intern 2018

# Program to produce plots regarding NETBUFST, NDROP, and PKTIDX from reduced files

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import matplotlib.colors as mcolors

cdict = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 0.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0))}

cdict2 = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.6, 0.6),
                   (1.0, 1.0, 1.0)),
         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 0.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0))}


cmap = mcolors.LinearSegmentedColormap('my_colormap', cdict, 100)
cmap2 = mcolors.LinearSegmentedColormap('my_colormap', cdict2, 100)


numberOfNodes = 8
TOTAL_COMPUTE_NODES = ['00', '01', '02', '03', '04', '05', '06', '07', '10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37']
ACTIVE_COMPUTE_NODES = []
SESSION_IDENTIFIER = "AGBT18A_999_122"

for i in TOTAL_COMPUTE_NODES:
    temp = subprocess.check_output("ls -trd /mnt_blc" + str(i) + "/datax/dibas/*", shell = True).split()
    if (np.any(np.array(temp) == ('/mnt_blc' + str(i) + '/datax/dibas/' + SESSION_IDENTIFIER))):
        ACTIVE_COMPUTE_NODES.append(i)

ACTIVE_COMPUTE_NODES = np.array(ACTIVE_COMPUTE_NODES).reshape(-1, numberOfNodes)

numberOfScans = int(subprocess.check_output("ls /mnt_blc" + str(ACTIVE_COMPUTE_NODES[0,0]) + "/datax/dibas/" + SESSION_IDENTIFIER + "/GUPPI/BLP00/*gpuspec..headers | wc -l",shell=True)[:-1])

numberOfBanks = ACTIVE_COMPUTE_NODES.shape[0]

################################################################################
### NETBUFST
NETBUFST_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
computeNodeNames = []

for bank in range(numberOfBanks):
    print("Analyzing NETBUFST for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
    for node in range(numberOfNodes):
        NETBUFST_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP""" + str(bank) + str(node) + """/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk 'BEGIN {max = 0} {if ($1 > max) max = $1} END {print max}'; done"""
        try:
            NETBUFST_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NETBUFST_command, shell=True)[:-1].split("\n")
        except:
            NETBUFST_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
            print("NETBUFST Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))
        computeNodeNames.append('blc' + str(ACTIVE_COMPUTE_NODES[bank,node]))

scanName_command = """ls /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP00/*.gpuspec..headers | awk '{print substr($1, 75, index($1,".")-75)}'"""
scanNames = subprocess.check_output(scanName_command, shell=True).split('\n')

timeStamp_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP00/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep DAQPULSE | awk 'NR==1{print$5}'; done"""
timeStamps = subprocess.check_output(timeStamp_command, shell = True).split('\n')[:-1]

plt.figure(figsize=(12,10))
plt.title("Max Location in Memory Ring Buffer: " + SESSION_IDENTIFIER)
plt.imshow(NETBUFST_waterfall, cmap = cmap)
plt.colorbar()
plt.clim(0,24)

plt.yticks(np.arange(numberOfBanks*numberOfNodes), computeNodeNames)
plt.tick_params(labelright = True, right = True)
plt.xticks(np.arange(numberOfScans), scanNames, rotation = 90)

tempAxis = plt.twiny()
tempAxis.set_xticks(np.arange(numberOfScans))
tempAxis.set_xticklabels(timeStamps, rotation = 90)

plt.tight_layout()
plt.savefig("testfinal.png", bbox_inches = 'tight')
plt.show()
################################################################################
### NDROP
NDROP_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
for bank in range(numberOfBanks):
    print("Analyzing NDROP for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
    for node in range(numberOfNodes):
        NDROP_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP""" + str(bank) + str(node) + """/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NDROP | awk '{print $3}' | sort | uniq -c | awk '{print $1 * $2}' | awk '{total += $1} END {print 100*(total/(NR*16384))}'; done"""
        try:
            NDROP_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NDROP_command, shell=True)[:-1].split("\n")
        except:
            NDROP_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
            print("NDROP Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

plt.title("Percentage of Packets Dropped: " + SESSION_IDENTIFIER)
plt.imshow(NDROP_waterfall, cmap = cmap)
plt.colorbar()
plt.clim(0,100)
#plt.ylabel("Source")
#plt.xlabel("Compute Node")
plt.tick_params(labelright = True)
plt.yticks(np.arange(numberOfBanks*numberOfNodes), computeNodeNames)
plt.xticks(np.arange(numberOfScans), scanNames, rotation = 90)
plt.tight_layout()
plt.show()



################################################################################
### PKTIDX
PKTIDX_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
for bank in range(numberOfBanks):
    print("Analyzing PKTIDX for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
    for node in range(numberOfNodes):
        PKTIDX_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP""" + str(bank) + str(node) + """/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep PKTIDX | awk '{print $3 - p; p = $3}' | sort | uniq -c | awk 'BEGIN{sum=0; number = 0}{number += $1}{if ($2>16384) sum += $1 * ($2/16384 - 1)} END {print sum/number*100}'; done"""
        try:
            PKTIDX_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(PKTIDX_command, shell=True)[:-1].split("\n")
        except:
            PKTIDX_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
            print("PKTIDX Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

plt.title("Percentage of Blocks Dropped: " + SESSION_IDENTIFIER)
plt.imshow(PKTIDX_waterfall, cmap = cmap2)
plt.colorbar()
plt.clim(0,100)
#plt.ylabel("Source")
#plt.xlabel("Compute Node")
plt.tick_params(labelright = True)
plt.yticks(np.arange(numberOfBanks*numberOfNodes), computeNodeNames)
plt.xticks(np.arange(numberOfScans), scanNames, rotation = 90)
plt.tight_layout()
plt.show()
