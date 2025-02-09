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
3. Install Dependencies
4. Set Up the Database
- python manage.py makemigrations
- python manage.py migrate
5. Create a Superuser
- python manage.py createsuperuser
6. Run the Development Server
- python manage.py runserver
7. Test it in Postman
- Register/Signup -> http://127.0.0.1:8000/register (POST)
Body example -> {
    "username": "example_user",
    "password": "example_password",
    "password2": "example_password",
    "email": "user@example.com",
    "first_name": "user1",
    "last_name": "user2"
}
- Login -> http://127.0.0.1:8000/login/ (POST)
Body Example -> {
    "username": "example_user",
    "password": "example_password"
}
- Adding the Train (only Admin/Superuser can do this) -> http://127.0.0.1:8000/add-train/ (POST)
Body Example -> {
    "train_name": "Superfast Express",
    "train_number": "12345",
    "source": "CityA",
    "destination": "CityB",
    "total_seats": 100
}
- Make sure to add the key as Authorization and Value as Bearer Access_token (ADMIN ONLY)
- Checkimg Availability -> http://127.0.0.1:8000/trains/availability/?source=CityA&destination=CityB (GET)
- Make sure to add the key as Authorization and Value as Bearer Access_token 
- Booking Seat -> http://127.0.0.1:8000/trains/book-seat/ (POST)
Body Example -> {
    "train_id": 1
}
