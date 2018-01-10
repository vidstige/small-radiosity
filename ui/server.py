import subprocess
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='')

@app.route('/render/cornel-box/<int:width>x<int:height>')
def render(width, height):
    # 1. compile
    subprocess.check_call(['g++', '-std=c++11', '../main.cpp', '-o', 'small_radiosity'])

    # 2. run
    photons = request.args.get('photons', "10000")
    subprocess.check_call(['../build/small_radiosity', '--photons', photons])
    subprocess.check_call('convert cameraImage.ppm cameraImage.png'.split())
    return app.send_static_file('cameraImage.png')

@app.route('/')
def index():
    return render_template('index.html')
