from website import make_app

app = make_app()

if __name__ == '__main__':
    app.debug = True
    app.run()