# django_lims
 
Legacy Django uses Python 2.6.5

docker pull ubuntu-debootstrap:10.04.4

https://registry.hub.docker.com/_/ubuntu-debootstrap?tab=tags

* Clone project

* Make a virtual env using python2

* Activate virtualenv

* Install packages

    `$ pip install -r requirements.txt`

* Sync DB

    `$python django_projects/tw/manage.py syncdb`

* Run server

    `$ python django_projects/tw/manage.py runserver`
