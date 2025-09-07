"""
API routes for Column Operations API
"""
from flask import Blueprint, request
from api.schemas import DataResponse, SumColumnsRequest, SumColumnsResponse, FormulaRequest, FormulaResponse
from services.data_service import get_all_data
from services.calculation_service import sum_columns, calculate_formula
from services.validation_service import validate_column_names, validate_formula

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

@api.route('/data:calculateFormula', methods=['POST'])
def calculate_formula_endpoint():
    """Calculate formula for each row"""
    try:
        data = request.get_json()
        request_obj = FormulaRequest(**data)
        validate_formula(request_obj)
        result = calculate_formula(request_obj)
        return FormulaResponse(result=result).model_dump()
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500
