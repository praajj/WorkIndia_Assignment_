Requirements ->
Python 3.6+
Django 3.0+
Django REST Framework
Django REST Framework SimpleJWT

Installation ->
1. Clone this repo
2. Set Up a Virtual Environment
- python -m venv env
- source env/bin/activate
4. Install Dependencies
5. Set Up the Database
- python manage.py makemigrations
- python manage.py migrate
6. Create a Superuser
- python manage.py createsuperuser
7. Run the Development Server
- python manage.py runserver
8. Test it in Postman
7.a Register/Signup -> http://127.0.0.1:8000/register (POST)
Body example -> {
    "username": "example_user",
    "password": "example_password",
    "password2": "example_password",
    "email": "user@example.com",
    "first_name": "user1",
    "last_name": "user2"
}
7.b Login -> http://127.0.0.1:8000/login/ (POST)
Body Example -> {
    "username": "example_user",
    "password": "example_password"
}
7.c Adding the Train (only Admin/Superuser can do this) -> http://127.0.0.1:8000/add-train/ (POST)
Body Example -> {
    "train_name": "Superfast Express",
    "train_number": "12345",
    "source": "CityA",
    "destination": "CityB",
    "total_seats": 100
}
- Make sure to add the key as Authorization and Value as Bearer Access_token (ADMIN ONLY)
7.d Checkimg Availability -> http://127.0.0.1:8000/trains/availability/?source=CityA&destination=CityB (GET)
- Make sure to add the key as Authorization and Value as Bearer Access_token
7.e Booking Seat -> http://127.0.0.1:8000/trains/book-seat/ (POST)
Body Example -> {
    "train_id": 1
}
