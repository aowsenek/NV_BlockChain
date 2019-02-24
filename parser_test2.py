import mygeotab

api = mygeotab.API(username='anow6879@colorado.edu', password='>zhsLk|*ab6Y%hkX', database='NV_Dan')
api.authenticate()

#print(data)

class Vehicle:
	def __init__(self, id):
		data = api.get('Device')
		self.id = id
		self.name = data[0]["name"]
		self.CMVVIN = data[0]["vehicleIdentificationNumber"]
		self.licensePlate = data[0]["licensePlate"]
		trip_data = api.get('Trip')
		dist = 0
		hours = 0
		minutes = 0
		seconds = 0
		for n in trip_data:
			dist += n["distance"]
			seconds += (int(n["workDrivingDuration"][6:7])+int(n["workStopDuration"][6:7]))%60
			minutes += (int(n["workDrivingDuration"][3:4]) + int(n["workStopDuration"][3:4]))%60 + (int(n["workDrivingDuration"][6:7])+int(n["workStopDuration"][6:7]))/60
			hours += int(n["workDrivingDuration"][0:1]) + int(n["workStopDuration"][0:1]) + (int(n["workDrivingDuration"][3:4])+int(n["workStopDuration"][3:4]))/60
		self.odometer = 0
		self.engineHours = str(round(hours + minutes/60)) + ':' + str(round(minutes%60 + seconds/60)) + ':' + str(round(seconds%60))
		self.vehicleMiles = dist

dan_car = Vehicle("b1")
print("ID:",dan_car.id)
print("NAME:",dan_car.name)
print("VIN:",dan_car.CMVVIN)
print("LICENSE PLATE:",dan_car.licensePlate)
print("ODOMETER:",dan_car.odometer)
print("ENGINE HOURS:",dan_car.engineHours)
print("VEHICLE MILES:",dan_car.vehicleMiles)
