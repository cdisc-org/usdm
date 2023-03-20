import os
import sys
from service.service import Service
import json

def file_read(filename):
  f = open('source_data/%s.json' % (filename))
  return json.load(f)

if __name__ == "__main__":
  
  endpoint = sys.argv[1]
  filename = sys.argv[2]
  service = Service(endpoint)
  
  data = file_read(filename)
  service.post("studyDefinitions", json.dumps(data))
