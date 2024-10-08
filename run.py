import os
import glob
from glob import glob
import geopandas as gpd
import shutil
import math
from geojson import Polygon
from os.path import join, isdir, isfile
from datetime import datetime

def metadata_json(output_path, output_title, output_description, bbox, file_name):
    """
    Generate a metadata json file used to catalogue the outputs of the UDM model on DAFNI
    """

    # Create metadata file
    metadata = f"""{{
      "@context": ["metadata-v1"],
      "@type": "dcat:Dataset",
      "dct:language": "en",
      "dct:title": "{output_title}",
      "dct:description": "{output_description}",
      "dcat:keyword": [
        "UDM"
      ],
      "dct:subject": "Environment",
      "dct:license": {{
        "@type": "LicenseDocument",
        "@id": "https://creativecommons.org/licences/by/4.0/",
        "rdfs:label": null
      }},
      "dct:creator": [{{"@type": "foaf:Organization"}}],
      "dcat:contactPoint": {{
        "@type": "vcard:Organization",
        "vcard:fn": "DAFNI",
        "vcard:hasEmail": "support@dafni.ac.uk"
      }},
      "dct:created": "{datetime.now().isoformat()}Z",
      "dct:PeriodOfTime": {{
        "type": "dct:PeriodOfTime",
        "time:hasBeginning": null,
        "time:hasEnd": null
      }},
      "dafni_version_note": "created",
      "dct:spatial": {{
        "@type": "dct:Location",
        "rdfs:label": null
      }},
      "geojson": {bbox}
    }}
    """

    # write to file
    with open(join(output_path, '%s.json' % file_name), 'w') as f:
        f.write(metadata)
    return

def round_down(val, round_val):
    """Round a value down to the nearst value as set by the round val parameter"""
    return math.floor(val / round_val) * round_val

def round_up(val, round_val):
    """Round a value up to the nearst value as set by the round val parameter"""
    return math.ceil(val / round_val) * round_val

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
parameter_outputs_path = os.path.join(outputs_path, 'parameters')
if not os.path.exists(parameter_outputs_path):
    os.mkdir(parameter_outputs_path)
meta_outputs_path = os.path.join(outputs_path, 'metadata')
if not os.path.exists(meta_outputs_path):
    os.mkdir(meta_outputs_path)

# Read environment variables
ssp = os.getenv('SSP')
year = os.getenv('YEAR')
location = os.getenv('LOCATION')
rainfall_mode = os.getenv('RAINFALL_MODE')
rainfall_total = int(os.getenv('TOTAL_DEPTH'))
duration = int(os.getenv('DURATION'))
open_boundaries = (os.getenv('OPEN_BOUNDARIES'))
permeable_areas = os.getenv('PERMEABLE_AREAS')
roof_storage = float(os.getenv('ROOF_STORAGE'))
post_event_duration = int(os.getenv('POST_EVENT_DURATION'))
output_interval = int(os.getenv('OUTPUT_INTERVAL'))
size = os.getenv('SIZE')  # convert from km to m
x = os.getenv('X')
y = os.getenv('Y')


if size != None:
  size = float(size)*1000

if x != None:
  x = int(x)

if y != None:
  y = int(y)

print(size)

# Unused Parameters for this version of citycat - for further studies these can be incorporated
# baseline = (os.getenv('BASELINE'))
# time_horizon = os.getenv('TIME_HORIZON')
# discharge_parameter = float(os.getenv('DISCHARGE'))
# return_period = int(os.getenv('RETURN_PERIOD'))

# Locate the boundary file and move into the correct output folder
# Rename based on the location of the city of interest
boundary = glob(boundary_path + "/*.*", recursive = True)
src=boundary[0]
#print('src:',src)
dst=os.path.join(boundary_outputs_path, location + '.gpkg')
#print('dst:',dst)
shutil.copy(src,dst)

#print('Baseline:',baseline)

if ssp != "baseline" :
  # Identify which of the SSP datasets is needed and move into the correct output folder
  # Retain the file name containing the SSP and year
  ssps = glob(ssps_path + "/*.*",recursive = True)
  print('ssp_data:',ssps)

  filename=[]
  filename=['xx' for n in range(len(ssps))]
  #print('filename:',filename)

  # Create a list of all of the files in the folder
  for i in range(0,len(ssps)):
      test = ssps[i]
      file_path = os.path.splitext(test)
      #print('Filepath:',file_path)
      filename[i]=file_path[0].split("/")
      #print('Filename:',filename[i])

  file =[]

  # Identify which file in the list relates to the chosen year / SSP
  for i in range(0,len(ssps)):
      if ssp in filename[i][-1]:
          if year in filename[i][-1]:
              file = ssps[i]
              dst = os.path.join(outputs_path, filename[i][-1] + '.zip')

  #print('File:',file)

  # Move that file into the correct folder.
  src=file
  #print('src:',src)
  #print('dst:',dst)
  shutil.copy(src,dst)

