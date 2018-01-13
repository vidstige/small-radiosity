import subprocess
import time
from flask import Flask, render_template, request, Response, stream_with_context
import numpy as np
import pickle

app = Flask(__name__)

def replace(input_file, output_file, replacements):
    def new_value(match):
        name = match.group(1)
        if name in replacements:
            return "const auto {} = {};".format(name, str(replacements.get(name)))
        return match.group(0)

    import re
    with open(input_file) as f:
        content = f.read()

    pattern = r'const\s+auto\s+([A-Z_]+)\s*=\s*(.+);'
    content = re.sub(pattern, new_value, content)

    with open(output_file, 'w') as f:
        f.write(content)


class Estimator(object):
    def __init__(self):
        self.history = self._load()

    def _load(self):
        from os.path import isfile
        if not isfile('history.pickle'):
            return []
        with open('history.pickle', 'rb') as f:
            return pickle.load(f)

    def register(self, weights, actual):
        self.history.append((weights, actual))
        # keep last 500 items
        self.history = self.history[-500:]
        with open('history.pickle', 'wb') as f:
            pickle.dump(self.history, f)

    def estimate(self, weights):
        A = np.array([w for w, _ in self.history])
        b = np.array([t for _, t in self.history])
        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        return str(np.dot(x, np.array(weights)))


estimator = Estimator()


@app.route('/estimate/cornel-box/<int:width>x<int:height>')
def estimate(width, height):
    weights = [int(request.args.get('photons', "50")), int(width) * int(height), 1]
    return estimator.estimate(weights)


@app.route('/render/cornel-box/<int:width>x<int:height>')
def render(width, height):
    start = time.time()

    # 1. Replace constants
    options = {
        'PHOTONS': int(request.args.get('photons', "50")),
        'WIDTH': float(width),
        'HEIGHT': float(height),
    }
    replace('../main.cpp', 'main.cpp', options)

    # 2. compile
    subprocess.check_call(['g++', '-std=c++11', 'main.cpp', '-o', 'small_radiosity'])

    # 3. run
    subprocess.check_call('./small_radiosity')

    # 4. convert to png
    cmd = 'convert cameraImage.ppm png:-'.split()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stop = time.time()

    weights = [int(request.args.get('photons', "50")), int(width) * int(height), 1]
    estimator.register(weights, stop - start)

    return Response(stream_with_context(proc.stdout), mimetype="image/png")


@app.route('/')
def index():
    return render_template('index.html')
