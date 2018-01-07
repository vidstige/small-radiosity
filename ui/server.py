import subprocess
from flask import Flask, render_template

app = Flask(__name__, static_folder='')

@app.route('/render/cornel-box/250x250')
def render():
    subprocess.check_call('../build/small_radiosity')
    subprocess.check_call('convert cameraImage.ppm cameraImage.png'.split())
    return app.send_static_file('cameraImage.png')

@app.route('/')
def index():
    return render_template('index.html')
