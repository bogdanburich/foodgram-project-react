# foodgram project

Social platfrom to publish recipes. To see project go to: http://51.250.98.13

## Local run

check docker installed and run

docker-compose build && docker-compose up from dir infra/

You can load some data, such as ingredients, tags and users running following management commdands:

```Bash
docker exec python manage.py load_ingredients
docker exec python manage.py load_tags
docker exec python manage.py load_users
```

Add .env file to dir infra/ using .env.example file.

## First deploy to server

1. Clone repo to server
2. Add .env file using .env.example file
3. Add enviromnent variables to CI
4. Run docker-compose on server: `docker-compose build && docker-compose up`
5. Collect static: `docker exec <container_name> python manage.py collectstatic`
6. Apply migrations: `docker exec <container_name> python manage.py migrate`

## Network

Manage nginx.conf if needed
