# EventMaster
Django web application, which allows users to enroll for events.
In case of non free events, payemnts are processed via django-payu-payments.
Simplified login ussing social accounts via django-allauth.

## Launch project
0. Clone the repository.
1. Ensure you have docker installed
3. Fill up ```backend/envs/*-default``` environmental variables configuration, and remove -default suffix.
4. Build containers.
```bash
cd "repository_location"
docker-compose up --build
```
5. Access application using browser via url ```127.0.0.1:8000```.
6. Create superuser.
```bash
# ensure docker container is running point 4
docker-compose exec backend python manage.py createsuperuser
# proceed according to instructions in bash window
```
7. login to admin and configure social accounts throught ```/admin/socialaccount/socialapp/```.
8. Configure payu if necessary.
9. 
