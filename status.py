from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/gpu-status')
def gpu_status():
    process = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    return '<pre>' + output.decode() + '</pre>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
