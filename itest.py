import pandas as pd
import numpy as np
import json

##Don't forget to implement debug routine
##Apply switch cases.
##Try to make columner data dynamic instead of passing it in as literals.

pd.set_option('display.max_rows', 500)
worksheet = pd.read_excel("hardware.xlsx")
departments = np.unique(worksheet["Group"].values).tolist()
departments = map(str,departments)
print "list of all departments that have hosted applications: "+json.dumps(departments)

applications = np.unique(worksheet["Application"].values).tolist()
print "list of all applications: "+json.dumps(applications)

data_centers = np.unique(worksheet["Site"].values).tolist()
print "list of all data centers: "+json.dumps(data_centers)
#for group in groups:
#  departments.append((json.dumps(group)).strip('"'))
#print "list of all departments that have hosted applications: "+json.dumps(departments)

#print (worksheet[worksheet["Group"]==departments[0]].drop_duplicates(subset=["Group","Application"]))
for group in departments:
  Apps = (worksheet[worksheet["Group"]==group].drop_duplicates(subset=["Group","Application"])["Application"].values).tolist()
  Apps = map(str,Apps)
  print "Hosted Applications for "+group+" department are "+ json.dumps(Apps)
#print (worksheet.drop_duplicates(subset=["Group","Application"]))

#number = worksheet[['Group','CPU cores']]
for group in departments:
  worksheet1 = worksheet[worksheet["Group"]==group]
  number_of_cpus = (worksheet1["CPU cores"].values).tolist()
  number_of_memory = (worksheet1["RAM (MB)"].values).tolist()
  print "number of RAMs used by "+group+" Department are "+str(len(number_of_memory))
  print "number of CPUs used by "+group+" Department are "+str(sum(number_of_cpus))

for app in applications:
  worksheet2 = worksheet[worksheet["Application"]==app]
  number_of_cpus = (worksheet2["CPU cores"].values).tolist() 
  number_of_memory = (worksheet2["RAM (MB)"].values).tolist()
  print "number of RAMs used by "+app+" Application are "+str(len(number_of_memory))
  print "number of CPUs used by "+app+" Application are "+str(sum(number_of_cpus))
  
for dc in data_centers:
  worksheet3 = worksheet[worksheet["Site"]==dc]
  number_of_cpus = (worksheet3["CPU cores"].values).tolist()
  number_of_memory = (worksheet3["RAM (MB)"].values).tolist()
  print "number of RAMs used by "+dc+" DataCenter are "+str(len(number_of_memory))
  print "number of CPUs used by "+dc+" DataCenter are "+str(sum(number_of_cpus)) 
