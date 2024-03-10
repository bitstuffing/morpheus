import flask
from flask import Flask

def run_flask():
    app = Flask(__name__)
    # set timeout to 5 seconds
    #app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
    

    # return files from the "static" folder
    @app.route('/<path:path>')
    def path(path):
        if path == "favicon.ico":
            return ""
        #return flask.render_template(f"{path}.html")
        return ""
    
    @app.route('/')
    def index():
        return flask.render_template('index.html')
    
    @app.route('/css/<path:path>')
    def css(path):
        return flask.send_from_directory('assets', path)
    
    @app.route('/js/<path:path>')
    def js(path):
        return flask.send_from_directory('assets', path)


    # make visible for all ips
    app.run(host='0.0.0.0',debug=True)
    
if __name__ == "__main__":
    run_flask()