###############################################
#                                             #
#                   TEST                      #
#                                             #
###############################################
test:
	PYTHONPATH=. python manage.py test

test-auth:
	python manage.py test authentication

test-product:
	python manage.py test product


###############################################
#                                             #
#                  DATABASE                   #
#                                             #
###############################################
makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

makemigrate: makemigrations migrate

###############################################
#                                             #
#                    RUN                      #
#                                             #
###############################################
runserver:
	python manage.py runserver 7000