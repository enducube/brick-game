from flask import Flask, render_template
from flask_socketio import SocketIO
import gevent


upgrades = {"generator": 0}
playersonline = 0  

app = Flask(__name__)
socketio = SocketIO(app)



### Routes

@app.route("/")
def index():
    return render_template("index.html")


## Socket.IO routes

@socketio.on("click")
def click():
    with open('save.txt', "r") as f:
        lines = f.readlines()
        bricks = int(lines[0])
    bricks += 1
    with open('save.txt', "w") as f:
        lines = f.write(str(bricks))
    print("click")
    socketio.emit("update",{'bricks': bricks,'upgrades': upgrades}, broadcast=True)

@socketio.on("buy")
def buy_upgrade(data):
    with open('save.txt', "r") as f:
        lines = f.readlines()
        bricks = int(lines[0])
    
    socketio.emit("update",{'bricks': bricks,'upgrades': upgrades}, broadcast=True)

@socketio.on("connect")
def onconnect():
    with open('save.txt') as f:
        lines = f.readlines()
        bricks = int(lines[0])
    socketio.emit("update",{'bricks': bricks,'upgrades': upgrades}, broadcast=True)

## Run app

if __name__ == "__main__":
    
    print("running")     
    socketio.run(app,host="0.0.0.0",port=80)