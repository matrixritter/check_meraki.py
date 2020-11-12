# check_meraki.py

Meraki checkcommand script for classical monitoring systems like Nagios

## Use Case Description

This script allows to check if a Meraki device is connected to Meraki cloud and can be considered alive when last connection to cloud is within your defined thresholds.

## Installation

This script currently uses the following modules:

* requests
* requests_cache
* argparse
* json
* time
* sys (default)

Please check your local environment if this modules are globally available. As your monitoring process typically has it's own user and you can't switch to any virtual python environment without having some wrapper scripts, it's best to have them globally available. As this script is not using any bleeding edge features, any version should work.

To install this, just copy check_meraki.py to any directory which your monitoring system can access and allow execution:

`chmod +x ./check_meraki.py`

## Usage

Currently check_meraki.py expects all arguments given at startup:

```
python ./check_meraki.py --help
usage: check_meraki.py [-h] [--serial SERIAL] [--org ORG] [--api-key API_KEY] [--warn WARN] [--crit CRIT] [--full-dump] [--debug] [--cache CACHE] [--cache-path CACHE_PATH]

optional arguments:
  -h, --help               show this help message and exit
  --serial SERIAL          Serial number of device from which you request status
  --org ORG                The organization where the requested device is
  --api-key API_KEY        Your Meraki API Key
  --warn WARN              Warning interval in seconds for last report to Meraki cloud
  --crit CRIT              Critical interval in seconds for last report to Meraki cloud
  --full-dump              Dump out the JSON for all device statuse
  --debug                  Debug mode
  --cache CACHE            Cache duraration in seconds
  --cache-path CACHE_PATH  Path to the sqlite DB used for caching
```

The API Key is generated on Merakis dashboard, but the Org ID needs to be retrieved with a HTTP client like curl:

```
curl https://api.meraki.com/api/v0/organizations -L -H 'X-Cisco-Meraki-API-Key: <Your key>'
```

Then you get some JSON output, where you can pull the ID. The next thing would be a full dump of all devices to retrieve the serial number:

```
python ./check_meraki.py --full-dump --api-key <Your Key> --org <Org ID>
```

Finally this can be used to generate Nagios compatible output:

```
python ./check_meraki.py --serial <Device serial> --api-key <Your key> --org <Org ID> --warn 180 --crit 300
> OK - <Your device name> is connected to Meraki cloud
```

## Known issues

Script is currently accepting all arguments via CLI and don't read from any configuration file yet.

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Author(s)

This project was written and is maintained by the following individuals:

* Klaus Kruse <mail@klaus-kruse.de>
