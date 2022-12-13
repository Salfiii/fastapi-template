import datetime
from asyncio import sleep
from uuid import uuid4

from fastapi import Depends, APIRouter, Body
from fastapi import BackgroundTasks
from app.configuration.getConfig import Config
from app.model.BenchmarkModel import Benchmark

# get the config file
configuration = Config()

# SET THE API-ID: DO NOT CHANGE THIS!
API_ID = configuration.API_ID
API_VERSION = configuration.API_VERSION

# fastAPI Instance
router = APIRouter()

# Logger
logger = configuration.logger


@router.get("/benchmark/hi", tags=["benchmark"])
async def plaintext_hi():
    """
    Returns the configuration of the webservice
    """
    return "Hi!"


@router.get("/benchmark/json", tags=["benchmark"])
async def json_response():
    """
    Returns the configuration of the webservice
    """
    return {"Hello": "World", "Foo": "Bar", "Num": 1, "String": "ABC"}


@router.post("/benchmark/json/post_and_return_modified", tags=["benchmark"], response_model=Benchmark)
async def post_and_return_modified(data: Benchmark = Body(None)):
    """
    Uses the same Model for Input & Output, usually you should use two.
    :param data:
    :return:
    """
    data.number = data.number + 1
    data.name = "APPENDED_START_" + data.name + "_APPENDED_END"
    data.another_class.nested_name = "APPENDED_START_" + data.another_class.nested_name + "_APPENDED_END"
    return data


async def wait_for_seconds(seconds: int, uuid_: str ):
    print(uuid_ + ": sleeping for " + str(seconds) + " seconds")
    await sleep(seconds)
    print(uuid_ + ": finished sleeping")


@router.post("/benchmark/backgroundtask/immediate_response", tags=["benchmark"])
async def backgroundtask_immediate_response(seconds_to_wait_on_server_side: int = 5,
                                            backgroundtasks: BackgroundTasks = BackgroundTasks()):
    """

    :param seconds_to_wait_on_server_side:
    :return:
    """
    uuid_: str = str(uuid4())
    received = datetime.datetime.now()
    backgroundtasks.add_task(wait_for_seconds, seconds_to_wait_on_server_side, uuid_)
    response = datetime.datetime.now()
    timedelta = response - received
    return {
        "uuid": uuid_,
        "received": received.isoformat(),
        "response": response.isoformat(),
        "seconds_to_wait_on_server_side": seconds_to_wait_on_server_side,
        "timedelta": timedelta.microseconds
        }
