import os

from flask import Flask, request
from . import utils


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CACHE=os.path.join(os.getcwd(), 'cache')
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

    try:
        os.makedirs(app.config['CACHE'])
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            print(request.files)
            if 'file' not in request.files:
                return 'No file part'

            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                return 'No selected file'
            if file and utils.allowed_file(file.filename):
                filename = utils.secure_filename(file.filename)
                filename = file.filename
                file.save(os.path.join(app.config['CACHE'], filename))
                return filename + ' is uploaded'

    return app
