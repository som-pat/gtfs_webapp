# uvicorn transit:app --reload
from fastapi import FastAPI, status, Request
from typing import List, Optional
import uvicorn
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from models import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


DATABASE_URL = "postgresql://gtadmin2:gtfsgudu1212@localhost/gtfs_del"
templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn



@app.get('/status')
async def check_status():
    return 'Hello World'

@app.get('/routes', response_model=List[Route], status_code=status.HTTP_200_OK)
async def get_routes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT route_id,route_short_name,route_long_name,route_type FROM route ORDER BY route_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Route(
                route_id=row[0],
                route_short_name=row[1],
                route_long_name=row[2],
                route_type=row[3],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes  # Ensure the list is returned

@app.get('/stops', response_model=List[Stops], status_code=status.HTTP_200_OK)
async def get_stops():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops ORDER BY stop_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Stops(
                stop_id=row[0],
                stop_name=row[1],
                stop_lat=row[2],
                stop_lon=row[3],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes 


@app.get('/trips', response_model=List[Trips], status_code=status.HTTP_200_OK)
async def get_trips():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT route_id, service_id, trip_id, shape_id, wheelchair_accessible, bikes_allowed FROM trips ORDER BY route_id,trip_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Trips(
                route_id =row[0],
                service_id = row[1],
                trip_id = row[2],
                shape_id =row[3],
                wheelchair_accessible = row[4],
                bikes_allowed = row[5],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes 


@app.get('/trip_shape', response_model=List[Shapes], status_code=status.HTTP_200_OK)
async def get_trip_shape():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled FROM shape")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Shapes(
                shape_id = row[0],
                shape_pt_lat = row[1],
                shape_pt_lon = row[2],
                shape_pt_sequence = row[3],
                shape_dist_traveled = row[4],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes

@app.get('/Stop_times', response_model=List[Stop_times], status_code=status.HTTP_200_OK)
async def get_stop_times():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled,timepoint FROM stop_times ORDER BY trip_id,stop_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Stop_times(
                trip_id = row[0],
                arrival_time = row[1],
                departure_time = row[2],
                stop_id =row[3],
                stop_sequence=row[4],
                pickup_type=row[5],
                drop_off_type=row[6],
                shape_dist_traveled=row[7],
                timepoint=row[8],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes

@app.get('/map_stops', response_class=HTMLResponse)
async def get_map_stops(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops")
    stops = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("maps.html", {"request": request, "stops": stops})



@app.post('/routes', status_code=status.HTTP_201_CREATED)
async def create_new_journey(new_journey:Route):
    return 'Hello World'


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
