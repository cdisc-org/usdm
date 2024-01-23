import json
import csv

def read_json(filename):
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    return json.load(f)

def save_csv(filename, tl, file_type, field_names, contents):
  with open(f"tests/integration_test_files/{filename}_{tl}_{file_type}.csv", 'w',newline='') as f:    
    if field_names:
      writer = csv.DictWriter(f, fieldnames=field_names)
      writer.writeheader()
      writer.writerows(contents)
    else:
      writer = csv.writer(f)
      writer.writerows(contents)

to_from_map = {
  'Start to Start': 'S2S',
  'Start to End': 'S2E',
  'End to Start': 'E2S',
  'End to End': 'E2E'
}      

timing_type_map = {
  'Before': 'BEFORE',
  'After': 'AFTER',
  'Fixed Reference': 'FIXED'
}
          
for filename in ['complex_1']:
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

        instances = [[], [], [], [], [], [], [], []]
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
          instances[0].append(instance_map[instance['id']])
          instances[1].append('')
          instances[2].append('')
          instances[3].append('Activity' if instance['instanceType'] == 'ScheduledActivityInstance' else 'Decision')
          instances[4].append(instance_map[instance['defaultConditionId']] if instance['defaultConditionId'] in instance_map else '(EXIT)')
          instances[5].append(conditions_str)
          instances[6].append(epoch_map[instance['epochId']] if instance['epochId'] in epoch_map else '')
          instances[7].append(encounter)

        timings = []
        for instance in tl['instances']:    
          for timing in instance['timings']:
            the_type = timing_type_map[timing['type']['decode']]
            record = {
              'name': timing['name'],
              'description': timing['description'],
              'label': timing['label'],
              'type': the_type,
              'from': instance_map[timing['relativeFromScheduledInstanceId']] if timing['relativeFromScheduledInstanceId'] in instance_map else '',
              'to': instance_map[timing['relativeToScheduledInstanceId']] if timing['relativeToScheduledInstanceId'] in instance_map else '',
              'timingValue': timing['value'],
              'toFrom': to_from_map[timing['relativeToFrom']['decode']] if the_type != 'FIXED' else '',
              'window': timing['window'],
            }
            timings.append(record)
        tl_clean = tl['name'].replace(' ', '-').lower()
        save_csv(filename, tl_clean, 'timings', ['name','description','label','type','from','to','timingValue','toFrom','window'], timings)
        save_csv(filename, tl_clean, 'instances', [], instances)