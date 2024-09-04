# Typsy
#### Video Demo:  [HERE](https://www.youtube.com/watch?v=KgXuv5290oQ)
#### Description
Typsy - a minimalist typing practice app

### About app
Typsy is a web app made in Python framework Flask and as database it uses SQLite3.
App uses Python SQLand Jinja on backend and HTML, CSS, JS, Bootstrap on frontend.
It has base.html file, that is a template for creating other html files.
HTML files are in /templates folder, JavaScript and CSS files are in /static folder.
Main app is in app.py, that can be run by command `python3 app.py` or `flask run`.
Additional flag are `--debug` for running in debug mode, which automatically refresh page after saving changes in file and `--host 0.0.0.0`, which enables access to site for every machine in local network by going to address `local_ip_of_flask_machine:port`.


### Main Page
First thing that is visible after opening app is a bunch of random English words on the middle of the screen. These words are meant to be typed as a training of typing, and are choosen by randint function from random library. That function returns a number, that is used as ID in query that gets words from databse.
Pretty much every button on keyboard has attached event listener to them and after pressing it there will be a check for correctness. If letter that should be typed is equal to button we have pressed, the letter will become a bit lighter and then we move on to the next letter. If the pressed letter was not the correct one, current letter will appear red. We can erase our mistake by hitting Backspace.
It all happens very fast, almost instantly, and it feels pretty intuitive.
After typing all words wpm (words per minute) and accuracy are counted and displayed. If user is logged in that data is sent to the server with current timestamp. Then the request for new random words is send and whole thing start again.


### Log in Page / Sign up Page
To save our progress and prevent it from disappearing we can sign up, or if we already have an account, log in. To go there we can click the upper right corner and choose from dropdown menu or just go to /login page. Going to /profile Page without being logged in will also redirect us to the login page.

Creating account and logging in are similar, at least in the frontend. All inputs are required in HTML, all have adequate types set. In backend every field is check for being empty, if it happens the error page will be rendered. After that in signup page new user will be inserted into users database, but only if the username is not aleady in use. It is necessary, because there would be no way to log in if users could have indentical usernames. Emails could be used, but I wanted them to be more like protection in case if user forgot the password. It's not implemented yet, but that could be the only way to recover password. Anyway, after while creating new user the hash of the password will be generated. This hash will be later used for logging in. It's not safe to store plain-text passwords in databases (but I did that in case I forgot password for any of the accounts, only for testing purposes). Hashes are safer, because it's really hard to crack them, especially when they are 'salted'.
Logging in on the backend also checks for empty values. After that it looks for hash of user with given usernaem. Then it compares that hash with given password by special security function called very reasonable check_password_hash from werkzeug.security module. If logging in goes well, the user_id is stored in session and user is redirected to the main page.

### Log out Option
Very simple thing to implement, not even a real page. After clicking it in the menu session is being cleared, so user_id is removed from session, and it looks like user has just entered the site. Functionalities are still working correctly, but the data about training sessions is not stored anywhere.

### Profile Page
Most useful part of app for checking on progress. To render this page user_id from session is used. Then all the data is queried from database, firstly from user to get username, then from user_data to display other data. After loading there will be displayed username, maximum wmp and average accuracy, based on database with training data. There is also button, that allows to display whole training history. After clicking this button request to the server is made. It has user_id in body. As response it gets every trainig session (not to confuse with browser session) of given user. It is then placed into a table and displayed below user stats.
