# Container image that runs your code
# pin the version
FROM godaddy/tartufo:3.3.0

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py

# Code file to execute when the docker container starts up (`entrypoint.py`)
ENTRYPOINT ["/entrypoint.py"]
