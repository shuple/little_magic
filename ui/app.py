# -*- coding: utf-8 -*-

import argparse, flask, json, os, re, sys
import logging, traceback

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f'{path}/../lib')

# flask instance
#
app = flask.Flask(__name__, static_url_path='/static')

# application info
#
with open("%s/../config/app.json" % (path), 'r') as fp:
    env = json.loads(fp.read())

# index
#
@app.route('/', methods=['GET'])
def root():
    return flask.redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    try:
        return flask.render_template('index.htm', path='index.htm', env=env)
    except Exception as e:
        logging.error(f'{flask.request.path} {traceback.format_exc()}')
        return {}
#  def index()

# stage map data
#
@app.route('/post/stage', methods=['POST'])
def post_oneline():
    try:
        data = flask.request.json
        with open(f"{path}/../data/system/map/sfc/{data['stage']}.json") as f:
            d = { 'data': f.read() }
    except Exception as e:
        logging.error(f'{flask.request.path} {traceback.format_exc()}')
        d = { 'error': f'{str(e)}' }
    return json.dumps(d)
#  def post_oneline()

# parse command line argument
#
def parse_args():
    parser = argparse.ArgumentParser(description='Little Magic REST API')
    parser.add_argument('--host', default='0.0.0.0', help='bind IP address')
    parser.add_argument('-d', '--debug', action='store_true', help='development mode')
    parser.add_argument('-p', '--port', type=int, default=44344, help='bind port')

    return vars(parser.parse_args())
#  def parse_arg()

# run flask
#
if __name__ == '__main__':
    # command line argument
    args = parse_args()

    # log setting
    logging_level = level=logging.DEBUG if args['debug'] else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)

    # flask setting
    app.config.update({ 'MAX_CONTENT_LENGTH': 1024 * 1024 * 10, 'DEBUG': args['debug'] })
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
#  if
