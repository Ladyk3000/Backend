from fastapi import FastAPI, Query
import uvicorn
import json

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from Repository.BranchManager import BranchManager
from Repository.PathFinder import PathFinder
from Repository.SQLiteConnection import SQLiteConnection


class FastAPIApp:
    def __init__(self, branch_manager: BranchManager, database: SQLiteConnection):
        self.pathfinder = PathFinder()
        self.branch_manager = branch_manager
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
            offices_for_maps = self.database.get_offices_for_maps(longitude_min=longitude_min,
                                                                  latitude_min=latitude_min,
                                                                  longitude_max=longitude_max,
                                                                  latitude_max=latitude_max)
            data = {"message": offices_for_maps, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/atms-for-maps')
        async def get_atms_for_maps(
                longitude_min: float = Query(..., description="Minimum longitude"),
                latitude_min: float = Query(..., description="Minimum latitude"),
                longitude_max: float = Query(..., description="Maximum longitude"),
                latitude_max: float = Query(..., description="Maximum latitude")
        ):
            atms_for_maps = self.database.get_atms_for_maps(longitude_min=longitude_min,
                                                            latitude_min=latitude_min,
                                                            longitude_max=longitude_max,
                                                            latitude_max=latitude_max)
            data = {"message": atms_for_maps, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/categories')
        async def get_categories():
            categories = self.database.get_categories()
            data = {"message": categories, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/subcategories')
        async def get_subcategories(category_id: int = Query(..., title="Category ID")):
            subcategories = self.database.get_subcategories(category_id)
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

        @self.app.get('/office-info')
        async def get_office_info(
                office_id: int = Query(..., description="Office ID"),
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            office_info = self.database.get_office_info(office_id=office_id,
                                                        latitude=latitude,
                                                        longitude=longitude)
            data = {"message": office_info, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/atm-info')
        async def get_atm_info(
                atm_id: int = Query(..., description="ATM ID"),
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            office_info = self.database.get_atm_info(atm_id=atm_id,
                                                     latitude=latitude,
                                                     longitude=longitude)
            data = {"message": office_info, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-suit-office')
        async def get_suitable_office(
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            office = self.database.get_best_office(longitude=longitude,
                                                   latitude=latitude)
            data = {"message": office, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-near-offices')
        async def get_near_offices(
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            office = self.database.get_best_office(longitude=longitude,
                                                   latitude=latitude,
                                                   k=10)
            data = {"message": office, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-suit-atm')
        async def get_suitable_atm(
                longitude: float = Query(..., description="Longitude"),
                latitude: float = Query(..., description="Latitude")
        ):
            atm = self.database.get_best_atm(longitude=longitude,
                                             latitude=latitude)
            data = {"message": atm, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-days')
        async def get_days_for_reservation(office_id: int = Query(..., description="Office ID")):
            days = self.database.get_reservation_days(office_id)
            data = {"message": days, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/get-time-slots')
        async def get_time_slots(
                office_id: int = Query(..., description="Office ID"),
                reservation_date: str = Query(..., description="Reservation date"),
        ):
            time_slots = self.database.get_time_slots(office_id, reservation_date)
            data = {"message": time_slots, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/add-reservation')
        async def add_reservation(
                office_id: int = Query(..., description="Office ID"),
                reservation_date: str = Query(..., description="Reservation date"),
                reservation_time: str = Query(..., description="Reservation time"),
                service_name: str = Query(..., description="Service name"),
        ):
            reservation_id = self.database.add_reservation(office_id=office_id,
                                                           reservation_date=reservation_date,
                                                           reservation_time=reservation_time,
                                                           service_name=service_name)
            data = {"message": reservation_id, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/add-reservation-notify')
        async def add_reservation(
                reservation_id: int = Query(..., description="Office ID"),
                phone_number: str = Query(..., description="Service name"),
        ):
            self.database.add_reservation_notify(reservation_id=reservation_id,
                                                 phone_number=phone_number)
            data = {"status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/available-services')
        async def available_services(office_id: int = Query(..., description="Office ID")):
            services = self.branch_manager.get_available_services(office_id)
            data = {"message": services, "status": "success"}
            return JSONResponse(content=data)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
