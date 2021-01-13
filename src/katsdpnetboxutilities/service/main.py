from fastapi.responses import PlainTextResponse
from functools import lru_cache

from fastapi import Depends, FastAPI
from pydantic import BaseSettings

from katsdpnetboxutilities.system.device import host_report


class Settings(BaseSettings):
    """Application settings."""

    netbox_token: str
    netbox_url: str
    cache_path: str = "/tmp/cache"
    cache_age: int = 600
    output_path: str = "/tmp/netboxutils"
    verbose: bool = False
    debug: bool = False
    device_info_url: str

    class Config:
        # Load values from an '.env' file.
        env_file = ".env"


settings = Settings()

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hostreport/{hostname}/index.rst", response_class=PlainTextResponse)
async def hostreport_get(hostname: str, settings: Settings = Depends(get_settings)):
    return host_report(hostname, settings )

@app.post("/hostreport/{hostname}/index.rst")
async def hostreport_post(hostname: str):
    return {"hostname": hostname}
