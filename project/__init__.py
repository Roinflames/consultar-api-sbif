# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.debug = True
app.config['url_short'] = "https://api.sbif.cl/api-sbifv3/recursos_api/"
app.config['apikey'] = '?apikey=92ff1092dbe40cbca45f2ea8f5d6c5d1e7b5ea37'
app.config['formato'] = '&formato=json'
toolbar = DebugToolbarExtension(app)
from project.controllers import *
