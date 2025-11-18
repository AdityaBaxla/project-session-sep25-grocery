from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv
from resources import auth_bp, api, api_bp
from flask_cors import CORS
from flask_caching import Cache
from extensions import cache
from celery_factory import celery_init_app
from celery.schedules  import crontab

def create_app():

    app = Flask(__name__)
    # load environment variable from .env

    # config
    app.config.from_object(LocalDevelopmentConfig)

    # connection for flask with flask_sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    # enable CORS
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"] )

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

    # cache
    cache.init_app(app)

    # celery config
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone = 'Asia/Kolkata',
    ),
    )
    celery_app = celery_init_app(app)
    

    # for trial
    with app.app_context():
        db.create_all()
    return app, celery_app



app, celery = create_app()


from datetime import datetime

@app.route('/cache')
@cache.cached(timeout=1)
def cache():
    return {"date" : str(datetime.utcnow())}


from tasks.test import add

@app.route("/celery-task")
def task():
    add.delay(1,2)
    return {"message": "task started"}

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, add.s(1, 5), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, add.s(100, 20), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=20, minute=00, day_of_week="*"),
        add.s(10, 20),
    )


if __name__ == "__main__":
    app.run()