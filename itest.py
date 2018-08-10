#!/usr/local/bin/python

import pandas as pd
import numpy as np
import sys, getopt
import collections

##Don't forget to implement debug routine
##Apply switch cases.
##Try to make columner data dynamic instead of passing it in as literals.

OBTAIN_DEPARTMENTS = 'false'
OBTAIN_APPS_PER_DEPARTMENT = 'false'
OBTAIN_CPU_RAM_PER_DEPARTMENT = 'false'
OBTAIN_CPU_RAM_PER_APPLICATION = 'false'
OBTAIN_CPU_RAM_PER_DATACENTER = 'false'
OBTAIN_HOSTING_COST_PER_DEPARTMENT = 'false'

pd.set_option('display.max_rows', 500)
worksheet = pd.read_excel("hardware.xlsx")
applications = np.unique(worksheet["Application"].values).tolist()
applications = map(str,applications)
departments = np.unique(worksheet["Group"].values).tolist()
departments = map(str,departments)
data_centers = np.unique(worksheet["Site"].values).tolist()
data_centers = map(str,data_centers)
cpu_num_of_cores = np.unique(worksheet["CPU cores"].values).tolist()
#ram_sizes_in_gig = ((worksheet["RAM (MB)"].values)/1024).tolist()
#unique_ram_sizes_in_gig = ((np.unique(worksheet["RAM (MB)"].values))/1024).tolist()
Engineering_Hardware_Growth = [10, 25, 40]
Sales_Hardware_Decrease = [80, 100, 0]
Change_in_Hardware_Requirements = ["Engineering", "Engineering Canada", "Sales"] 
#hosting_cost = {}
#yearly_hosting_cost = []
cost_for_department_over_years = {}

#assumption_for_instance_prizes in below dictionary are (0->t2.nano, 1->t2.mciro, 2->t2.small, 4->t2.medium, 8->t2.large, 16->m5.large, 24->m5.2xlarge, 32->m5.2xlarge, 64->m5.4xlarge)
instance_prices_per_hour = {0:0.0058, 1:0.0116, 2:0.023, 4:0.0464, 8:0.0928, 16:0.192, 24:0.384, 32:0.384, 64:0.768}

def hosting_cost_per_department():
  for group in departments:
    hosting_cost = {}
    yearly_hosting_cost = []
    group_worksheet = (worksheet[worksheet["Group"]==group])
    ram_sizes_in_gig = ((group_worksheet["RAM (MB)"].values)/1024).tolist()
    ram_counter = dict(collections.Counter(ram_sizes_in_gig))
#   here ram_counter defines size and number rams per size used by each department.

    if ( group == "Engineering" ) or (group == "Engineering Canada" ):
      for growth in Engineering_Hardware_Growth:
        for key in ram_counter.keys():
          ram_counter.update({key:(ram_counter[key]+ram_counter[key]*(float(growth)/100))})
        for key in ram_counter.keys():
          instance_cost = (ram_counter[key]*instance_prices_per_hour[key]*24*365)
          hosting_cost.update ({key:instance_cost})
        yearly_hosting_cost.append(sum(hosting_cost.values()))
      cost_for_department_over_years.update({group:yearly_hosting_cost}) 

    elif ( group == "Sales" ):
      for decrease in Sales_Hardware_Decrease:
        for key in ram_counter.keys():
          ram_counter.update({key:(ram_counter[key]-ram_counter[key]*(float(decrease)/100))})
        for key in ram_counter.keys():
          instance_cost = (ram_counter[key]*instance_prices_per_hour[key]*24*365)
          hosting_cost.update ({key:instance_cost})
        yearly_hosting_cost.append(sum(hosting_cost.values()))
        cost_for_department_over_years.update({group:yearly_hosting_cost}) 

    else:
      for price in range(3):
        for key in ram_counter.keys():
          instance_cost = (ram_counter[key]*instance_prices_per_hour[key]*24*365)
          hosting_cost.update ({key:instance_cost})
        yearly_hosting_cost.append(sum(hosting_cost.values()))
        cost_for_department_over_years.update({group:yearly_hosting_cost})
  return cost_for_department_over_years

def list_of_departments():
  return departments

def list_of_apps_per_department():
  global apps_per_department
  apps_per_department = {}
  for group in departments:
    Apps = (worksheet[worksheet["Group"]==group].drop_duplicates(subset=["Group","Application"])["Application"].values).tolist()
    Apps = map(str,Apps)
    apps_per_department.update({group:Apps})
  return apps_per_department

