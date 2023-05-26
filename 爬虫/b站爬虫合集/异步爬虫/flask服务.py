from flask import Flask
import time
app=Flask(__name__)

@app.route('/a')
def index_a():
    time.sleep(2)
    return 'hellow a'
@app.route('/b')
def index_b():
    time.sleep(2)
    return 'hellow b'
@app.route('/c')
def index_c():
    time.sleep(2)
    return 'hellow c'
@app.route('/d')
def index_d():
    time.sleep(2)
    return 'hellow d'
if __name__=='__main__':
    app.run(threaded=True)