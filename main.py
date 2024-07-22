from flask import url_for
from flask import redirect
from flask import request
from flask import flash
from youtube_downloader import download_video
from flask import send_file  # Added import for send_file

import logging

from flask import Flask, render_template
from gunicorn.app.base import BaseApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'a_very_secret_key'


@app.route("/", methods=['GET', 'POST'])
def home_route():
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if video_url:
            try:
                download_path = download_video(video_url)
                return send_file(download_path, as_attachment=True)
            except Exception as e:
                flash(f'Failed to download video. Error: {str(e)}')
        return render_template("home.html")
    return render_template("home.html")


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# Do not remove the main function while updating the app.
if __name__ == "__main__":
    options = {"bind": "%s:%s" % ("0.0.0.0", "8080"), "workers": 4, "loglevel": "info", "accesslog": "-"}
    StandaloneApplication(app, options).run()