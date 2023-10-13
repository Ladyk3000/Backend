from fastapi import FastAPI, Path, Query
import uvicorn
import json

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from Repository.PathFinder import PathFinder
from Repository.SQLiteConnection import SQLiteConnection


class FastAPIApp:
    def __init__(self, database: SQLiteConnection):
        self.pathfinder = PathFinder()
        self.database = database
        self.app = FastAPI()
        origins = ["*"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get('/')
        async def get_home():
            return {'all': 'ok'}

        @self.app.get('/offices-for-maps')
        async def get_offices_for_maps(
                longitude_min: float = Query(..., description="Minimum longitude"),
                latitude_min: float = Query(..., description="Minimum latitude"),
                longitude_max: float = Query(..., description="Maximum longitude"),
                latitude_max: float = Query(..., description="Maximum latitude")
        ):
            offices_for_maps = self.database.get_offices_for_maps(longitude_min,
                                                                  latitude_min,
                                                                  longitude_max,
                                                                  latitude_max)
            data = {"message": offices_for_maps, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/atms-for-maps')
        async def get_atms_for_maps(
                longitude_min: float = Query(..., description="Minimum longitude"),
                latitude_min: float = Query(..., description="Minimum latitude"),
                longitude_max: float = Query(..., description="Maximum longitude"),
                latitude_max: float = Query(..., description="Maximum latitude")
        ):
            atms_for_maps = self.database.get_atms_for_maps(longitude_min,
                                                            latitude_min,
                                                            longitude_max,
                                                            latitude_max)
            data = {"message": atms_for_maps, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/categories')
        async def get_categories():
            categories = self.database.get_categories()
            data = {"message": categories, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/categories/{category_id}/subcategories')
        async def get_subcategories(category_id: int = Path(..., title="Category ID")):
            subcategories = self.database.get_subcategories_by_category(category_id)
            data = {"message": subcategories, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/offices')
        async def get_offices():
            with open('Data/offices.txt', 'r', encoding='utf-8') as file:
                data = file.read()
            offices = json.loads(data)
            data = {"message": offices, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/atms')
        async def get_atms():
            with open('Data/atms.txt', 'r', encoding='utf-8') as file:
                data = file.read()
            atms = json.loads(data)
            data = {"message": atms, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-suit-office')
        async def get_suitable_office(
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            office = self.database.get_best_office(longitude, latitude)
            data = {"message": office, "status": "success"}
            return JSONResponse(content=data)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
