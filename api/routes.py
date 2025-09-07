"""
API routes for Column Operations API
"""
from flask import Blueprint, request
from services.data_service import get_all_data

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

@api.route('/data')
def view_data():
    """View all data in the database"""
    return get_all_data()
