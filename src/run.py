from flask import jsonify, Flask, request, render_template
from autolog import autolog
import os
import time
import datetime
import logging
import threading

LOGGER = logging.getLogger("AutoLogApp")

class AutoLogApp(object):
    def __init__(self, autolog_obj, title, post_magic):
        self.bk = autolog_obj
        self.title = title
        self.post_magic = post_magic

    def get_info(self):
        l = self.bk.list()
        result = {"logs": l}
        return jsonify(result)

    def get_log_for_date(self, date):
        log = self.bk.get(date)
        if log:
            return jsonify(log)
        return jsonify({"error": "failed to find log"}), 404

    def get_logs_entries(self, oldest_date_str=None, newest_date_str=None):
        all_logs = self.bk.list()
        if not oldest_date_str:
            oldest_date_str = '1900-01-01'
        if not newest_date_str:
            newest_date_str = datetime.date.today().isoformat()
        oldest_date_str = datetime.datetime.strptime(oldest_date_str, '%Y-%m-%d').date().isoformat()
        newest_date_str = datetime.datetime.strptime(newest_date_str, '%Y-%m-%d').date().isoformat()

        result = [self.bk.get(x) for x in all_logs if x >= oldest_date_str and x <= newest_date_str]
        return result

    def get_logs(self):
        oldest_date_str = request.args.get('oldest_date', None)
        newest_date_str = request.args.get('newest_date', None)

        try:
            result = self.get_logs_entries(oldest_date_str, newest_date_str)
            LOGGER.debug("Result: {0}".format(result))
            return jsonify({"logs": result})
        except:
            return {"error": "failed to get logs"}, 500

    def post_log(self):
        data = request.get_json(force=True)
        msg = data.get('msg', None)
        magic = data.get('post_magic', None)
        if not msg or magic != self.post_magic:
            return jsonify({"error": "bad input"}), 400
        self.bk.put(msg)
        return jsonify({"result": 'success'})

    def refresh(self):
        self.bk.fetch()
        return jsonify({"result": "success"})

    def index(self):
        logs = self.get_logs_entries()
        return render_template("index.html", title=self.title, logs=logs)

    def new(self):
        return render_template("new.html", title="new message")

    def setup_flask_app(self, app):
        app.add_url_rule('/autolog/v1/info', methods=['GET'], view_func=self.get_info)
        app.add_url_rule('/autolog/v1/logs/<date>', methods=['GET'], view_func=self.get_log_for_date)
        app.add_url_rule('/autolog/v1/logs', methods=['GET'], view_func=self.get_logs)
        app.add_url_rule('/autolog/v1/logs', methods=['POST'], view_func=self.post_log)
        app.add_url_rule('/new', methods=['GET'], view_func=self.new)
        app.add_url_rule('/autolog/v1/fetch', methods=['GET'], view_func=self.refresh)
        app.add_url_rule('/', methods=['GET'], view_func=self.index)

    def fetch_loop(self):
        while True:
            try:
                LOGGER.debug("Fetching data")
                self.bk.fetch()
                time.sleep(3600)
            except:
                LOGGER.exception("Error happened in the fetch thread")

    def start_fetch_thread(self):
        fetch_thread = threading.Thread(target=self.fetch_loop)
        fetch_thread.daemon = True
        fetch_thread.start()

# environment variables in use
ENV_KEY_BAIDU_TOKEN     = 'BAIDU_TOKEN'
ENV_KEY_DATA_DIR        = 'DATA_DIR'
ENV_KEY_TZ              = 'TZ'
ENV_KEY_CITY            = 'CITY'
ENV_KEY_DEBUG           = 'DEBUG'
ENV_KEY_PORT            = 'PORT'
ENV_KEY_TITLE           = 'TITLE'
ENV_KEY_POST_MAGIC      = 'POST_MAGIC'

def main():
    baidu_token = os.getenv(ENV_KEY_BAIDU_TOKEN, '1ef059103bc02c7f1cd9b35e5bcab3ab')
    data_dir = os.getenv(ENV_KEY_DATA_DIR,
                         os.path.join(os.path.abspath(os.curdir),
                                      'autolog_data'))
    tz = os.getenv(ENV_KEY_TZ, time.tzname[1])
    city = os.getenv(ENV_KEY_CITY, "Nanjing").decode('utf-8')
    debug = os.getenv(ENV_KEY_DEBUG, None)
    port = os.getenv(ENV_KEY_PORT, "80")
    title = os.getenv(ENV_KEY_TITLE, "Autolog").decode('utf-8')
    post_magic = os.getenv(ENV_KEY_POST_MAGIC, "the-very-secret-magic")

    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level)

    autolog_obj = autolog.AutoLog(baidu_token=baidu_token, data_dir=data_dir, city=city)
    autolog_app = AutoLogApp(autolog_obj, title, post_magic)
    autolog_app.start_fetch_thread()

    app = Flask(__name__)
    autolog_app.setup_flask_app(app)
    app.run(host='0.0.0.0', port=int(port), debug=debug, threaded=True, use_reloader=False)

if __name__ == '__main__':
    main()
