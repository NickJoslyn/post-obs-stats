# Nicholas Joslyn
# Breakthrough Listen UC Berkeley SETI Intern 2018
# Creates waterfall plots detailing packet information during a GBT observation.

# Imports
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import matplotlib.colors as mcolors
from argparse import ArgumentParser

# Green to Red colormaps for waterfall plots
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

# All compute nodes at GB. Add to/subtract from as necessary
TOTAL_COMPUTE_NODES = ['00', '01', '02', '03', '04', '05', '06', '07', '10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37']

def plotting_packet_info(packet_data, title_identifier, colormap, type_to_plot, topClim, apprehensionLim, dangerLim, criticalLim):
    """
    Save the waterfall plot for NETBUFST, NDROP, and PKTIDX to the corresponding directory.

    Simple statistics are calculated and shown in top right of figure. The green-red
    waterfall plot follows this template:
        - Bottom x-axis: Scan Name
        - Left y-axis: Compute Node
        - Right y-axis: Compute Node
        - Top x-axis: Start Time of Scan

    Return: Nothing
    """

    global totalLength, numberOfBanks, numberOfNodes, computeNodeNames, numberOfScans, scanNames, timeStamps

    # Some simple statistics
    maxindex1 = np.unravel_index(np.argmax(packet_data, axis=None), packet_data.shape)[0]
    maxindex2 = np.unravel_index(np.argmax(packet_data, axis=None), packet_data.shape)[1]
    maxNode = computeNodeNames[maxindex1]
    maxTime = timeStamps[maxindex2]
    maxValue = round(packet_data[maxindex1, maxindex2],2)
    numberOfApprehension = round(100*(len(np.where(packet_data > apprehensionLim)[0])/float(totalLength)),2)
    numberOfDanger = round(100*(len(np.where(packet_data > dangerLim)[0])/float(totalLength)),2)
    numberOfCritical = round(100*(len(np.where(packet_data > criticalLim)[0])/float(totalLength)),2)

    # Begin figure
    fig = plt.figure(figsize=(25,15))
    plt.gcf().subplots_adjust(bottom = 0.2)
    ax1 = fig.add_subplot(111)
    plt.suptitle(title_identifier + SESSION_IDENTIFIER)
    im = ax1.imshow(packet_data, cmap = colormap, aspect='auto')
    clb = plt.colorbar(im, fraction = 0.025, pad = 0.09)
    im.set_clim(0,topClim)
    textForPlot = "Max: " + str(maxNode) + " | " + str(maxTime) + " | " + str(maxValue) + "\n>" + str(apprehensionLim) + ": " + str(numberOfApprehension)+ "%\n>" + str(dangerLim) + ": " + str(numberOfDanger) + "%\n>" + str(criticalLim) + ": " + str(numberOfCritical) + "%"
    ax1.text(1.02, 1.1, textForPlot, verticalalignment = 'center', transform = ax1.transAxes)

    # Set up left, right, and bottom axes
    ax1.set_yticks(np.arange(numberOfBanks*numberOfNodes))
    ax1.set_yticklabels(computeNodeNames)
    ax1.set_xticks(np.arange(numberOfScans))
    ax1.set_xticklabels(scanNames, rotation = 90)
    ax1.tick_params(labelright = True, right = True, top = True, labeltop = False)

    # Put time on top x axis
    ax2 = fig.add_axes(ax1.get_position(), frameon = False)
    ax2.tick_params(labelbottom = 'off', top = 'off', labeltop = 'on', labelleft = 'off', labelright = 'off', bottom = 'off', left = 'off', right = 'off')
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(np.arange(numberOfScans))
    ax2.set_xticklabels(timeStamps, rotation = 90)
    plt.draw()
    pos1 = ax1.get_position()
    ax2.set_position([pos1.x0, pos1.y0, pos1.width, pos1.height])
    plt.draw()

    # Save to relevant folders
    plt.savefig((type_to_plot + "/" + str(SESSION_IDENTIFIER) + "_" + type_to_plot + ".png"), bbox_inches = 'tight')
    plt.close()


