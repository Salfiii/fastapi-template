# Python [FastAPI](https://fastapi.tiangolo.com/) Template Project wie [poetry](https://python-poetry.org/)

## Tutorials zur Verwendeten Technologie:
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI & Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/101-tutorial)
- [Helm](https://opensource.com/article/20/5/helm-charts)
- 
## Dokumentation:

### Dateistruktur:

#### [app](app)
Enthält die eigenliche Python Applikation.
- **[configuration](app/configuration)**:
    - **_[getConfig.py](app/configuration/getConfig.py)_**:
        - Zentrale [Singleton](https://de.wikipedia.org/wiki/Singleton_(Entwurfsmuster)) Konfigurationsklasse
        - Liest die config.ini ein und stellt die Werte bereit
    - **_[config.ini](app/configuration/config.ini)_**:
        - Zentrale Konfigurationselemente/Einstellungen welche an x stellen im Code verwendet werden.
        - Hier keine Umgebungsspezifische (Test/Prod) Konfiguration vornehmen, dies geschieht über den Helm-Chart.
- **[dal](app/dal)**:
    - Falls eine Datenbank als Quelle oder Senke verwendet wird, beinhaltet dieser Order die Connect-Klasse und ggf. die ORM-Modelle.
        - Für relationale Datenbanken: [SQLAlchemy](https://www.sqlalchemy.org/)
        - Für MongoDB: [PyMongo](https://pymongo.readthedocs.io/en/stable/)
- **[gui](app/gui)**:
    - Falls die Applikation eine JavaScript GUI enthält wird diese hier abgelegt.
- **[routers](app/routers)**:
    - Enthält die Definition der FastAPI REST-Endpunkte
    - **_[config.py](app/routers/config.py)_**
        - enthält die beiden Standardenpunkte:
            - "/actuator/health": 
                - Kubernets Health Check Endpoint. Dieser wird von Kubernets verwendet um den Gesundheitszustand des Services zu prüfen.
                - Hier sollten alle zwingend notwendigen Umsysteme überprüft werden ohne welche die App nicht funktionieren kann wie z.B. die zugehörige Datenbank etc.
                - Das von K8s erwartete Return-Format ist im Endpunkt selbst einsehbar.
            - "/config": liefert die im service hinterlegte Konfiguration zurück, vgl. "getConfig.py". Passwörter etc. werden ausgeblendet.
    - **_[benchmark.py](app/routers/benchmark.py)_**
        - Testenpunkte für Benchmarkzwecke. Sollte in finaler App gelöscht werden.
            - ACHTUNG: auch Referenz in [main.py](app/main.py) und unter [tests](tests/test_routers/test_routers.py) entfernen!
- **_[gunicorn_conf.py](app/gunicorn_conf.py)_**
    - Konfigurationsdatei für den WSGI HTTP Server [Gunicorn](https://gunicorn.org/)
    - Die Datei ist ebenfalls im Base-Image enthalten und kann theoretisch entfern werden.
- **_[main.py](app/main.py)_**
    - Einstiegspunkt/Main in die Applikation.
    - Enthält keine Endpunkte/Logik. Die Endpunkte werden in den routers definiert.

#### [bin](bin)
Ablage von verwendeten Binaries wie z.B. CMD-Apps die aus dem Python Code aufgerufen werden wie Tesseract etc.
I.d.R. leer und kann entfernt werden.

#### [docs](docs)
Ablageort für Dokumentationen

#### [helm](helm)
Applikations- und Umgebungsspezifische (Test/Kons/Prod) HELM-Dateien.
Enthält folgende 3 Dateien welche die Umgebungsspezifischen Werte für test, kons und prod definieren.
Es müssen nicht alle Werte gesetzt sein, dann werden die o.g. Defaults verwendet.
- [test_values.yaml](helm/test_values.yaml): Testumgebung -> **Diese Datei beeinhaltet eine Erläuterung der verschiedenen Möglichkeiten**
- [kons_values.yaml](helm/kons_values.yaml): Konsolidierungsumgebung
- [prod_values.yaml](helm/prod_values.yaml): Produktionsumgebung

#### [tests](tests)
- Ablageort für die Tests welche mit dem [PyTest-Framwork](https://docs.pytest.org/en/6.2.x/) erstellt werden.
- Dokumentation für die Erstellung von [Tests für FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
- Um die Tests auszuführen: Rechtsklick auf den Test-Ordner -> "Run 'pytests' in tests 
- Test-Beispiele sind enthalten

#### [tmp](tmp)
1. [in](tmp/in)
    - Wird zur (temporären) Ablage von Input-Dateien für den Service verwendet, z.B. beim File-upload etc.
    - Der Pfad kann über die Variable "in_folder" der [Config-Klasse](app/configuration/getConfig.py) abgerufen werden.
2. [out](tmp/out)
    - Wird zur (temporären) Ablage von Output-Dateien des Services verwendet. 
    Wenn der Service also etwas schreibt, bitte hier ablegen. 
    - Der Pfad kann über die Variable "out_folder" der [Config-Klasse](app/configuration/getConfig.py) abgerufen werden.
3. [test](tmp/test)
    - Kann zur Ablage von Skripten etc. verwendet werden um Dinge auszuprobieren.

#### - weitere Dateien -

3. [Dockerfile](Dockerfile)
    - Dockerfile welches die Erstellung des Docker-Containers orchestriert.
    - Eine Dokumentation der Befehle liegt im File selbst vor
4. [version.txt](version.txt)
    - Aktuelle Version der Applikation. Wird am Ende in der OpenAPI/Swagger Doc Oberfläche angezeigt und sollte bei jeder Änderung nach oben gezählt werden.
5. [.gitlab-ci.yml](.gitlab-ci.yml)
    - GitLab bzw. die zugehörigen Pipelines prüfen ob eine solche Datei existiert. Falls ja, wird die darin aufgeführte
      Referenz auf ein ci/cd-Projekt verwendet um das Projekt zu bauen und bereitzustellen.
6. [Readme.md](README.md)
    - Dokumentation (this!)
7. [.gitignore.](.gitignore)
    - Beinhaltet verweise auf Dateien/Ordner welche von git ignoriert werden sollen.
    - Alles hier enthaltene wird nicht versioniert.
8. [pyproject.toml](pyproject.toml)
    - [Poetry project file](https://python-poetry.org/docs/pyproject/)

# Ausführung des Templates:
Folgende Umbebungsvariablen werden benötigt für die lokale Ausführung:

PYTHONUNBUFFERED=1;
SERVICE_URL=127.0.0.1:8000;
IS_LOCAL=True;
