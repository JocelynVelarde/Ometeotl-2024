import pickle



#["Grassland temp","evapotranspiration","SOil 5","Soil 15","Soil 50","EMition m14","Landsurface temp day","landsurface temp night"],
#[first 5 are api, last 3 appeears nasa]



from env import creds
import datetime as dt
import meteomatics.api as api
import random

username = creds.username
password = creds.password
now = dt.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
startdate_ts = now
enddate_ts = dt.datetime.utcnow()
interval_ts = dt.timedelta(hours=1)
coordinates_ts = [(25.25863754474608, -99.68200619248428)]
parameters_ts =['grass_land_temperature_sum:C',
                  'evapotranspiration_24h:mm', 
                  'soil_moisture_index_-5cm:idx',
                    'soil_moisture_index_-15cm:idx',
                    'soil_moisture_index_-50cm:idx']
print("Array Agricultural Parameters:")
try:
    df = api.query_time_series(coordinates_ts, startdate_ts, enddate_ts, interval_ts,
                                  parameters_ts, username, password)
    if not df.empty:
        data_array = df.values.tolist()
        insert_value = data_array[-1]
        print("Latest entry:", insert_value)
        insert_value.append(random.uniform(0.0,1.0))
        insert_value.append(random.uniform(0.0,320.0))
        insert_value.append(random.uniform(0.0,320.0))
        print(insert_value)
        load_model = pickle.load(open("Modelo_Pred_LeafWetness.pkl","rb"))
        topred_array= [insert_value]

        result = load_model.predict(topred_array)

        print(result)
    else:
        print("No data retrieved Error.")

except Exception as e:
    print("Failed, the exception is {}".format(e))