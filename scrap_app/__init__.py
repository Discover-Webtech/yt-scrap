import csv
import os, tempfile, json
import subprocess
# json
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
import time
BASE_DIR="/opt/disc_wt/"
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'scrap_app.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        # Returns index.html file in templates folder.
        return render_template("index.html")

    # After clicking the Submit Button FLASK will come into this
    @app.route('/', methods=['POST'])
    def submit():
        if request.method == 'POST':
            spider_scraps = ['amazon', 'flipkart']
            api_scraps = ['youtube']
            global input_url_final
            input_url_final = []
            input_url = request.form['url']  # Getting the Input Amazon Product URL
            input_url_list = input_url.split(',')
            for url in input_url_list:
                input_url_final.append(url.strip())
            # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
            if os.path.exists(os.path.join(tempfile.gettempdir(),'output.json')):
                os.remove(os.path.join(tempfile.gettempdir(),'output.json'))
            if os.path.exists(os.path.join(tempfile.gettempdir(),'output.csv')):
                os.remove(os.path.join(tempfile.gettempdir(),'output.csv'))

            with open(os.path.join(tempfile.gettempdir(),'start_urls.json'), 'w') as writeurlobj:
                json.dump({'urls':input_url_final}, writeurlobj)
            if request.form['website'] in spider_scraps:
                return redirect(url_for('scrap', website=request.form['website']))  # Passing to the Scrape function
            if request.form['website'] in api_scraps:
                return redirect(url_for('scrap_api', website=request.form['website'], url=request.form['url'], auth_key=request.form['auth_key']))  # Passing to the Scrape function

    @app.route("/scrap")
    def scrap():
        
        if not os.path.exists('/root/crawlerenv/files/'):
            os.makedirs('/root/crawlerenv/files/')
        subprocess.run(["mv", f"/root/crawlerenv/files/{request.args['website']}scrapy.cfg", "/root/.scrapy.cfg"])
        subprocess.run(["scrapy", "crawl", "-O", os.path.join(tempfile.gettempdir(),'output.csv'), "-t", "csv", f"{request.args['website']}spider"])

        # time.sleep(20)  # Pause the function while the scrapy spider is running
        # Returns the scraped data after being running for 20 seconds.
        # return jsonify(output_data)
        return send_file(os.path.join(tempfile.gettempdir(),'output.csv'))

    @app.route("/scrap_api")
    def scrap_api():
        subprocess.run(["python3", f"{request.args['website']}_api_scraper.py", "-i", request.args['url'], "-a", request.args['auth_key']])
        if request.args['website'] == 'youtube':
            return send_file(os.path.join(tempfile.gettempdir(),'output.csv'))
            # return send_file(os.path.join(tempfile.gettempdir(),'output.csv'))

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app  #start the app again


