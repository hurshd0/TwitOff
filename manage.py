from twitoff import create_app

APP = create_app()
APP.run(port=5001, debug=True)
