# Property Management API

This project is a Django-based API designed for managing properties, auctions, and related data. It provides endpoints for CRUD operations, paginated data retrieval, and a structured response format.

---

## Features

- **CRUD Operations:** Manage properties, addresses, and auction details.
- **Paginated Responses:** Retrieve large datasets with pagination.
- **Structured Responses:** All responses follow a standardized format for ease of use.
- **Error Handling:** Clear error messages for invalid or missing data.
- **Flexible Models:** Supports dynamic data storage for additional details.

---

## Project Structure

```
auction-backend/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── utils.py
│   ├── views.py
│   ├── urls.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── db.sqlite3
├── manage.py
├── requirements.txt
├── venv/
└── README.md
```

---

## Requirements

- **Python**: 3.9 or higher
- **Django**: 4.x
- **Database**: PostgreSQL (or SQLite for testing)
- **Virtual Environment**: Recommended

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AsilbekT/auction-backend.git
cd auction-backend
```


2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies


```bash
pip install -r requirements.txt
```

4. Configure the Database
Update settings.py with your database credentials:


```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the Server

```bash
python manage.py runserver
```

The API will be accessible at http://127.0.0.1:8000/api/.


## API Endpoints

| HTTP Method | Endpoint                 | Description                                      |
|-------------|--------------------------|--------------------------------------------------|
| POST        | `/api/token/`            | Obtain JWT access and refresh tokens             |
| POST        | `/api/token/refresh/`    | Refresh the access token using the refresh token |
| GET         | `/api/properties/`       | List all properties (paginated)                  |
| POST        | `/api/properties/`       | Create a new property                            |
| GET         | `/api/properties/<id>/`  | Retrieve a property by ID                        |
| PUT         | `/api/properties/<id>/`  | Update a property by ID                          |
| DELETE      | `/api/properties/<id>/`  | Delete a property by ID                          |

## Authentication Workflow

### 1. Obtain Tokens
To authenticate, users must send their credentials to the `/api/token/` endpoint to receive an access token and a refresh token.

**Request:**
```json
{
    "username": "username",
    "password": "password"
}
```
## Example Response (POST /api/token/)
```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```


## Example Request (GET /api/properties/)
Authorization: Bearer <access_token>

```json
{
    "error": false,
    "message": "Data fetched successfully",
    "data": {
        "error": false,
        "message": "Data fetched successfully",
        "data": {
            "results": [
                {
                    "id": 1,
                    "address": {
                        "full_address": "123 Main St",
                        "unit": "Apt 1",
                        "city": "Springfield",
                        "state": "IL",
                        "zip_code": "62704",
                        "county": "Sangamon"
                    },
                    "property_type": "Single Family Home",
                    "beds": 4,
                    "baths": 3.0,
                    "square_footage": 1500,
                    "lot_size": 0.5,
                    "year_built": 1990,
                    "owner_occupied": true,
                    "additional_details": {
                        "has_garage": true,
                        "school_district": "District 11"
                    }
                },
            ],
            "pagination": {
                "count": 2,
                "next": null,
                "previous": null
            }
        }
    }
}
```

