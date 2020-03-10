# FootBotApi
A set of rest api methods used for calculating statistics and applying models for football data 
Uses mongo db as a backend database 


Three methods are available:
a. /api/v1/matches/<int:match_id>/<time_status>/event-stats  : uses nested events collection for a match and build statistics per interval 
 result looks  like  { }  


b.


c.

    

#deployment instructions 

similar to this
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

sudo apt install python3-venv
python3.7 -m venv FootBotApiEnv 
cd FootBotApiEnv 
source bin/activate
git clone https://github.com/athanikos/FootBotApi
cd FootBotApi
gunicorn --bind 0.0.0.0:5000 "wsgi:create_app()"
