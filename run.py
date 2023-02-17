import os
import glob
from glob import glob
import shutil

# Set data paths
data_path = os.getenv('DATA','/data')
inputs_path = os.path.join(data_path, 'inputs')
ssps_path = os.path.join(inputs_path, 'ssps')
boundary_path = os.path.join(inputs_path, 'boundary')
outputs_path = os.path.join(data_path, 'outputs')
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path)
boundary_outputs_path = os.path.join(outputs_path, 'boundary')
if not os.path.exists(boundary_outputs_path):
    os.mkdir(boundary_outputs_path)

# Read environment variables
ssp = os.getenv('SSP')
year = os.getenv('YEAR')
location = os.getenv('LOCATION')
rainfall_mode = os.getenv('RAINFALL_MODE')
time_horizon = os.getenv('TIME_HORIZON')
rainfall_total = int(os.getenv('TOTAL_DEPTH'))
size = float(os.getenv('SIZE')) * 1000  # convert from km to m
duration = int(os.getenv('DURATION'))
post_event_duration = int(os.getenv('POST_EVENT_DURATION'))
return_period = int(os.getenv('RETURN_PERIOD'))
x = int(os.getenv('X'))
y = int(os.getenv('Y'))
open_boundaries = (os.getenv('OPEN_BOUNDARIES').lower() == 'true')
permeable_areas = os.getenv('PERMEABLE_AREAS')
roof_storage = float(os.getenv('ROOF_STORAGE'))
discharge_parameter = float(os.getenv('DISCHARGE'))
output_interval = int(os.getenv('OUTPUT_INTERVAL'))

# Locate the boundary file and move into the correct output folder
# Rename based on the location of the city of interest
boundary = glob(boundary_path + "/*.*", recursive = True)
src=boundary[0]
print('src:',src)
dst=os.path.join(boundary_outputs_path, location + '.gpkg')
print('dst:',dst)
shutil.copy(src,dst)

# Identify which of the SSP datasets is needed and move into the correct output folder
# Retain the file name containing the SSP and year
ssps = glob(ssps_path + "/" + ssp + "-" + year + "*.*",recursive = True)
print('ssp_data:',ssps)

# Create a list of all of the files in the folder
for i in range(0,len(ssps)):
    test = ssps[i]
    file_path = os.path.splitext(test)
    print('Filepath:',file_path)
    filename[i]=file_path[0].split("/")
    print('Filename:',filename[-1])

file =[]

# Identify which file in the list relates to the chosen year / SSP
for i in range(0,len(ssps)):
    if ssp in filename[i][-1]:
        if year in filename[i][-1]:
            file = ssps[i]

print('File:',file)

# Move that file into the correct folder.
src=file
print('src:',src)
dst = os.path.join(outputs_path, filename[-1] + '.zip')
print('dst:',dst)
shutil.copy(src,dst)

# Print all of the input parameters to an excel sheet to be read in later
with open(os.path.join(outputs_path,location + '-'+ ssp + '-' + year +'-parameters.csv'), 'w') as f:
    f.write('PARAMETER, VALUE\n')
    f.write('LOCATION, %s\n' %location)
    f.write('SSP, %s\n' %ssp)
    f.write('YEAR, %s\n' %year)
    f.write('RAINFALL_MODE, %s\n' %rainfall_mode)
    f.write('TIME_HORIZON, %s\n' %time_horizon)
    f.write('TOTAL_DEPTH, %s\n' %rainfall_total)
    f.write('SIZE, %s\n' %size)
    f.write('DURATION, %s\n' %duration)   
    f.write('POST_EVENT_DURATION, %s\n' %post_event_duration)
    f.write('RETURN_PERIOD, %s\n' %return_period)
    f.write('X, %s\n' %x)
    f.write('Y, %s\n' %y)
    f.write('OPEN_BOUNDARIES, %s\n' %open_boundaries)
    f.write('PERMEABLE_AREAS, %s\n' %permeable_areas)
    f.write('ROOF_STORAGE, %s\n' %roof_storage)
    f.write('DISCHARGE, %s\n' %discharge_parameter)
    f.write('OUTPUT_INTERVAL, %s\n' %output_interval)