def num_of_cpu_and_ram_per_department():
  global cpu_and_ram_per_department
  cpu_and_ram_per_department = {}
  for group in departments:
    worksheet_dept = worksheet[worksheet["Group"]==group]
    number_of_cpus = (worksheet_dept["CPU cores"].values).tolist()
#    number_of_memory = (worksheet_dept["RAM (MB)"].values).tolist()
    cpu_and_ram_per_department.update({group:len(number_of_cpus)})
  return cpu_and_ram_per_department

def num_of_cpu_and_ram_per_application():
  global cpu_and_ram_per_application
  cpu_and_ram_per_application = {}
  for app in applications:
    worksheet_app = worksheet[worksheet["Application"]==app]
    number_of_cpus = (worksheet_app["CPU cores"].values).tolist()
#    number_of_memory = (worksheet_app["RAM (MB)"].values).tolist()
    cpu_and_ram_per_application.update({app:len(number_of_cpus)})
  return cpu_and_ram_per_application

def num_of_cpu_and_ram_per_datacenter():
  global cpu_and_ram_per_datacenter
  cpu_and_ram_per_datacenter = {}
  for dc in data_centers:
    worksheet_dc = worksheet[worksheet["Site"]==dc]
    number_of_cpus = (worksheet_dc["CPU cores"].values).tolist()
#    number_of_memory = (worksheet_dc["RAM (MB)"].values).tolist()
    cpu_and_ram_per_datacenter.update({dc:len(number_of_cpus)})
  return cpu_and_ram_per_datacenter

def usage():
  print("""usage: %s [-g|-a|-c|-r|-d|-h] [file|-]
  -g: generates a list of all dedpartments that have hardware hosted.
  -a: generates a list of all applications for each department.
  -c: calculates the number of CPUs and memory used by each department.
  -r: calculates the number of CPUs and memory used by each application.
  -d: calculates the number of CPUs and memory used by each data center.
  -h: calculates hardware hosting cost per department over the course of 3 years."""%sys.argv[0])
  sys.exit(2)

try:
  opts, args = getopt.getopt(sys.argv[1:],'gacrdh')
except getopt.error as msg:
  sys.stdout = sys.stderr
  print(msg)
  usage()

if len(sys.argv) == 1:
  usage()

for opt, arg in opts:
  if opt == '-g': OBTAIN_DEPARTMENTS = 'true'
  if opt == '-a': OBTAIN_APPS_PER_DEPARTMENT = 'true'
  if opt == '-c': OBTAIN_CPU_RAM_PER_DEPARTMENT = 'true'
  if opt == '-r': OBTAIN_CPU_RAM_PER_APPLICATION = 'true'
  if opt == '-d': OBTAIN_CPU_RAM_PER_DATACENTER = 'true'
  if opt == '-h': OBTAIN_HOSTING_COST_PER_DEPARTMENT = 'true'

if OBTAIN_DEPARTMENTS == 'true':
  print "list of all departments that have hosted applications: %s " % str(list_of_departments())

if OBTAIN_APPS_PER_DEPARTMENT == 'true':
  list_of_apps_per_department()
  for department in apps_per_department.keys():
    print "Applications hosted by "+department+" department are: "+str(apps_per_department[department])

if OBTAIN_CPU_RAM_PER_DEPARTMENT == 'true':
  num_of_cpu_and_ram_per_department()
  for department in cpu_and_ram_per_department.keys():
    print "Total number of CPUs and RAMs used by "+department+" department are "+str(cpu_and_ram_per_department[department])

if OBTAIN_CPU_RAM_PER_APPLICATION == 'true':
  num_of_cpu_and_ram_per_application()
  for application in cpu_and_ram_per_application.keys():
    print "Total number of CPUs and RAMs used by "+application+" application are "+str(cpu_and_ram_per_application[application])

if OBTAIN_CPU_RAM_PER_DATACENTER == 'true':
  num_of_cpu_and_ram_per_datacenter()
  for datacenter in cpu_and_ram_per_datacenter.keys():
    print "Total number of CPUs and RAMs used by "+datacenter+" datacenter are "+str(cpu_and_ram_per_datacenter[datacenter])

if OBTAIN_HOSTING_COST_PER_DEPARTMENT == 'true':
  hosting_cost_per_department()
  for department in cost_for_department_over_years.keys():
    print "Hosting cost for "+department+" department over the course of 3 years are :"+str(cost_for_department_over_years[department])
#  print "Hosting cost for each department over the course of 3 years: "+str(cost_for_department_over_years)

