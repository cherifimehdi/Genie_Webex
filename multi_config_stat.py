# Author : Mehdi CHERIFI

# Note : Please make sure to apply your access_token and room_id in the required emplacement

from genie.testbed import load
from genie.utils.diff import Diff
from genie.libs.parser.utils import get_parser_exclude
import ast
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

testbed=load('connex.yml')
for device in testbed.devices:
   testbed.devices[device].connect(log_stdout=False)


   # retrieve golden config for each router and transfer it from string dict into python dict
   D=open("Golden_Config/golden_conf_"+str(device)+".txt", 'r')
   data=D.read()
   pre_conf=ast.literal_eval(data)

   # retrieve the actual configuration for each router
   actual_conf=testbed.devices[device].api.get_running_config_dict()
   # apply the diff between the current config and the golden config
   diff=Diff(actual_conf, pre_conf)

   diff.findDiff()
   # save the diff in text file
   with open('change_'+str(device)+".txt", 'w') as f:
      print(diff, file=f)
      f.close()
   # open the saved file and verufy if it is empty and there is no space and new line
   f=open('change_'+str(device)+".txt", 'r')
   content=f.read()

   is_empty=content.isspace()

   # send message NO CHANGE to Webex room if the diff file is empty and then no change in configuration
   if is_empty==True:
      access_token = '<YOUR access_token HERE>'
      room_id = '<YOUR room_id HERE>'
      message = 'NO CHANGE in ' +str(device) +' !!!'
      url = 'https://webexapis.com/v1/messages'
      headers = {
          'Authorization': 'Bearer {}'.format(access_token),
          'Content-Type': 'application/json'
      }
      params = {'roomId': room_id, 'markdown':message}
      res = requests.post(url, headers=headers, json=params)

   # send the diff text file to Webex room to indicate the change in the configuration

   else:

      m = MultipartEncoder({'roomId': '<YOUR room_id HERE>',
                         'text': 'HERE THE CHANGE in '+ str(device) + ' !!!, WE WILL PROCEED FOR GOLDEN CONFIGURATION RESTORING',
                         'files': ('change_'+str(device)+".txt", open('change_'+str(device)+".txt", 'rb'),
                         'document/txt')})

      r = requests.post('https://webexapis.com/v1/messages', data=m,
                     headers={'Authorization': 'Bearer <YOUR access_token HERE>',
                     'Content-Type': m.content_type})

      # process for retrieving the golden config saved in disk0 file in the router in case of change
      testbed.devices[device].execute("configure replace disk0:startup-config force")

