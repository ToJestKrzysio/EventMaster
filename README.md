# EventMaster
This application allows users to register for events the want to participate.
There is possibility to login via 3rd party platforms.

## Launch project
0. Clone the repository
1. Ensure you have docker installed
3. Fill up ```backend/envs/*-default``` envoromental variables configuration, and remove -default suffix.
2. Build containers
```bash
cd "repository_location"
docker-compose up --build
```
3. Access application using browser via url ```127.0.0.1:8000```

