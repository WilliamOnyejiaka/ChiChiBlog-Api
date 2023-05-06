from flask import jsonify
from typing import Dict,Tuple

def response(response_dict:Dict,status_code) -> Tuple:
    return jsonify(response_dict),status_code