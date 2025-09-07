"""
API routes for Column Operations API
"""
from flask import Blueprint, request
from api.schemas import DataResponse, SumColumnsRequest, SumColumnsResponse
from services.data_service import get_all_data
from services.calculation_service import sum_columns
from services.validation_service import validate_column_names

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

@api.route('/data')
def view_data():
    """View all data in the database"""
    data_dict = get_all_data()
    return DataResponse(**data_dict).model_dump()

@api.route('/data:sumColumns', methods=['POST'])
def sum_columns_endpoint():
    """Add (Sum Columns) two columns row by row"""
    try:
        data = request.get_json()
        request_obj = SumColumnsRequest(**data)
        validate_column_names(request_obj)
        result = sum_columns(request_obj)
        return SumColumnsResponse(result=result).model_dump()
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500

