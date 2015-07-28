from flask import Flask, jsonify, request
import dbops
import string
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object("settings_default")
try:
    # Because we can override the debug / dev config
    app.config.from_envvar("PRODUCTION_CONFIG")
except RuntimeError:
    pass


@app.route("/")
def hello():
    """This is our root route. Returns the value route path"""
    return jsonify({"value_url": "/value"})


@app.route("/value/<inc_key>", methods=["GET"])
def increment_key_value(inc_key):
    """Get an incremented value on calling this."""
    if not all(c in string.printable for c in inc_key):
        return jsonify({"value": -1}), 404

    result, status_code = dbops.inc_value(inc_key, app)
    return jsonify(result), status_code


@app.route("/value/<inc_key>", methods=["POST"])
def set_key_value(inc_key):
    """Set a key value when invoked by POST"""
    try:
        data = request.get_json(force=True)
        result, status_code = dbops.set_val(data["key"], data["value"], app)
        return jsonify(result), status_code
    except Exception, ex:  # A BadRequest will be generated if get_json fails
        app.logger.error("Error Happened in set_key_val : ")
        return jsonify({"value": -1}), 404


if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(
        app.config["LOG_FILENAME"], maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(debug=app.config["DEBUG"], host='0.0.0.0')
