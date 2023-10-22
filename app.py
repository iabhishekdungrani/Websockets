#AbhishekDungrani WebSocket app
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import data
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Simulate stock price changes and updates
def simulate_price_changes():
    while True:
        for stock in data.stocks:
            stock["price"] += round(random.uniform(-5, 5), 2)
            socketio.emit('stock_update', stock)
        time.sleep(5)

#Html page that shows changes of stock price in real-time
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket route > connecting to real-time updates
@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected to stock updates'})

if __name__ == '__main__':
    # Start the price simulation in a separate thread
    price_simulation_thread = threading.Thread(target=simulate_price_changes)
    price_simulation_thread.start()

    socketio.run(app, debug=True)
