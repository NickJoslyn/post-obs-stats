# Nicholas Joslyn
# Breakthrough Listen UC Berkeley SETI Intern 2018

# Program to produce plots regarding NETBUFST, NDROP, and PKTIDX from reduced files

import numpy as np
import matplotlib.pyplot as plt
import subprocess
#from mpl_toolkits.axes_grid1 import make_axes_locatable
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

TOTAL_COMPUTE_NODES = ['00', '01', '02', '03', '04', '05', '06', '07', '10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37']

def plotting_packet_info(packet_data, title_identifier, colormap, type_to_plot, topClim, dangerLim, criticalLim):
    global totalLength, numberOfBanks, numberOfNodes, computeNodeNames, numberOfScans, scanNames, timeStamps


    maxindex1 = np.unravel_index(np.argmax(packet_data, axis=None), packet_data.shape)[0]
    maxindex2 = np.unravel_index(np.argmax(packet_data, axis=None), packet_data.shape)[1]

    maxNode = computeNodeNames[maxindex1]
    maxTime = timeStamps[maxindex1]
    maxValue = packet_data[maxindex1, maxindex2]
    numberOfDanger = round(100*(len(np.where(packet_data > dangerLim)[0])/totalLength),2)
    numberOfCritical = round(100*(len(np.where(packet_data > criticalLim)[0])/totalLength),2)

    fig = plt.figure(figsize=(12,10))
    plt.gcf().subplots_adjust(bottom = 0.2)
    ax1 = fig.add_subplot(111)
    plt.suptitle(title_identifier + SESSION_IDENTIFIER)
    im = ax1.imshow(packet_data, cmap = colormap)
    clb = plt.colorbar(im, fraction = 0.025, pad = 0.09)
    #clb.ax.set_title("blc max = 24\nblc min = 0")
    im.set_clim(0,topClim)
    textForPlot = "Max: blc" + str(maxNode) + " | " + str(maxTime) + " | " + str(maxValue) + "\n>" + str(dangerLim) + ": " + str(numberOfDanger) + "%\n>" + str(criticalLim) + ": " + str(numberOfCritical) + "%"
    ax1.text(1.1, 1.1, textForPlot, verticalalignment = 'center', transform = ax1.transAxes)

    ax1.set_yticks(np.arange(numberOfBanks*numberOfNodes))
    ax1.set_yticklabels(computeNodeNames)
    ax1.set_xticks(np.arange(numberOfScans))
    ax1.set_xticklabels(scanNames, rotation = 90)
    ax1.tick_params(labelright = True, right = True, top = True, labeltop = False)

    ax2 = fig.add_axes(ax1.get_position(), frameon = False)
    ax2.tick_params(labelbottom = 'off', top = 'off', labeltop = 'on', labelleft = 'off', labelright = 'off', bottom = 'off', left = 'off', right = 'off')
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(np.arange(numberOfScans))
    ax2.set_xticklabels(timeStamps, rotation = 90)

    plt.draw()
    pos1 = ax1.get_position()
    ax2.set_position([pos1.x0, pos1.y0-0.042, pos1.width, pos1.height])
    plt.draw()
    plt.show()
    plt.savefig((type_to_plot + "/" + str(SESSION_IDENTIFIER) + "_" + type_to_plot + ".png"), bbox_inches = 'tight')
    plt.close()


if __name__ == "__main__":

    numberOfNodes = 8
    SESSION_IDENTIFIER = "AGBT18A_999_122"

    ################################################################################
    ### Generic
    ACTIVE_COMPUTE_NODES = []
    for i in TOTAL_COMPUTE_NODES:
        temp = subprocess.check_output("ls -trd /mnt_blc" + str(i) + "/datax/dibas/*", shell = True).split()
        if (np.any(np.array(temp) == ('/mnt_blc' + str(i) + '/datax/dibas/' + SESSION_IDENTIFIER))):
            ACTIVE_COMPUTE_NODES.append(i)

    ACTIVE_COMPUTE_NODES = np.array(ACTIVE_COMPUTE_NODES).reshape(-1, numberOfNodes)

    computeNodeNames = []
    for i in ACTIVE_COMPUTE_NODES.reshape(-1):
        computeNodeNames.append('blc' + str(i))

    numberOfBanks = ACTIVE_COMPUTE_NODES.shape[0]

    numberOfScans = int(subprocess.check_output("ls /mnt_blc" + str(ACTIVE_COMPUTE_NODES[0,0]) + "/datax/dibas/" + SESSION_IDENTIFIER + "/GUPPI/BLP00/*gpuspec..headers | wc -l",shell=True)[:-1])

    scanName_command = """ls /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP00/*.gpuspec..headers | awk '{print substr($1, 75, index($1,".")-75)}'"""
    scanNames = subprocess.check_output(scanName_command, shell=True).split('\n')

    timeStamp_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP00/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep DAQPULSE | awk 'NR==1{print$5}'; done"""
    timeStamps = subprocess.check_output(timeStamp_command, shell = True).split('\n')[:-1]

    totalLength = numberOfBanks * numberOfNodes * numberOfScans

    ################################################################################
    ### NETBUFST
    NETBUFST_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))

    for bank in range(numberOfBanks):
        print("Analyzing NETBUFST for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
        for node in range(numberOfNodes):
            NETBUFST_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/BLP""" + str(bank) + str(node) + """/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk 'BEGIN {max = 0} {if ($1 > max) max = $1} END {print max}'; done"""
            try:
                NETBUFST_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NETBUFST_command, shell=True)[:-1].split("\n")
            except:
                NETBUFST_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                print("NETBUFST Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

    plotting_packet_info(NETBUFST_waterfall, "Max Location in Memory Ring Buffer: ", cmap, "NETBUFST", 24, 12, 20)

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

    plotting_packet_info(NDROP_waterfall, "Percentage of Packets Dropped: ", cmap, "NDROP", 100, 50, 75)

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

    plotting_packet_info(PKTIDX_waterfall, "Percentage of Blocks Dropped: ", cmap2, "PKTIDX", 100, 50, 75)
