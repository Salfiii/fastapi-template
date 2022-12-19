
from fastapi import FastAPI
from app.configuration.getConfig import Config
# routers
from app.routers import config, benchmark

# get the config file
configuration = Config()

API_ID = configuration.API_ID
API_VERSION = configuration.API_VERSION

# fastAPI Instance
app = FastAPI(
    title="Python FastAPI Template (API ID: "
    + str(API_ID) + ")", docs_url="/", version=configuration.API_VERSION
)


# include the routers
app.include_router(config.router)
app.include_router(benchmark.router)


# needed to start the application locally for development/debugging purpose. Will never be called on K8s.
if configuration.is_local:
    import uvicorn
    if __name__ == '__main__':
        # if run locally, the port might already be in use, just use another one then.
        uvicorn.run(app, host='127.0.0.1', port=8002)
