# ProjectIII-The_Trial
In this repo we are creating what we were supposed to learn in better way creating a proper file


# Here write everything you learned about the project related things 
also make sure to create folder of your own name and create an env outside your folder or the main folder where requirements.txt is 

# How to Setup Docker Container

## Postgres DataBase Setup
- Go to server
  - In PostgreSQL:
    - Login/Group Role
      - Right-click and select **Create**
      - Write the role name
      - Go to **Definition** tab
      - Set the password
      - Switch to **Privileges** tab
      - Enable **"Can login?"** option
      - Save the role
    - Databases
      - Right-click and select **Create**
      - Enter the database name
      - Choose the admin user you created earlier (from Login/Group Role)
      - Save the database
- In the terminal:
  - Run migrations and start the server
### from there u ll get the db name username and password for db

## setting up your .yml file
you dont need to change the ymal file just create .env file outside and put these variables
DB_HOST=db
DB_PORT=5432
DB_NAME=ur_db_name
DB_USER=ur_username
DB_PASSWORD=ur_password
DJANGO_SECRET_KEY=your_screte

### let the port and host be as it is

### before terminal i want you to make sure that ur frontend and backend are working
to make sure create an venv outside
```
py -m venv venv
```
goto backend
```
cd backend
```
install through requirements
```
pip install -r requirements.txt
py manage.py runserver
```
and in frontend
```
cd ../frontend
npm i
npm run dev
```

### NOTE : your backend might not run due to uncomposed yml but dw try composing the yml and its good to go

## Composing docker yml file
```
docker compose up -d --build
docker compose ps
```
#### if all 3 containers are shown u r ready to go 