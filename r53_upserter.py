import os
import boto3
import urllib.request
import time

MANDATORY_ENV_VARS = [
  'AWS_ACCESS_KEY_ID',
  'AWS_SECRET_ACCESS_KEY',
  'A_RECORD'
  ]

if 'INTERVAL' in os.environ:
  INTERVAL = os.environ['INTERVAL']
else:
  INTERVAL = 900

if 'IP_URL' in os.environ:
  IP_URL = os.environ['IP_URL']
else:
  IP_URL = 'http://icanhazip.com'

A_RECORD = os.environ["A_RECORD"]

for var in MANDATORY_ENV_VARS:
  if var not in os.environ:
    raise EnvironmentError("{} not set, exiting.".format(var))

def poll_result(change_id):
  start_time = time.time()
  r53 = boto3.client('route53')
  result = r53.get_change(Id=change_id)['ChangeInfo']
  while result['Status'] == 'PENDING':
    if time.time() - start_time > INTERVAL:
      raise Exception('Timeout error!')
    time.sleep(5)
    result = r53.get_change(Id=change_id)['ChangeInfo']
    print(".", end="", flush=True)
  print()
  duration = time.time() - start_time
  return [result['Status'], int(duration)]

def upsert_record():
  r53 = boto3.client('route53')
  return r53.change_resource_record_sets(
    ChangeBatch=generate_change_batch(),
    HostedZoneId=get_record_zone_id()
  )['ChangeInfo']

def generate_change_batch():
  batch = {
    'Changes': [
      {
        'Action': 'UPSERT',
        'ResourceRecordSet': {
          'Name': A_RECORD,
          'ResourceRecords': [
            {
              'Value': get_ip(IP_URL),
            },
          ],
          'TTL': 60,
          'Type': 'A',
        },
      },
    ]
  }
  return batch

def get_ip(url):
  try:
    LOCAL_IP = urllib.request.urlopen(url).read().strip().decode()
    print("Local IP is \"{}\".".format(LOCAL_IP))
    return LOCAL_IP
  except Exception as e:
    print("Error {0} on {1}".format(e, url))
    quit()

def get_record_zone_id(): # matches zone to A_RECORD, returns ID
  for zone in get_hosted_zones():
    if zone["Name"].rstrip('.') in A_RECORD:
      return zone['Id'].split('/')[2]
  raise Exception("No zone found that matches {}".format(record))

def get_caller_id():
  sts = boto3.client('sts')
  return sts.get_caller_identity()

def get_hosted_zones():
  r53 = boto3.client('route53')
  return r53.list_hosted_zones()['HostedZones']

def main():
  # print(get_caller_id())
  while True:
    print("{} - Updating record \"{}\"...".format(time.strftime("%H:%M:%S", time.localtime()), A_RECORD))
    change_id = upsert_record()['Id'].split('/')[2]
    result = poll_result(change_id)
    print("Status: {0}, Duration: {1} seconds.".format(result[0], result[1]))
    print("Next cycle in {} seconds...".format(INTERVAL-result[1]))
    time.sleep(INTERVAL-result[1])

if __name__ == "__main__":
  main()