# Print all of the input parameters to an excel sheet to be read in later
with open(os.path.join(parameter_outputs_path,location + '-'+ ssp + '-' + year +'-parameters.csv'), 'w') as f:
    f.write('PARAMETER,VALUE\n')
    f.write('LOCATION,%s\n' %location)
    f.write('SSP,%s\n' %ssp)
    f.write('YEAR,%s\n' %year)
    f.write('RAINFALL_MODE,%s\n' %rainfall_mode)  
    f.write('TOTAL_DEPTH,%s\n' %rainfall_total)
    f.write('DURATION,%s\n' %duration) 
    f.write('OPEN_BOUNDARIES,%s\n' %open_boundaries)
    f.write('PERMEABLE_AREAS,%s\n' %permeable_areas)
    f.write('ROOF_STORAGE,%s\n' %roof_storage)
    f.write('POST_EVENT_DURATION,%s\n' %post_event_duration)
    f.write('OUTPUT_INTERVAL,%s\n' %output_interval)
    f.write('SIZE,%s\n' %size)
    f.write('X,%s\n' %x)
    f.write('Y,%s\n' %y)
    #f.write('BASELINE, %s\n' %baseline)
    #f.write('TIME_HORIZON,%s\n' %time_horizon)
    #f.write('DISCHARGE,%s\n' %discharge_parameter)
    #f.write('RETURN_PERIOD,%s\n' %return_period)

boundary_1 = glob(boundary_path + "/*.*", recursive = True)
boundary = gpd.read_file(boundary_1[0])
bbox = boundary.bounds
extents = 1000
left = round_down(bbox.minx,extents)
bottom = round_down(bbox.miny,extents)
right = round_down(bbox.maxx,extents)
top = round_down(bbox.maxy,extents)
geojson = Polygon([[(left,top), (right,top), (right,bottom), (left,bottom)]])
    
SSP=ssp.upper()

# Creating the title for each model output
title_for_output_inputs = location + ' - ' + SSP + ' - ' + year + ' input_model'
title_for_output_ufg = location + ' - ' + SSP + ' - ' + year + ' urban fabric results'
title_for_output_green_areas = location + ' - ' + SSP + ' - ' + year + ' existing greenspaces'
title_for_output_buildings = location + ' - ' + SSP + ' - ' + year + ' existing buildings'
title_for_output_dtm = location + ' - ' + SSP + ' - ' + year + ' digital terrain data'
title_for_output_udm_citycat = location + ' - ' + SSP + ' - ' + year + ' new urban form'
title_for_output_citycat = location + ' - ' + SSP + ' - ' + year + ' CityCAT results'
title_for_output_impact = location + ' - ' + SSP + ' - ' + year + ' flood impact results'
title_for_output_visualisation = location + ' - ' + SSP + ' - ' + year + ' maps'

# Defining the description for each model output
description_for_output_inputs = 'This csv includes all the parameters used to run the Urban Flooding Impact Assessment Workflow for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'
description_for_output_ufg = 'Spatial footprints of the new urban form for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'. This data includes housing footprints, gardens and new roads.'
description_for_output_green_areas = 'Greenspace data for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +' based on the current (2017) urban form.'  
description_for_output_buildings = 'Building data for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +' based on the current (2017) urban form.'
description_for_output_dtm = 'The digital terrain data for ' + location + '.'
description_for_output_udm_citycat = 'This data presents the new urban form for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'. New urban developments, houses, gardens and roads are merged with the current urban form.'  
description_for_output_citycat = 'Outputs from the CityCAT model for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'
description_for_output_impact = 'This data shows the flood impact data generated by the CityCat flooding model for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'
description_for_output_visualisation = 'These maps and graphics show flood impact metrics for ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'  
   
# write a metadata file so outputs properly recorded on DAFNI
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_inputs, output_description=description_for_output_inputs, bbox=geojson, file_name='metadata_inputs')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_ufg, output_description=description_for_output_ufg, bbox=geojson, file_name='metadata_ufg')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_green_areas, output_description=description_for_output_green_areas, bbox=geojson, file_name='metadata_green_areas')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_buildings, output_description=description_for_output_buildings, bbox=geojson, file_name='metadata_buildings')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_dtm, output_description=description_for_output_dtm, bbox=geojson, file_name='metadata_dtm')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_udm_citycat, output_description=description_for_output_udm_citycat, bbox=geojson, file_name='metadata_udm_citycat')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_citycat, output_description=description_for_output_citycat, bbox=geojson, file_name='metadata_citycat')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_impact, output_description=description_for_output_impact, bbox=geojson, file_name='metadata_impact')
metadata_json(output_path=meta_outputs_path, output_title=title_for_output_visualisation, output_description=description_for_output_visualisation, bbox=geojson, file_name='metadata_visualisation')

# title_for_output = location + ' - ' + SSP + ' - ' + year

# description_for_output_inputs = 'This data shows all of the input data generated to run the CityCat flooding model for the chosen city of ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'
# description_for_output_FIM = 'This data shows the flood impact data generated by the CityCat flooding model for the chosen city of ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'
# description_for_output_Vis = 'These maps and graphics show flood impact metrics for the chosen city of ' + location + ' for the year ' + year + ' and social economic scenario ' + SSP +'.'  
   
# # write a metadata file so outputs properly recorded on DAFNI
# metadata_json(output_path=meta_outputs_path, output_title=title_for_output+'-inputs', output_description=description_for_output_inputs, bbox=geojson, file_name='metadata_citycat_inputs')

# # write a metadata file so inputs properly recorded on DAFNI - for ease of use adds onto info provided for outputs
# metadata_json(output_path=meta_outputs_path, output_title=title_for_output+'-output data', output_description=description_for_output_FIM, bbox=geojson, file_name='metadata_FIM_data')

# # write a metadata file so outputs properly recorded on DAFNI - for UDM AND CityCat outputs
# metadata_json(output_path=meta_outputs_path, output_title=title_for_output+'-output graphics', output_description=description_for_output_Vis, bbox=geojson, file_name='metadata_FIM_graphics')
