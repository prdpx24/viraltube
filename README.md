# Viraltube
> A set of APIs to fetch latest youtube videos for a given query

## Installation

#### Basic (Recommended)
* Clone the repo
```bash
git clone https://github.com/prdpx24/viraltube.git
cd viraltube/
chmod +x buid.sh
```
* Execute `build.sh` to start the build and run server
```bash
./build.sh
```
#### Via Docker
* Clone the repo
```bash
git clone https://github.com/prdpx24/viraltube.git
cd viraltube/
```
* make sure docker and docker-compose are installed in your system
```bash
docker-compose build
docker-compose up -d
``` 
#### Manual Build
* Make sure python-3.7 is installed in your system
* For debian based distros
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3-pip python3.7 python3.7-dev
```
* Setup instructions
```bash
git clone https://github.com/prdpx24/viraltube.git
cd viraltube/
virtualenv venv --python=/usr/bin/python3.7
source ./.venv/bin/activate
pip install -r requirements.txt
# although, we never push database file into remote a repository,
# but since it's for demo purpose
# you can skip below steps since all migrations are already applied and sqlite file is exists in repo
python manage.py makemigrations
python manage.py migrate
```
* Running Server(s)
```bash
python manage.py runserver 8000
# open three new terminals
# on first terminal run
redis-server
# on second terminal, activate env and run celery beat
celery -A tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
# on third terminal, activate env and run celery worker
celery -A tasks worker -l info
```

## APIs
### List Videos
* will returns the stored video data in a paginated response sorted in descending order of published datetime and a background cron get started and will fetch and save videos based on query, every 60 seconds.
* method - `GET`
* url  - `http://localhost:8000/videos/api/?query=football`
* Example - 
```bash
    curl -H "Content-Type:application/json" "http://localhost:8000/api/videos/?query=football"
```
<details><summary>Response</summary>
<img src="https://i.imgur.com/bwgHa6i.gif" width=900>
</details>

### Search Video
* To search in stored videos based on query in title and description
* method - `GET`
* url - `http://127.0.0.1:8000/api/videos/search/?query=football instagram`
* Example - 
```bash
    curl -H "Content-Type:application/json" "http://127.0.0.1:8000/api/videos/search/?query=football instagram"
```
<details><summary>Response</summary>
<img src="https://i.imgur.com/clJffed.gif" width=900>
</details>

## Admin Portal
* first create a superuser account
```bash
python manage.py createsuperuser
```
* goto http://localhost:8000/admin/
* enter credentials of the superuser account you just created and voila!
* Demo

    <img src="https://i.imgur.com/Ps0bD1W.gif" width=900>
    </details>