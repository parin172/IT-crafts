import pandas as pd
import numpy as np
import json

##Don't forget to implement debug routine
##Apply switch cases.
##Try to make columner data dynamic instead of passing it in as literals.

pd.set_option('display.max_rows', 500)
worksheet = pd.read_excel("hardware.xlsx")
applications = np.unique(worksheet["Application"].values).tolist()
applications = map(str,applications)
departments = np.unique(worksheet["Group"].values).tolist()
departments = map(str,departments)
data_centers = np.unique(worksheet["Site"].values).tolist()
data_centers = map(str,data_centers
)
apps_per_department={}
cpu_and_ram_per_department={}
cpu_and_ram_per_application={}
cpu_and_ram_per_datacenter={}

def list_of_departments():
  return departments

def list_of_apps_per_department():
  for group in departments:
    Apps = (worksheet[worksheet["Group"]==group].drop_duplicates(subset=["Group","Application"])["Application"].values).tolist()
    Apps = map(str,Apps)
    apps_per_department.update({group:Apps})
  return apps_per_department

def num_of_cpu_and_ram_per_department():
  for group in departments:
    worksheet1 = worksheet[worksheet["Group"]==group]
    number_of_cpus = (worksheet1["CPU cores"].values).tolist()
    number_of_memory = (worksheet1["RAM (MB)"].values).tolist()
    cpu_and_ram_per_department.update({group:[sum(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_department

def num_of_cpu_and_ram_per_application():
  for app in applications:
    worksheet2 = worksheet[worksheet["Application"]==app]
    number_of_cpus = (worksheet2["CPU cores"].values).tolist()
    number_of_memory = (worksheet2["RAM (MB)"].values).tolist()
    cpu_and_ram_per_application.update({app:[sum(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_application

def num_of_cpu_and_ram_per_datacenter():
  for dc in data_centers:
    worksheet3 = worksheet[worksheet["Site"]==dc]
    number_of_cpus = (worksheet3["CPU cores"].values).tolist()
    number_of_memory = (worksheet3["RAM (MB)"].values).tolist()
    cpu_and_ram_per_datacenter.update({dc:[sum(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_datacenter

###Start Switch cases from here....

print "list of all departments that have hosted applications: %s " % str(list_of_departments())

list_of_apps_per_department()
for department in apps_per_department.keys():
  print "Application hosted by "+department+" department are: "+str(apps_per_department[department])

num_of_cpu_and_ram_per_department()
for department in cpu_and_ram_per_department.keys():
  print "Total number of CPUs and RAMs used by "+department+" department are "+str(cpu_and_ram_per_department[department])

num_of_cpu_and_ram_per_application()
for application in cpu_and_ram_per_application.keys():
  print "Total number of CPUs and RAMs used by "+application+" application are "+str(cpu_and_ram_per_application[application])

num_of_cpu_and_ram_per_datacenter()
print cpu_and_ram_per_datacenter
for datacenter in cpu_and_ram_per_datacenter.keys():
  print "Total number of CPUs and RAMs used by "+datacenter+" datacenter are "+str(cpu_and_ram_per_datacenter[datacenter])

#Engineering_Hardware_Growth = [10, 25, 40]
#for growth in Engineering_Hardware_Growth:
#  number_of_cpus = (worksheet1["CPU cores"].values).tolist()
#  cpu_each_year_growth = sum(number_of_cpus)+(sum(number_of_cpus)*(growth/100))
#  print "each "
