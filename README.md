# Lilleflex
TV show Episode tracker built using django and bootstrap4.<br/>
Episodes allows you to keep track of your favourite tv shows either continuing or ending and also provide you with recommendations based on your likings using machine learning using libraries like pandas, sci-kit learn, numpy etc.
Using http://thetvdb.com/ for metadata.
Inspired from https://github.com/jamienicol/episodes

Requirements:

 * python 2/3
 * django
 * sklearn
 * requests
 * pandas

To use clone the production branch, install requirements, run the following terminal commands:

    $ sudo pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    
![alt tag](https://github.com/christopheduruisseau/Lilleflex/blob/main/page.png)
