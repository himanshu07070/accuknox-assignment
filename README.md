# Social Networking API

## Installation

1. Clone the repository:

   git clone https://github.com/himanshu07070/social-network-api.git
   cd social-network-api

2. Build and start the Docker containers:

    docker-compose up --build

3. Apply database migrations:

    docker-compose exec web python manage.py migrate

4. Create a superuser:

    docker-compose exec web python manage.py createsuperuser