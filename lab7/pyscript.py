# create db
# psql -d template1
import psycopg2
import geopy
from geopy.geocoders import Nominatim
# https://stackabuse.com/working-with-postgresql-in-python/
con = psycopg2.connect(database="dvdrental", user="postgres",
                       password="123456", host="127.0.0.1", port="5433")

print("Database opened successfully")
cur = con.cursor()
cur.execute("SELECT retrieve_address();")
rows = cur.fetchall()
geolocator = Nominatim(user_agent="dvdrental")
cur.execute("ALTER TABLE public.address ADD COLUMN IF NOT EXISTS latitude double precision;")
cur.execute("ALTER TABLE public.address ADD COLUMN IF NOT EXISTS longitude double precision;")
con.commit();
print("got it")
for i in range(len(rows)):
	location = geolocator.geocode(rows[i][0])
	if location == None:
		print("(0, 0)")
		cur.execute("UPDATE address SET latitude = 0, longitude = 0 WHERE address = '"+ rows[i][0] +"';")
		continue
	print((location.latitude, location.longitude))
	cur.execute("UPDATE address SET latitude = " + str(location.latitude) + ", longitude = " + str(location.longitude) + " WHERE address = '"+ rows[i][0] +"';")
	con.commit()	


















con.close()
