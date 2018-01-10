import subprocess
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='')

def replace(input_file, output_file, replacements):
    def new_value(match):
        name = match.group(1)
        if name in replacements:
            return "const auto {} = {};".format(name, replacements.get(name))
        return match.group(0)

    import re
    with open(input_file) as f:
        content = f.read()

    pattern = r'const\s+auto\s+([A-Z_]+)\s*=\s*(.+);'
    content = re.sub(pattern, new_value, content)

    with open(output_file, 'w') as f:
        f.write(content)


@app.route('/render/cornel-box/<int:width>x<int:height>')
def render(width, height):
    print("{}x{}".format(width, height))
    # 1. Replace constants
    replacements = {
        'PHOTONS': request.args.get('photons', "50"),
        'WIDTH': float(width),
        'HEIGHT': float(height),
    }
    replace('../main.cpp', 'main.cpp', replacements)


    # 2. compile
    subprocess.check_call(['g++', '-std=c++11', 'main.cpp', '-o', 'small_radiosity'])

    # 3. run
    subprocess.check_call('./small_radiosity')

    # 4. convert to png
    subprocess.check_call('convert cameraImage.ppm cameraImage.png'.split())
    return app.send_static_file('cameraImage.png')

@app.route('/')
def index():
    return render_template('index.html')
