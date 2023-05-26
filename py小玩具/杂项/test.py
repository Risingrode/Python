from flask import Flask
app = Flask(__name__)

@app.route("/show/info")
def index():
    return "中国联通"

if __name__ == '__main__':
    app.run()