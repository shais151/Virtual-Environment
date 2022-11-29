import logging
import os

from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from myprojectname.core.weather import weather

logs_file = Path(Path().resolve(), "log.txt")
logs_file.touch(exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO"),
    handlers=[logging.FileHandler(logs_file), logging.StreamHandler()],
)

log = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

weather_api = weather()


@app.get("/")
async def root():
    log.info("gone to root")
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    log.info(f"loaded item {item_id}")
    return {"item_id": item_id}


@app.get("/weather")
async def get_weather(
    latitude: float = 51.5002,
    longitude: float = -0.120000124,
    options: str = "temperature_2m",
):
    log.info(
        f"Requested latitude: {latitude} and longitude: {longitude} with options {options}"
    )
    output = weather_api.get_weather(
        latitude=latitude, longitude=longitude, options=options
    )
    return {"weather": output}


@app.get("/html", response_class=HTMLResponse)
def html_output(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "data": ["hello", 1, False]},
    )


@app.get("/chart", response_class=HTMLResponse)
def chart_output(
    request: Request,
    latitude: float = 51.5002,
    longitude: float = -0.120000124,
    city="London",
    options: str = "temperature_2m",
    limit: int = 50,
):
    data = weather_api.get_weather(
        latitude=latitude, longitude=longitude, options=options
    )

    labels = data["hourly"]["time"][:limit]
    labels = ",".join(labels)

    temp_values = data["hourly"]["temperature_2m"][:limit]
    temp_values = str(temp_values)[1:-1]

    if len(options) > len("temperature_2m"):
        rain_values = data["hourly"]["rain"][:limit]
        rain_values = str(rain_values)[1:-1]
        return templates.TemplateResponse(
            "weather.html",
            {
                "request": request,
                "data": [data, labels, temp_values, rain_values],
                "city": [city.title(), latitude, longitude],
            },
        )

    return templates.TemplateResponse(
        "weather.html",
        {
            "request": request,
            "data": [data, labels, temp_values],
            "city": [city.title(), latitude, longitude],
        },
    )


@app.post("/weather_send")
async def weather_send(
    request: Request, city: str = Form(), rain: Optional[str] = Form(None)
):
    cities = {
        "berlin": [52.52, 13.41],
        "london": [51.51, -0.13],
        "paris": [48.8566, 2.3522],
        "new_york": [40.71, -74.01],
    }
    options = "temperature_2m"
    if rain:
        options += ",rain"
    if city in cities:
        return chart_output(
            request=request,
            latitude=cities[city][0],
            longitude=cities[city][1],
            options=options,
            city=city.title(),
        )
    return chart_output(request=request, options=options, city=city.title())
