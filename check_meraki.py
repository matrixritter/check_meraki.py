import requests
import requests_cache
import argparse
import json
import time
import sys

# User input
parser = argparse.ArgumentParser()
parser.add_argument('--serial', help='Serial number of device from which you request status')
parser.add_argument('--org', help='The organization where the requested device is')
parser.add_argument('--api-key', help='Your Meraki API Key')
parser.add_argument('--warn', help='Warning interval in seconds for last report to Meraki cloud')
parser.add_argument('--crit', help='Critical interval in seconds for last report to Meraki cloud')
parser.add_argument('--full-dump', help='Dump out the JSON for all device statuse', action ='store_true')
parser.add_argument('--debug', help='Debug mode', action ='store_true')
parser.add_argument('--cache', help='Cache duraration in seconds', default=30)
parser.add_argument('--cache-path', help='Path to the sqlite DB used for caching', default='meraki_cache')
args = parser.parse_args()

if not args.full_dump == True:
    warn_in_sec = int(args.warn) 
    crit_in_sec = int(args.crit)


requests_cache.install_cache(args.cache_path, backend='sqlite', expire_after=args.cache)

# Variables
url = "https://api.meraki.com/api/v0/organizations/" + str(args.org) + "/deviceStatuses"
payload = {}
headers = {
  'Accept': '*/*',
  'X-Cisco-Meraki-API-Key': args.api_key
}

response = requests.get(url, headers=headers, data = payload)
json_load = json.loads(response.text)

if args.full_dump == True:
    print(json.dumps(json_load, indent=2))
    sys.exit()

for dic in json_load:
    if dic['serial'] == args.serial:
       if args.debug == True:
           print("JSON output from API for device", str(args.serial))
           print(json.dumps(dic, indent=2))

       # Workaround to prevent time_struct object with time_dst=-1 and to handle nanoseconds of different length
       time_string = dic['lastReportedAt'].partition('.')[0] + " UTC"
       meraki_time = time.strptime(time_string, "%Y-%m-%d %H:%M:%S %Z") 
       current_time = time.gmtime(None)
       time_difference = time.mktime(current_time) - time.mktime(meraki_time)

       if args.debug == True: 
           print("Local time struct object:", str(current_time))
           print("Meraki time struct object:", str(meraki_time))
           print("Last reported time in epoch:", str(time.mktime(meraki_time))) 
           print("Current time in epoch:", str(time.time()))
           print("Time difference in seconds: ", str(time_difference))

       if dic['status'] == "online" and time_difference > crit_in_sec:
           print("WARN, device", dic['name'],"reported to Meraki cloud",str(time_difference),"seconds ago")
           sys.exit(1)

       if dic['status'] == "offline":
           if time_difference > crit_in_sec:
               print("CRITICAL - device", dic['name'],"is not connected to Meraki cloud since",str(time_difference),"seconds")
               sys.exit(2)
           else:
               print("WARN - device", dic['name'],"is not connected to Meraki cloud since",str(time_difference),"seconds")
               sys.exit(1)

       print("OK - device", dic['name'], "is connected to Meraki cloud")
       sys.exit(0)
