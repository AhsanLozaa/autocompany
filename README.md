To seeed the data ->  
python3 seed_data.py

1.) please run ./setup.sh to setup the app
Note that it will creatre a super admin user (username: admin, password: adminpass)

2.) create a .env file in the root of the project and add the folowing (add the values from the settings in your environment)
DB_NAME=test1
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

3.) Run these commands to make the database migrations
python3 manage.py makemigrations autocompany
python3 manage.py migrate autocompany
python3 manage.py makemigrations product
python3 manage.py migrate product

4.) Activate the venv
source venv/bin/activate

4.) Run the app
python3 manage.py runserver

5.) You can access the swagger api doc in this url
http://localhost:8000/api/v1/swagger/schema/
