from flask import Flask

# def make_app():
#     from .views import App

#     app = App()

#     return app

def make_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my secret key'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
