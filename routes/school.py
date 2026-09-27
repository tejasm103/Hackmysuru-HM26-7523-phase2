"""
AdaptiveLearn AI - School Routes
"""

from flask import Blueprint, jsonify
from models.school import SchoolModel

school_bp = Blueprint("school", __name__)

@school_bp.route("/api/schools", methods=["GET"])
def get_schools():
    schools = SchoolModel.get_all()
    return jsonify({"schools": schools})
