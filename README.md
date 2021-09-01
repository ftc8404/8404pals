# FTC 8404 Quixilver's Python web app for dealing with tournament data

This app uses Python to handle web stuff. The website is hosted on Azure at [https://pals.quixilver8404.org/](https://pals.quixilver8404.org/)
Updates to this repository are automagically deployed to the web server.

# Building for development

Prerequisites: Python 3

Building follows the general procedure found [here](https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python)

Bash:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r app/requirements.txt
    FLASK_APP=app/main.py flask run

Windows powershell:

    py -3 -m venv env
    env\scripts\activate
    pip install -r app\requirements.txt
    Set-Item Env:FLASK_APP ".\app\main.py"
    flask run

For simplicity, windows users can enable powershell scripts by opening powershell as administrator and running:

    Set-ExecutionPolicy RemoteSigned

Then run

    setup-env-dev.ps1
    flask run

Mac and Linux users can use the bash script. First make it executable:

    chmod +x setup-env-dev.sh

Then run

    setup-env-dev.sh
    FLASK_APP=app/main.py flask run

# Building for production

Prerequisites: Docker Community

First, make sure the Docker desktop app is running.

Build the Docker image with:

    docker build --rm -f "Dockerfile" -t [image tag]:latest .

Create a container instance from the image:

    docker run --rm -it -p 5000:5000 [image tag]

Push the service to Docker Hub or some other docker repository,
then link it to a platform such as Azure web services. 

# License

    Copyright 2018 Quixilver 8404

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
