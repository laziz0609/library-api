from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def home_view():
    return {'message': 'ok'}
    