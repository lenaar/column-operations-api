# Column Operations API

A Flask-based REST API for performing column operations on integer data stored in SQLite.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd tacton

# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t column-operations-api .
docker run -p 8000:8000 column-operations-api
```

### Option 2: Local Python

#### Prerequisites

- Python 3.11+
- pip

#### Installation

```bash
# Clone the repository
git clone <repository-url>
cd tacton

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Interactive API documentation is available at: `http://localhost:8000/apidocs`

## 🔗 API Endpoints

### 1. View All Data

```http
GET /api/v1/data
```

**Response:**

```json
{
  "data": [
    {
      "id": 1,
      "column_1": 10,
      "column_2": 20,
      "column_3": 30,
      "column_4": 40,
      "column_5": 50
    },
    {
      "id": 2,
      "column_1": 15,
      "column_2": 25,
      "column_3": 35,
      "column_4": 45,
      "column_5": 55
    }
  ],
  "count": 2
}
```

### 2. Sum Two Columns

```http
POST /api/v1/data:sumColumns
```

**Request:**

```json
{
  "the_first_col_name": "column_1",
  "my_second_colname": "column_5"
}
```

**Response:**

```json
{
  "result": [60, 70]
}
```

### 3. Calculate Formula

```http
POST /api/v1/data:calculateFormula
```

**Request:**

```json
{
  "myFormula": "column_1 + column_2 * column_3"
}
```

**Response:**

```json
{
  "result": [610, 890]
}
```

## 🧪 Testing

### Docker Testing

```bash
# Run tests in Docker container
docker-compose run test

# Or build and run tests only
docker build -t column-operations-api .
docker run --rm column-operations-api python run_tests.py
```

### Local Testing

```bash
# Run all tests
python run_tests.py

# Or using pytest directly
pytest tests/ -v
```

## 🏗️ Architecture

```
├── api/           # API routes and schemas
├── config/        # Configuration and environment
├── db/            # Database models and initialization
├── services/      # Business logic
├── tests/         # Test suite
└── docs/          # API documentation
```

## ⚙️ Configuration

Copy `env.sample` to `.env` and customize:

```bash
cp env.sample .env
```

Available environment variables:

- `DATABASE_URL`: SQLite database path
- `TABLE_NAME`: Database table name
- `LOG_LEVEL`: Logging level
- `API_HOST`: API host (default: localhost)
- `API_PORT`: API port (default: 8000)

## 🔧 Development

### Adding New Columns

1. Update `config/columns.py`:

```python
COLUMN_NAMES = ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6']
```

2. Update Swagger documentation manually in `docs/openapi/v1.yaml`

3. Update database schema (migration needed)

### Code Quality

- **Type hints** throughout the codebase
- **Pydantic models** for validation
- **Comprehensive tests** with 30+ test cases
- **Error handling** with proper HTTP status codes

## 📊 Features

- ✅ **RESTful API** with Flask
- ✅ **SQLite database** with automatic initialization
- ✅ **Pydantic validation** for request/response
- ✅ **Swagger documentation** with OpenAPI 2.0
- ✅ **Comprehensive testing** with pytest
- ✅ **Error handling** with detailed error messages
- ✅ **Environment configuration** support
- ✅ **API versioning** (`/api/v1/`)
- ✅ **Modular architecture** with separation of concerns
- ✅ **Docker support** with automated testing
- ✅ **Health checks** for monitoring

## 🚧 Future Enhancements

See [ENHANCEMENTS.md](ENHANCEMENTS.md) for planned improvements.

## 📝 License

[Add your license here]
