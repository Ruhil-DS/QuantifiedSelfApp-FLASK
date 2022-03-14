# QuantifiedSelfApp-FLASK
This is my submission for the final project for the course Modern Application Development I

Project name - Lyf Record

Roll number - 21f2001180

Name - Pushpak Ruhil

Submission date - 18 March, 2022



--------------

# How to use
  - Open your terminal in the respective folder of the repository/project.
  - First, you need to install the dependencies. Simply run the following command

            pip install -r requirements.txt

    This would install all the required dependencies onto your machine/environment.



  - From there, simply run the command ```python3 main.py``` (recommended) or ```python main.py```
    - If you are running the server from a web service like Replit, you will have to specify the host in the app.run() 
    command. In the main file, simply replace ```app.run()``` with ```app.run(host='0.0.0.0')``` 
    
  - Then, assuming the default port 5000, simply head to any of the following URLs 
        
        http://localhost:5000/
         
        http://0.0.0.0:5000/
        
        http://127.0.0.1:5000/
    A URL will also be displayed on the terminal, which can be referred to visit the web application's site.
    
------------------
# Test user
The application can be tested using a test user if you don't wish to register. Below are the credentials for the same

```python
username = 'Pushpak'  # Case in-sensitive
password = 'abcd'  # All lower case
```

------------------
# Lyf Record
- In this project, I have built a WebApp which can be used as an event logger. 
- Users can login to their account, create different sorts of tracker, and log values for that particular event in that tracker.
- Each user gets the CRUD functionality for their trackers and events(logs)
      - CRUD: Create, Read, Update, Delete
- I have used the following major technologies:
      
      - Python
      - Flask
      - Flask-SQLAlchemy
      - matplotlib's pyplot
      - HTML/CSS/JS/Jinja2/Bootstrap
      - SQLite
