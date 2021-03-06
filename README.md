## <img src='twitoff/static/img/logo.png' alt='twit off logo' height=40 width=40> *TwitOff*
*A fun web application for comparing and predicting Tweets*

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Demo

![showing how twitoff works](media/demo.gif)

### Architecture

![front end, back end architecture of twitoff](media/twitoff_arch.png)

### Deployed App

👉 [TwitOff](https://twitoff.com/)

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


### Acknowledgements

| [Kyle Guerrero](https://github.com/AceMouty)     |
| :--------------------: |
| <img src="https://avatars0.githubusercontent.com/u/45374681?s=400&v=4" width = "200" />                   |
| Front End Engineer |
| [<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/AceMouty) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/kyle-g-a7b7a0b6/)                   |

### Credits

This app was developed based on [curriculum](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud) from Lambda School, but it has major modifictations like:


- L2 model for improved predictions
- Responsive design via Bootstrap
- JQuery  
- Using Flask Alembic for easy db migrations

