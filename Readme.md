#   Let's run this app!

~~~ 
git clone git@github.com:SabirzhanovN/testingProject.git
~~~

~~~
cd testingProject/
~~~

~~~
python3 -m venv venv
~~~

~~~
source venv/bin/activate
~~~

~~~
pip install -r requirements.txt
~~~

~~~
python manage.py migrate
~~~


* Create your superuser 
~~~
python manage.py createsuperuser
~~~

~~~
python manage.py runserver
~~~
