# Author : Mehdi CHERIFI
# Note : Please you must create a folder named "Golden_Config" before running the script

from genie.testbed import load

testbed=load('connex.yml')
for device in testbed.devices:
   testbed.devices[device].connect(log_stdout=False)
   pre_conf=testbed.devices[device].parse('show running-config')
   f=open("Golden_Config/golden_conf_"+str(device)+".txt", 'wt')
   print(pre_conf, file=f)
   f.close()


