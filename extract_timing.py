import json
import csv

def read_json(filename):
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    return json.load(f)

def save_csv(filename, tl, file_type, field_names, contents):
  with open(f"tests/integration_test_files/{filename}_{tl}_{file_type}.csv", 'w',newline='') as f:    
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(contents)

for filename in ['complex_1', 'cycles_1']:
  data = read_json(filename)
  for version in data['study']['versions']:
    for design in version['studyDesigns']:
      encounter_map = {}
      epoch_map = {}
      for encounter in design["encounters"]:
        encounter_map[encounter['id']] = encounter['name']
      #print(f"ENCOUNTER_MAP: {encounter_map}")
      for epoch in design["epochs"]:
        epoch_map[epoch['id']] = epoch['name']
      for tl in design["scheduleTimelines"]:

        instance_map = {}
        for instance in tl['instances']: 
          instance_map[instance['id']] = instance['id'].replace("ScheduledActivityInstance", "INSTANCE")

        instances = []
        for instance in tl['instances']: 
          instance_map[instance['id']] = instance['id'].replace("ScheduledActivityInstance", "INSTANCE")
          encounter = ''
          if 'encounterId' in instance:
            encounter = encounter_map[instance['encounterId']] if instance['encounterId'] in encounter_map else ''
          #print(f"ENCOUNTER: {encounter}")
          conditions_str = ""  
          if instance['instanceType'] == 'ScheduledDecisionInstance':
            conditions = []
            for condition in instance["conditionAssignments"]:
              conditions.append(f"{condition[0]}: {instance_map[condition[1]]}")
            conditions_str = ", ".join(conditions)
          record = {
            'name': instance_map[instance['id']],
            'description': '',
            'label': '',
            'type': instance['instanceType'],
            'default': instance_map[instance['defaultConditionId']] if instance['defaultConditionId'] in instance_map else '(EXIT)',
            'condition': conditions_str,
            'epoch': epoch_map[instance['epochId']] if instance['epochId'] in epoch_map else '',
            'encounter': encounter,
          }
          # "ScheduledDecisionInstance"
          instances.append(record)

        timings = []
        for instance in tl['instances']:          
          for timing in instance['timings']:
            record = {
              'name': timing['name'],
              'label': timing['label'],
              'description': timing['description'],
              'type': timing['type']['decode'],
              'relative': timing['relativeToFrom']['decode'],
              'from': instance_map[timing['relativeFromScheduledInstanceId']] if timing['relativeFromScheduledInstanceId'] in instance_map else '',
              'to': instance_map[timing['relativeToScheduledInstanceId']] if timing['relativeToScheduledInstanceId'] in instance_map else '',
              'window': timing['window'],
            }
            timings.append(record)
        tl_clean = tl['name'].replace(' ', '-').lower()
        save_csv(filename, tl_clean, 'timings', ['name','label','description','type','relative','from','to','window'], timings)
        save_csv(filename, tl_clean, 'instances', ['name','description','label','type','default','condition','epoch','encounter'], instances)