# post-obs-stats
Display packet statistics following a Breakthrough Listen observation

After running blctl reduce (and it finishes) on a Breakthrough Listen Green Bank Observatory observation, run this program to get information regarding:
* The maximum location in memory ring buffer in which files were written to disk (NETBUFST)
* The average percentage of packets dropped (NDROP)
* The average percentage of blocks dropped (PKTIDX)

** There must be NETBUFST, NDROP, and PKTIDX sub-directories in the same directory as the program.** These sub-directories are where the .png's are saved.

Run this program from a storage node (**_or any node with all compute nodes -- include blc18 -- mounted_**)

---

'''python
>>> python packet_information.py -h

usage: packet_information.py [-h] [-s SESSION_NAME] [-b NODES_IN_BANK]
                             [-o OLD_SESSION_DATE]

Creates waterfall plots showing packet diagnostics from a GBT observation.
Plots are saved to NETBUFST, NDROP, and PKTIDX directories. Run from storage
node (or similar location with all compute nodes mounted)
optional arguments:
  -h, --help           show this help message and exit
  -s SESSION_NAME      Session name. Default: Last created dibas directory in
                       first compute node of /home/obs/triggers/hosts_running
  -b NODES_IN_BANK     Nodes per bank. Program assumes total number of compute
                       nodes is multiple of this value. Default: 8 (unlikely
                       to change from default)
  -o OLD_SESSION_DATE  Date of non-current observation (YYYMMDD). Only use if
                       desired session is not from this semester. MUST specify
                       session name. Default: 'No'
'''

The defaults are set to run the analysis on the most recent observation.

(The most recent observation is determined by running the active_hosts trigger and using the last modified directory in the active compute node's dibas directory.)

'''python
>>> python packet_information.py
Analyzing NETBUFST for blc0*
Analyzing NDROP for blc0*
Analyzing PKTIDX for blc0*
'''

To run on an archived session (i.e. dibas.YYYYMMDD/ instead of dibas/), the date AND session must be specified.

'''python
>>> python packet_information.py -s AGBT18A_999_53 -o 20180503
Analyzing NETBUFST for blc0*
Analyzing NETBUFST for blc2*
Analyzing NDROP for blc0*
Analyzing NDROP for blc2*
Analyzing PKTIDX for blc0*
Analyzing PKTIDX for blc2*
'''

The program is not completely robust against errors. For example, if session names contain errors, then the program will crash or produce no results.

The program is very robust and automated if the command line args are specified correctly.

If/when more compute nodes are added at GB, alter line 36 as necessary.

'''python
TOTAL_COMPUTE_NODES = ['00', '01', '02', '03', '04', '05', '06', '07', '10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37']
'''
