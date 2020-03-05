## <img src='twitoff/static/img/logo.png' alt='twit off logo' height=40 width=40> *TwitOff*
*A fun web application for comparing and predicting Tweets*

---

### Deployed App

👉 [TwitOff](https://twitoff-says.herokuapp.com/)

### Usage if running local

> Make sure you have Python 3.4 or higher, and git

1. Clone the repo: `git clone https://github.com/hurshd0/TwitOff.git`
2. Change directory: `cd TwitOff`
3. Install Pipenv: `pip install pipenv`, if running conda use: `conda -c conda-forge install pipenv`
4. Create Virtual Environment: 
    a. Install python packages need to run app: `pipenv install -r requirements.txt`
    b. Activate virtual environment: `pipenv shell` 
5. Setup App environment variable:
    a. On linux: `export FLASK_APP=twitoff:APP`
    b. On Windows: `set FLASK_APP=twitoff:APP`
6. `flask run`
7. Navigate to `httpL//localhost:5000` on your browser, and have fun! 🥳