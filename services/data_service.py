"""
Database service for data operations
"""
from db.model import DataTable, SessionLocal
from api.schemas import DataRow

def get_all_data():
    """Get all data from the database"""
    session = SessionLocal()
    try:
        rows = session.query(DataTable).all()
        data = []
        for row in rows:
            data.append(DataRow(
                id=row.id,
                column_1=row.column_1,
                column_2=row.column_2,
                column_3=row.column_3,
                column_4=row.column_4,
                column_5=row.column_5
            ).model_dump())  # Convert Pydantic model to dict
        return {'data': data, 'count': len(data)}
    finally:
        session.close()