if __name__ == "__main__":

    # Command Line Arguments
    parser = ArgumentParser(description="Creates waterfall plots showing packet diagnostics from a GBT observation. Plots are saved to NETBUFST, NDROP, and PKTIDX directories by default. Run from storage node (or similar location with all compute nodes mounted)")
    parser.add_argument('-s', action='store', default='', dest='session_name', type=str,
                        help="Session name. Default: Last created dibas directory in first compute node of /home/obs/triggers/hosts_running")
    parser.add_argument('-b', action='store', default=8, dest='nodes_in_bank', type=int,
                        help="Nodes per bank. Program assumes total number of compute nodes is multiple of this value. Default: 8 (unlikely to change from default)")
    parser.add_argument('-o', action='store', default='No', dest='old_session_date', type=str,
                        help="Date of non-current observation (YYYMMDD). Only use if desired session is not from this semester. MUST specify session name. Default: 'No'")
    parser.add_argument('-n', action='store', default=['NETBUFST', 'NDROP', 'PKTIDX'], dest='directory_names', nargs = 3, type=str,
                        help="Directory names to store png's. Specify 3 locations. Default: 'NETBUFST NDROP PKTIDX'")

    # Initialize
    parse_args = parser.parse_args()
    SESSION_IDENTIFIER = parse_args.session_name
    numberOfNodes = parse_args.nodes_in_bank
    DATE_STRING = parse_args.old_session_date
    DIRECTORY_NAMES = parse_args.directory_names

    # Make folder for .png's if it doesn't exist
    for individualDirectory in DIRECTORY_NAMES:
        if (int(subprocess.check_output("find -maxdepth 1 -type d -name " + individualDirectory + " | wc -l", shell=True)) == 0):
            subprocess.Popen("mkdir " + individualDirectory, shell=True)

    # If user doesn't specify a date (i.e. not using archived dibas data)
    if (DATE_STRING == 'No'):

        # If using default, find the session of first active node as returned by hosts_running trigger
        if (SESSION_IDENTIFIER == ''):
            first_active_node = subprocess.check_output(['cat', '/home/obs/triggers/hosts_running']).replace('blc','').split()[0]
            test_if_any_sessions = "ls -tr /mnt_blc" + first_active_node + "/datax/dibas"

            if (subprocess.check_output(test_if_any_sessions, shell = True)[:-1] == ''):
                print("No sessions in first active node given by hosts_running trigger")
                quit()

            string_for_session = 'ls -trd /mnt_blc' + first_active_node + '/datax/dibas/* | tail -1'
            SESSION_IDENTIFIER = subprocess.check_output(string_for_session, shell = True)[23:-1]

        ################################################################################
        ### Generic

        # Find the compute nodes used during the specified session
        ACTIVE_COMPUTE_NODES = []
        for i in TOTAL_COMPUTE_NODES:
            if (subprocess.check_output("ls -tr /mnt_blc" + str(i) + "/datax/dibas", shell = True)[:-1] != ''):
                temp = subprocess.check_output("ls -trd /mnt_blc" + str(i) + "/datax/dibas/*", shell = True).split()
                if (np.any(np.array(temp) == ('/mnt_blc' + str(i) + '/datax/dibas/' + SESSION_IDENTIFIER))):
                    ACTIVE_COMPUTE_NODES.append(i)
        ACTIVE_COMPUTE_NODES = np.array(ACTIVE_COMPUTE_NODES).reshape(-1, numberOfNodes)

        # Names of nodes for graphing
        computeNodeNames = []
        for i in ACTIVE_COMPUTE_NODES.reshape(-1):
            computeNodeNames.append('blc' + str(i))

        numberOfBanks = ACTIVE_COMPUTE_NODES.shape[0]

        # Find the scan/target names
        numberOfScans = int(subprocess.check_output("ls /mnt_blc" + str(ACTIVE_COMPUTE_NODES[0,0]) + "/datax/dibas/" + SESSION_IDENTIFIER + "/GUPPI/*/*gpuspec..headers | wc -l",shell=True)[:-1])
        scanName_command = """ls /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/*/*.gpuspec..headers | awk '{print substr($1, 75, index($1,".")-75)}'"""
        scanNames = subprocess.check_output(scanName_command, shell=True).split('\n')

        # Find the initial time stamp of the scan
        timeStamp_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep DAQPULSE | awk 'NR==1{print$5}'; done"""
        timeStamps = subprocess.check_output(timeStamp_command, shell = True).split('\n')[:-1]

        totalLength = numberOfBanks * numberOfNodes * numberOfScans

        ################################################################################
        ### NETBUFST
        # Loop through and find max value in each scan for each compute node

        NETBUFST_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))

        for bank in range(numberOfBanks):
            print("Analyzing NETBUFST for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                NETBUFST_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk 'BEGIN {max = 0} {if ($1 > max) max = $1} END {print max}'; done"""
                try:
                    NETBUFST_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NETBUFST_command, shell=True)[:-1].split("\n")
                except:
                    NETBUFST_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("NETBUFST Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(NETBUFST_waterfall, "Max Location in Memory Ring Buffer: ", cmap, DIRECTORY_NAMES[0], 24, 6, 12, 18)

        ################################################################################
        ### NDROP
        # Loop through and find average value in each scan for each compute node

        NDROP_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
        for bank in range(numberOfBanks):
            print("Analyzing NDROP for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                NDROP_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NDROP | awk '{print $3}' | sort | uniq -c | awk '{print $1 * $2}' | awk '{total += $1} END {print 100*(total/(NR*16384))}'; done"""
                try:
                    NDROP_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NDROP_command, shell=True)[:-1].split("\n")
                except:
                    NDROP_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("NDROP Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(NDROP_waterfall, "Percentage of Packets Dropped: ", cmap, DIRECTORY_NAMES[1], 100, 25, 50, 75)

        ################################################################################
        ### PKTIDX
        # Loop through and find average value in each scan for each compute node

        PKTIDX_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
        for bank in range(numberOfBanks):
            print("Analyzing PKTIDX for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                PKTIDX_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas/""" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep PKTIDX | awk '{print $3 - p; p = $3}' | sort | uniq -c | awk 'BEGIN{sum=0; number = 0}{number += $1}{if ($2>16384) sum += $1 * ($2/16384 - 1)} END {print sum/number*100}'; done"""
                try:
                    PKTIDX_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(PKTIDX_command, shell=True)[:-1].split("\n")
                except:
                    PKTIDX_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("PKTIDX Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(PKTIDX_waterfall, "Percentage of Blocks Dropped: ", cmap2, DIRECTORY_NAMES[2], 100, 25, 50, 75)

    # If user specifies date, then use that date and session name to find the archived data
    else:

        ################################################################################
        ### Generic

        # Find the compute nodes used during the specified session
        ACTIVE_COMPUTE_NODES = []
        for i in TOTAL_COMPUTE_NODES:
            temp = subprocess.check_output("ls -trd /mnt_blc" + str(i) + "/datax/*", shell = True).split()
            if (np.any(np.array(temp) == ('/mnt_blc' + str(i) + '/datax/dibas.' + DATE_STRING))):
                ACTIVE_COMPUTE_NODES.append(i)

        ACTIVE_COMPUTE_NODES = np.array(ACTIVE_COMPUTE_NODES).reshape(-1, numberOfNodes)

        # Names of nodes for graphing
        computeNodeNames = []
        for i in ACTIVE_COMPUTE_NODES.reshape(-1):
            computeNodeNames.append('blc' + str(i))

        numberOfBanks = ACTIVE_COMPUTE_NODES.shape[0]

        # Find the scan/target names
        numberOfScans = int(subprocess.check_output("ls /mnt_blc" + str(ACTIVE_COMPUTE_NODES[0,0]) + "/datax/dibas." + DATE_STRING + "/" + SESSION_IDENTIFIER + "/GUPPI/*/*gpuspec..headers | wc -l",shell=True)[:-1])
        scanName_command = """ls /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas.""" + DATE_STRING + "/" + SESSION_IDENTIFIER + """/GUPPI/*/*.gpuspec..headers | awk '{print substr($1, index($1, "BLP"), index($1,".gpuspec"))}' | awk '{print substr($1, 31, index($1, ".gpuspec") - 36)}'"""
        scanNames = subprocess.check_output(scanName_command, shell=True).split('\n')

        # Find the initial time stamp of the scan
        timeStamp_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[0,0]) + """/datax/dibas.""" + DATE_STRING + "/" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep DAQPULSE | awk 'NR==1{print$5}'; done"""
        timeStamps = subprocess.check_output(timeStamp_command, shell = True).split('\n')[:-1]

        totalLength = numberOfBanks * numberOfNodes * numberOfScans

        ################################################################################
        ### NETBUFST
        # Loop through and find max value in each scan for each compute node

        NETBUFST_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))

        for bank in range(numberOfBanks):
            print("Analyzing NETBUFST for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                NETBUFST_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas.""" + DATE_STRING + "/" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NETBUFST | awk '{print substr($2,2, index($2,"/")-2)}' | awk 'BEGIN {max = 0} {if ($1 > max) max = $1} END {print max}'; done"""
                try:
                    NETBUFST_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NETBUFST_command, shell=True)[:-1].split("\n")
                except:
                    NETBUFST_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("NETBUFST Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(NETBUFST_waterfall, "Max Location in Memory Ring Buffer: ", cmap, DIRECTORY_NAMES[0], 24, 6, 12, 18)

        ###############################################################################
        ## NDROP
        # Loop through and find average value in each scan for each compute node

        NDROP_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
        for bank in range(numberOfBanks):
            print("Analyzing NDROP for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                NDROP_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas.""" + DATE_STRING + "/" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep NDROP | awk '{print $3}' | sort | uniq -c | awk '{print $1 * $2}' | awk '{total += $1} END {print 100*(total/(NR*16384))}'; done"""
                try:
                    NDROP_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(NDROP_command, shell=True)[:-1].split("\n")
                except:
                    NDROP_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("NDROP Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(NDROP_waterfall, "Percentage of Packets Dropped: ", cmap, DIRECTORY_NAMES[1], 100, 25, 50, 75)

        ################################################################################
        ### PKTIDX
        # Loop through and find average value in each scan for each compute node

        PKTIDX_waterfall = np.zeros((numberOfBanks*numberOfNodes, numberOfScans))
        for bank in range(numberOfBanks):
            print("Analyzing PKTIDX for blc" + str(ACTIVE_COMPUTE_NODES[bank,0][0])+"*")
            for node in range(numberOfNodes):
                PKTIDX_command = """for i in /mnt_blc""" + str(ACTIVE_COMPUTE_NODES[bank,node]) + """/datax/dibas.""" + DATE_STRING + "/" + SESSION_IDENTIFIER + """/GUPPI/*/*gpuspec..headers; do /usr/bin/fold -w80 $i | grep PKTIDX | awk '{print $3 - p; p = $3}' | sort | uniq -c | awk 'BEGIN{sum=0; number = 0}{number += $1}{if ($2>16384) sum += $1 * ($2/16384 - 1)} END {print sum/number*100}'; done"""
                try:
                    PKTIDX_waterfall[(bank*numberOfNodes + node), :] = subprocess.check_output(PKTIDX_command, shell=True)[:-1].split("\n")
                except:
                    PKTIDX_waterfall[(bank*numberOfNodes + node), :] = -float('Inf')
                    print("PKTIDX Problem with " + str(ACTIVE_COMPUTE_NODES[bank,node]))

        plotting_packet_info(PKTIDX_waterfall, "Percentage of Blocks Dropped: ", cmap2, DIRECTORY_NAMES[2], 100, 25, 50, 75)
