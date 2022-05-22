from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """
    Error response for api requests
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """
    Wrapper for error response for api requests
    """
    return error_response(400, message)
