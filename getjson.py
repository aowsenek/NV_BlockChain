import json
import mygeotab

api = mygeotab.API(username='anow6879@colorado.edu', password='>zhsLk|*ab6Y%hkX', database='NV_Dan')
api.authenticate()

data = api.get('Trip', resultsLimit=10)
json_string = json.dumps(data, indent=4, sort_keys=True, default=str)
writeFile = open("data_file.json", "w")
writeFile.write(json_string)
writeFile.close()

print("It is done.")
