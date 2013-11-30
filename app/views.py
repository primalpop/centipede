from flask import Flask, render_template, request, jsonify, make_response, session
from app import app
from app.lib.AppExceptions import *

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/locationsearch', methods=['GET'])
def locationsearch():
    try:
        if request.args.has_key('prefix'):
            prefix = request.args['prefix']
            search_results = app.locationsearch.search(prefix)
            return jsonify(status='success', results=search_results)
        else:
            raise ParameterMissingException(expected=['prefix'], provided=request.args)
    except ParameterMissingException as error:
        return jsonify(status='error', msg=str(error))