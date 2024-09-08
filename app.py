import os
import random
from flask import Flask, send_file

app = Flask(__name__)
PORT = 8081
DIRECTORY = "videos"

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_file(os.path.join(DIRECTORY, filename), mimetype='video/webm')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

