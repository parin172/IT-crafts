import pandas as pd
import numpy as np
import json

pd.set_option('display.max_rows', 500)
worksheet = pd.read_excel("hardware.xlsx")
departments = []
groups = np.unique(worksheet["Group"].values).tolist()
for group in groups:
  departments.append((json.dumps(group)).strip('"'))
print "list of all departments that have hosted applications: "+json.dumps(departments)

#print (worksheet[worksheet["Group"]==departments[0]].drop_duplicates(subset=["Group","Application"]))
for group in departments:
  Apps = (worksheet[worksheet["Group"]==group].drop_duplicates(subset=["Group","Application"])["Application"].values).tolist()
  Apps = map(str,Apps)
  print "Hosted Applications for "+group+" group are "+ json.dumps(Apps)
#print (worksheet.drop_duplicates(subset=["Group","Application"]))

#number = worksheet[['Group','CPU cores']]
for group in departments:
  worksheet1 = worksheet[worksheet["Group"]==group]
  number_of_cpus = (worksheet1["CPU cores"].values).tolist()
  number_of_memory = (worksheet1["RAM (MB)"].values).tolist()
  print "number of RAMs used by "+group+" department are "+str(len(number_of_cpus))
  print "number of CPUs used by "+group+" department are "+str(sum(number_of_cpus))

