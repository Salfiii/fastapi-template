# Python [Fastapi](https://fastapi.tiangolo.com/) Template Project with[poetry](https://python-poetry.org/) and [Docker](https://www.docker.com/101-tutorial)

## used frameworks/technologies:
- [Fastapi](https://fastapi.tiangolo.com/tutorial/)
- [Fastapi & Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/101-tutorial)
- [Helm](https://opensource.com/article/20/5/helm-charts)

## How to use the template

1. Clone the template (Or use the "Use this template" button in GitHub directly!)
    - ``git clone https://github.com/Salfiii/fastapi-template.git``
2. remove the ".git"-Folder from the local repository to delete the reference to the template project
3. create a new git repository locally
4. (install [poetry](https://python-poetry.org/docs/) if you want to run it locally)
5. Install [Docker](https://www.docker.com/products/docker-desktop/) or use a remote machine if you have one
6. change the project name from "fastapi-template" to something to your likings (you can also run it directly, if you like so)
   - in the parent Folder "fastapi-template"
   - in the [pyproject.toml](pyproject.toml)
   - in the [main.py](app/main.py)
   - in the [dockerfile](Dockerfile)
7. Run the dockerfile (you can change "fastapi-template" to whatever you like):
   - ``docker build -t fastapi-template . && docker run -it -p 50001:8080 fastapi-template``
   - If you want to remove the dockerfile after exiting the service automatically, add "--rm" before "-it"
   - You can change the port 50001 to whatever port you want to use on your host
8. Open http://localhost:50001 in your browser and you should see the OpenAPI docs.

## Documentation:

### file structure:

#### [app](app)
Contains the general python application.
- **[Configuration](app/configuration)**:
     - **[GetConfig.py](app/configuration/getConfig.py)**:
         - central [Singleton](https://en.wikipedia.org/wiki/Singleton_pattern) configuration class
         - read the config.ini and provide the values
     - **[config.ini](app/configuration/config.ini)**:
         - Central configuration elements/settings that are used in the code at x areas.
         - Do not make an ambient-specific (test/product) configuration here, this happens via the helmet chart.
- **[dal](app/dal)**:
     -If a database is used as a source or sink, this order includes the Connect class and, if necessary, the Orm models.
         - For relational databases: [SQLALCHEMY](https://www.sqlalchemy.org/)
         - for Mongodb: [Pymongo](https://pymongo.readthedocs.io/en/stable/)
- **[GUI](app/gui)**:
     - If the application contains a JavaScript GUI, it will be stored here.
- **[Routers](app/routers)**:
     - contains the definition of the Fastapi residual endpoints
     - **[config.py](app/routers/config.py)**
         - Contains the two standard points:
             - "/Actuator/Health":
                 - Kubernets Health Check Endpoint. This is used by Kubernetes to check the health status of the service.
                 - All mandatory converter should be checked here without which the app cannot work such as the associated database etc.
                 - The return format expected by K8S can be viewed in the end point itself.
             - "/config": delivers the configuration stored in the service, see "Getconfig.py". Passwords etc. are hidden.
     - **[benchmark.py](app/routers/benchmark.py)**
         - Test points for benchmark purposes. Should be deleted in the final app.
             - Attention: also remove the reference in [main.py](app/main.py) and under [tests](tests/test_routers/test_routers.py)!
- **[gunicorn_conf.py](app/gunicorn_conf.py)**
     - Configuration file for the WSGI HTTP Server [Gunicorn](https://gunicorn.org/)
     - The file is also included in the base image and can be theoretically removed.
- **[main.py](app/main.py)**
     - Entry point/Main in the application.
     - contains no end points/logic. The end points are defined in the routers.

#### [bin](bin)
Place for binaries such as CMD apps called from the Python code like Google Tesseract etc.
Often empty and can be removed.

#### [docs](docs)
Local location for documentation

#### [Helm](helm)
Application and ambient-specific (test/consumption) helmet files.
Contains the following 3 files that define the environment -specific values for test, consumption and prod.
Not all values have to be set, then the above defaults are used.
- [test_values.yaml](helm/test_values.yaml): Test environment -> ** This file includes an explanation of the different options **
- [Kons_values.yaml](helm/kons_values.yaml): Consolidation environment
- [Prod_values.yaml](helm/prod_values.yaml): Production environment

#### [tests](tests)
- Location for the tests which are created with the [pytest framework](https://docs.pytest.org/en/6.2.x/).
- Documentation for the creation of [tests for Fastapi](https://fastapi.tiangolo.com/tutorial/testing/)
-To carry out the tests: Right-click on the test folder -> "Run 'Pytests' in tests
- Test examples are included

#### [tmp] (tmp)
1. [in](tmp/in)
     -is used for the (temporary) storage of input files for the service, e.g. for file upload etc.
     - The path can be called up via the variable "in_folder" of the [Config class] (app/configuration/getConfig.py).
2. [out](tmp/out)
     - is used for the (temporary) storage of output files of the service.
     So if the service writes something, please put it here.
     - The path can be called up via the variable "Out_Folder" of the [Config-Class] (app/configuration/getConfig.py).
3. [Test](tmp/test)
     - Can be used to keep scripts etc. to try things out.

#### - additional files -

1. [Dockerfile](./Dockerfile)
     - Docker file that orchestrates the creation of the Docker container.
     - A documentation of the commands is in the file itself
2. [version.txt](version.txt)
     - Current version of the application. Is shown in the OpenAPI/Swagger Doc surface at the end and should be up at every change
to be counted.
3. [.gitlab-ci.yml](.gitlab-ci.yml)
     - Gitlab or the associated pipelines check whether such a file exists. If so, the one listed in it
       Reference to a CI/CD project used to build and provide the project.
4. [README.md](README.md)
     - Documentation (this!)
5. [gitignore.](.gitignore)
     - includes references to files/folders which are to be ignored by git.
     - Everything contained here is not versioned.
6. [pyproject.toml](pyproject.toml)
     - [Poetry Project File] (https://python-poetry.org/docs/pyproject/)
