from flasklogin import app, csrf

if __name__ == "__main__":
    csrf.init_app(app)
    #loginmanager.init_app(app)
    app.run(host='0.0.0.0', port=8080, debug=True)