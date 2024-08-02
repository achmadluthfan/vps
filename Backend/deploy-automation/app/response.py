from flask import jsonify, make_response

def success(value):
  res = {
    'data' : value
  }

  return make_response(jsonify(res)), 200

def failed(code, message):
  res = {
    'error' : {
      'code' : code,
      'message' : message
    }
  }

  return make_response(jsonify(res)), code