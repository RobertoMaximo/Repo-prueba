from flask import Flask

app= Flask(__name__)

app.register_blueprint(url_prefix="/partidos")
app.register_blueprint(url_prefix="/usuarios")
app.register_blueprint(url_prefix='/ranking')





if __name__== "__main__":
    app.run(port=5000,debug=True)
