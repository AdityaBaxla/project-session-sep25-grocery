from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv
from resources import auth_bp, api, api_bp

def create_app():

    app = Flask(__name__)
    # load environment variable from .env
    # config
    app.config.from_object(LocalDevelopmentConfig)
    # connection for flask with flask_sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    # flask security stuff
    from flask_security.datastore import SQLAlchemyUserDatastore
    from extensions import security
    datastore = SQLAlchemyUserDatastore(db, User, Role )
    security.init_app(app, datastore = datastore, ) #register_blueprint=False

    app.datastore = datastore

    # blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # flask restful
    # api.init_app(app)


    # for trial
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run()