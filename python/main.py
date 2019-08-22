import opc
import time
import threading

from flask import Flask, render_template, redirect, url_for

from patterns.base_pattern import BasePattern

IP = '192.168.4.5'
#IP = '127.0.0.1'
PORT = '7890'
IP_PORT = IP + ':' + PORT


base = BasePattern()

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('index'))

@app.route('/')
def index():
    patterns = [p.name for p in base.patterns]
    return render_template('index.html', patterns=patterns)
    return ','.join([p.name for p in base.patterns])

@app.route('/patterns/<pattern_name>')
def select_pattern(pattern_name):
    base.set_pattern(pattern_name)
    return redirect(url_for('index'))

def start_server():
    app.run(host="0.0.0.0", port="80")


server_thread = threading.Thread(target=start_server)
server_thread.start()

client = opc.Client(IP_PORT)

if client.can_connect():
    print('    connected to %s' % IP_PORT)
else:
    # can't connect, but keep running in case the server appears later
    print('    WARNING: could not connect to %s' % IP_PORT)
print('')


#-------------------------------------------------------------------------------
# send pixels

print('    sending pixels forever (control-c to exit)...')
print('')

fps = 7
target_frame_time = 1.0 / fps


while True:
    start_frame = time.time()

    base.render_pattern()
    for i, s in enumerate(base.pixels):
        client.put_pixels([p.rgb_255 for p in s], channel=i+1)

    frame_time = time.time() - start_frame
    frame_sleep = target_frame_time - frame_time
    if frame_sleep > 0:
        time.sleep(target_frame_time - frame_time)
