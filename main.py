from fastapi import FastAPI
import uvicorn
import json

app = FastAPI()


@app.get('/')
def get_home():
    return {'all': 'ok'}


@app.get('/offices')
def get_offices():
    with open('offices.txt', 'r', encoding='utf-8') as file:
        data = file.read()

    offices = json.loads(data)
    return offices


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
