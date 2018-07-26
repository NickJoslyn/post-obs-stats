# post-obs-stats
Display packet statistics following a Breakthrough Listen observation

After running reduce on a Breakthrough Listen Green Bank Observatory observation, run this program to get information regarding:
* The maximum location in memory ring buffer in which files were written to disk (NETBUFST)
* The average percentage of packets dropped (NDROP)
* The average percentage of blocks dropped (PKTIDX)

The program is not yet fully automated. After discussion with Emilio/Howard/Matt, the best course forward for ease of use will be discussed.

Currently to run:
* Go to a storage node (probably not bls1)
* Specify the number of banks (i.e. 3 for X band)
* Can specify the number of nodes (but that's unlikely to change from 8)
* Change the session number to desired (i.e. AGBT18A_999_77)

The program cannot handle offset banks (blctl start{1..3}{0..7}), but that will be able to be accomplished with the active hosts trigger depending on how we move forward with automation.
