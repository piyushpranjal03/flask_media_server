import os
import random
import subprocess

from flask import Flask, Response

app = Flask(__name__)
PORT = 8081
DIRECTORY = "/app/videos"


def get_video_duration(file_path):
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries',
        'format=duration',
        '-of',
        'default=noprint_wrappers=1:nokey=1',
        file_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return float(result.stdout)


def generate_video(file_path, start_time):
    command = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', file_path,
        '-c', 'copy',
        '-f', 'webm',
        'pipe:1'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        chunk = process.stdout.read(8192)
        if not chunk:
            break
        yield chunk


@app.route('/videos/<filename>')
def serve_video(filename):
    file_path = os.path.join(DIRECTORY, filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    duration = get_video_duration(file_path)
    random_start = random.uniform(0, max(0, int(duration - 60)))  # Start within the last 60 seconds if video is shorter

    response = Response(generate_video(file_path, random_start), mimetype='video/webm')
    response.headers['Content-Disposition'] = f'inline; filename={filename}'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
