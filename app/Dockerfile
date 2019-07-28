FROM python:3.7
WORKDIR /var/www
CMD ["bash","-c","pip install pipenv && pipenv install --system && gunicorn run:app -b 0.0.0.0:4000"]
