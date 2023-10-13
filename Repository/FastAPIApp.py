from fastapi import FastAPI, Path
import uvicorn
import json
from starlette.responses import JSONResponse

from Repository.SQLiteConnection import SQLiteConnection


class FastAPIApp:
    def __init__(self, database: SQLiteConnection):
        self.database = database
        self.app = FastAPI()

        @self.app.get('/')
        async def get_home():
            return {'all': 'ok'}

        @self.app.get('/categories')
        async def get_categories():
            categories = self.database.get_categories()
            data = {"message": categories, "status": "success"}
            return JSONResponse(content=data)

        @self.app.get('/categories/{category_id}/services')
        async def get_category_services(category_id: int = Path(..., title="Category ID")):
            services = self.database.get_services_by_category(category_id)
            data = {"message": services, "status": "success"}
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

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
