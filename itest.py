import pandas as pd
import numpy as np
import json
import sys, getopt

##Don't forget to implement debug routine
##Apply switch cases.
##Try to make columner data dynamic instead of passing it in as literals.

OBTAIN_DEPARTMENTS = 'false'
OBTAIN_APPS_PER_DEPARTMENT = 'false'
OBTAIN_CPU_RAM_PER_DEPARTMENT = 'false'
OBTAIN_CPU_RAM_PER_APPLICATION = 'false'
OBTAIN_CPU_RAM_PER_DATACENTER = 'false'
OBTAIN_HARDWARE_GROWTH_AND_DECREASE = 'false'

pd.set_option('display.max_rows', 500)
worksheet = pd.read_excel("hardware.xlsx")
applications = np.unique(worksheet["Application"].values).tolist()
applications = map(str,applications)
departments = np.unique(worksheet["Group"].values).tolist()
departments = map(str,departments)
data_centers = np.unique(worksheet["Site"].values).tolist()
data_centers = map(str,data_centers)
cpu_num_of_cores = np.unique(worksheet["CPU cores"].values).tolist()
ram_sizes = np.unique(worksheet["RAM (MB)"].values).tolist()
Engineering_Hardware_Growth = [10, 25, 40]
Sales_Hardware_Decrease = [80, 100]

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
    number_of_memory = (worksheet_dept["RAM (MB)"].values).tolist()
    cpu_and_ram_per_department.update({group:[len(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_department

def num_of_cpu_and_ram_per_application():
  global cpu_and_ram_per_application
  cpu_and_ram_per_application = {}
  for app in applications:
    worksheet_app = worksheet[worksheet["Application"]==app]
    number_of_cpus = (worksheet_app["CPU cores"].values).tolist()
    number_of_memory = (worksheet_app["RAM (MB)"].values).tolist()
    cpu_and_ram_per_application.update({app:[len(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_application

def num_of_cpu_and_ram_per_datacenter():
  global cpu_and_ram_per_datacenter
  cpu_and_ram_per_datacenter = {}
  for dc in data_centers:
    worksheet_dc = worksheet[worksheet["Site"]==dc]
    number_of_cpus = (worksheet_dc["CPU cores"].values).tolist()
    number_of_memory = (worksheet_dc["RAM (MB)"].values).tolist()
    cpu_and_ram_per_datacenter.update({dc:[len(number_of_cpus),len(number_of_memory)]})
  return cpu_and_ram_per_datacenter

def Hardware_Growth_and_Decrease():
  num_of_cpu_and_ram_per_department()
  for growth in Engineering_Hardware_Growth:
    each_year_cpu_growth = (cpu_and_ram_per_department['Engineering'][0]+((cpu_and_ram_per_department['Engineering'][0])*(float(growth)/100)))
    each_year_ram_growth = (cpu_and_ram_per_department['Engineering'][1]+((cpu_and_ram_per_department['Engineering'][1])*(float(growth)/100)))
    cpu_and_ram_per_department.update({'Engineering':[each_year_cpu_growth, each_year_ram_growth]})
  for decrease in Sales_Hardware_Decrease:
    each_year_cpu_decrease = (cpu_and_ram_per_department['Sales'][0]-((cpu_and_ram_per_department['Sales'][0])*(float(decrease)/100)))
    each_year_ram_decrease = (cpu_and_ram_per_department['Sales'][1]-((cpu_and_ram_per_department['Sales'][1])*(float(decrease)/100)))
    cpu_and_ram_per_department.update({'Sales':[each_year_cpu_decrease, each_year_ram_decrease]})
  return cpu_and_ram_per_department

def usage():
  print("""usage: %s [-g|-a|-c|-r|-d|-h] [file|-]
  -g: generates a list of all dedpartments that have hardware hosted.
  -a: generates a list of all applications for each department.
  -c: calculates the number of CPUs and memory used by each department.
  -r: calculates the number of CPUs and memory used by each application.
  -d: calculates the number of CPUs and memory used by each data center.
  -h: calculates hardware growth and decrease in partiular departments for upcoming years."""%sys.argv[0])
  sys.exit(2)

###Start Switch cases from here....
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
  if opt == '-h': OBTAIN_HARDWARE_GROWTH_AND_DECREASE = 'true'

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

if OBTAIN_HARDWARE_GROWTH_AND_DECREASE == 'true':
  Hardware_Growth_and_Decrease()
  print "cpu Growth in Engineering Department after 3 years: "+str(int(cpu_and_ram_per_department['Engineering'][0]))
  print "ram Growth in Engineering Department after 3 years: "+str(int(cpu_and_ram_per_department['Engineering'][1]))
  print "cpu decrease in Sales Department after 2 years: "+str(int(cpu_and_ram_per_department['Sales'][0]))
  print "ram decrease in Engineering Department after 2 years: "+str(int(cpu_and_ram_per_department['Sales'][1]))


