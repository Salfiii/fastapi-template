#@TODO: Webservice entry point: https://fastapi.tiangolo.com/tutorial/bigger-applications/
import json
from fastapi import Depends, APIRouter
from app.configuration.getConfig import Config

# get the config file
configuration = Config()

# SET THE API-ID: DO NOT CHANGE THIS!
API_ID = configuration.API_ID
API_VERSION = configuration.API_VERSION

# fastAPI Instance
router = APIRouter()
# Logger
logger = configuration.logger


@router.get("/config/", tags=["config"])
def get_config():
    """
    Returns the configuration of the webservice
    """
    return configuration.configuration_dict


@router.get("/actuator/health", tags=["config"])
async def health() -> dict:
    """
    Actuator health check
    :return:
    """

    global_status = "UP"

    status_dict = {
        "status": global_status,
        "description": "Health",
        "details": {
            "Just another check": {
                "status": "UP",
                "description": "description"
            },
        }
    }

    return status_dict
