# rishattest
This is test task from Rishat.Had create an app to buy things using the stripe api.
<br>
URL: fickle-rishattest.tk

WEB routes

1) /items - items list
2) /item/{{int:itemId}} - item info


APIs routes

you can see all api routes in rishatapi.postman_collection.json file



docker setup

for local:
1) clone repository
2) rename in /nginx nginx.conf to cache_ssl.txt and cache_nossl.txt to nginx.conf
3) create .env_dev in project root with SECRET_KEY=DJANGO-SECRET_KEY, DEBUG=1, ALLOWED_HOSTS=localhost 127.0.0.1, API_KEY=YOUR_STRIPE_SECRET_KEY, AND DATABASE SETTINGS
4) delete line CSRF_TRUSTED_ORIGINS in setting.py
5) use command docker-compose up -d --build
6) create superuser inside web container: docker-compose exec web python manage.py createsuperuser
<br>
<br>
done

for prod:
1) clone repository
2) create .env_prod in project root with SECRET_KEY=DJANGO-SECRET_KEY, DEBUG=0, ALLOWED_HOSTS=<YOUR_DOMAIN OR IP> <YOUR_DOMAIN OR IP> ... <YOUR_DOMAIN OR IP>, API_KEY=YOUR_STRIPE_SECRET_KEY, AND DATABASE SETTINGS
3) put your_domain and your_email in docker-compose.prod.yml, cache_nossl.txt, nginx.conf
4) rename in /nginx nginx.conf to cache_ssl.txt and cache_nossl.txt to nginx.conf
5) make dhparam dir in /nginx, move in folder and create dhparam key with command: openssl dhparam -out dhparams-2048.pem 4096
6) use command: docker-compose -f docker-compose.prod.yml up -d --build
7) rename in /nginx nginx.conf to cache_nossl.txt and cache_ssl.txt to nginx.conf
8) rebuild and reup nginx container: docker-compose -f docker-compose.prod.yml up -d --build --no-deps nginx
9) create superuser inside app container: docker-compose -f docker-compose.prod.yml exec app python manage.py createsuperuser
<br>
<br>
done
