# MADR - My Digital Romance Collection

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A REST API for managing a digital book and author collection, developed as a final project for a FastAPI course.

## 📖 About The Project

MADR (My Digital Romance Collection) is a complete personal library management system that allows:
- User registration and JWT authentication
- Author (romancist) management
- Book management with relationships
- Advanced search and filters
- Automatic data sanitization

The project was developed following best practices, including automated tests, Pydantic data validation, and organized architecture.

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, high-performance web framework
- **Python 3.11+**: Programming language
- **SQLAlchemy 2.0**: ORM with modern type hints support
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation and serialization
- **Poetry**: Dependency management

### Security
- **python-jose**: JWT implementation
- **bcrypt**: Password hashing
- **OAuth2**: Authentication standard

### Testing
- **pytest**: Testing framework
- **factory-boy**: Test data generation
- **httpx**: HTTP client for testing

### Infrastructure
- **Docker**: PostgreSQL containerization
- **Uvicorn**: ASGI server

## 💡 Technical Decisions

### Why FastAPI?
I chose FastAPI for its superior performance, automatic documentation (Swagger/OpenAPI), integrated data validation with Pydantic, and native async/await support. The automatic interactive documentation makes development and endpoint testing much easier.

### Why SQLAlchemy 2.0 with Registry Pattern?
I opted for the latest SQLAlchemy version (2.0+) to use modern type hints with `Mapped` and `mapped_column`, making the code more readable with better IDE support. The registry pattern offers greater flexibility in organizing models.

### Why PostgreSQL?
PostgreSQL is a robust, open-source database widely used in production. It supports advanced features like ACID transactions, efficient indexing, and is highly reliable.

### Data Sanitization
I implemented a sanitization layer that:
- Converts names to lowercase
- Removes extra spaces and special characters
- Ensures data consistency

This prevents duplicates due to capitalization differences and improves search experience.

### Layered Architecture
I organized the project in well-defined layers:
- **Routers**: Endpoints and request/response logic
- **Schemas**: Input/output validation with Pydantic
- **Models**: Database representation
- **Core**: Configuration, authentication, and utilities

## 🚀 How to Run

### Prerequisites
- Python 3.11 or higher
- Poetry (dependency manager)
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JeanCalmon10/madr.git
cd madr
```

2. **Install dependencies**
```bash
poetry install
```

3. **Configure environment variables**

Create a `.env` file in the project root:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=madr_db
DB_USER=your_user
DB_PASSWORD=your_password
```

4. **Start the database**
```bash
docker-compose up -d
```

5. **Run the application**
```bash
poetry shell
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

Interactive documentation (Swagger): `http://localhost:8000/docs`

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Run specific tests
poetry run pytest tests/test_users.py
```

## 📚 API Endpoints

### Authentication
- `POST /auth/token` - Login and JWT token generation
- `POST /auth/refresh_token` - Token renewal

### Users
- `POST /users/` - Create new account (public)
- `GET /users/me` - Get authenticated user data
- `GET /users/{id}` - Find user by ID (public)
- `PUT /users/{id}` - Update user data (requires authentication)
- `DELETE /users/{id}` - Delete account (requires authentication)

### Romancists
- `POST /romancists/` - Add romancist (requires authentication)
- `GET /romancists/` - List romancists with filters and pagination
- `GET /romancists/{id}` - Find romancist by ID
- `PUT /romancists/{id}` - Update romancist (requires authentication)
- `DELETE /romancists/{id}` - Delete romancist (requires authentication)

### Books
- `POST /books/` - Add book (requires authentication)
- `GET /books/` - List books with filters (title, year) and pagination
- `GET /books/{id}` - Find book by ID
- `PUT /books/{id}` - Update book (requires authentication)
- `DELETE /books/{id}` - Delete book (requires authentication)

### Utilities
- `GET /health` - Check application status and database connection
- `GET /` - Root endpoint with welcome message

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Login at `/auth/token` with email and password
2. Receive the `access_token` in the response
3. Include the token in request headers: `Authorization: Bearer {token}`

Tokens expire in 30 minutes. Use `/auth/refresh_token` to renew.

## 🔍 Special Features

### Automatic Sanitization
Romancist names and book titles are automatically sanitized:
- "Machado de Assis" → "machado de assis"
- "Edgar Allan Poe    " → "edgar allan poe"

### Smart Pagination
Lists only apply pagination when there are more than 20 results, optimizing performance.

### Integrity Validations
- Prevents duplicate usernames, emails, romancists, or titles
- Validates romancist existence when creating/updating books
- Verifies ownership in user operations

### Error Handling
Clear and standardized error messages:
- `400 BAD REQUEST` - Invalid data
- `401 UNAUTHORIZED` - Not authenticated
- `403 FORBIDDEN` - No permission
- `404 NOT FOUND` - Resource not found
- `409 CONFLICT` - Data conflict (duplicate)

## 📂 Project Structure

```
madr/
├── app/
│   ├── core/
│   │   ├── auth.py          # Authentication logic
│   │   ├── config.py        # Environment settings
│   │   ├── database.py      # Database configuration
│   │   ├── jwt.py           # JWT token management
│   │   └── security.py      # Password hashing
│   ├── models/
│   │   ├── base.py          # Base model configuration
│   │   ├── user.py          # User model
│   │   ├── romancist.py     # Romancist model
│   │   └── book.py          # Book model
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── user.py          # User endpoints
│   │   ├── romancist.py     # Romancist endpoints
│   │   ├── book.py          # Book endpoints
│   │   └── health.py        # Health check endpoint
│   ├── schemas/
│   │   ├── user.py          # User schemas
│   │   ├── romancist.py     # Romancist schemas
│   │   ├── book.py          # Book schemas
│   │   └── token.py         # Token schemas
│   ├── utils/
│   │   └── sanitize.py      # Data sanitization
│   └── main.py              # Application entry point
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Authentication tests
│   ├── test_users.py        # User tests
│   ├── test_romancists.py   # Romancist tests
│   └── test_books.py        # Book tests
├── docker-compose.yml       # Docker configuration
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variables example
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🧪 Testing

The project has comprehensive test coverage including:
- Unit tests for all CRUD operations
- Authentication flow tests
- Error scenario tests (404, 401, 409, etc.)
- Database integrity tests
- Pagination and filter tests

Test coverage aims for 100% of critical code paths.

## 🤝 Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to:
1. Fork the project
2. Create a feature branch (`git checkout -b feature/MadrFeature`)
3. Commit your changes (`git commit -m 'Add some MadrFeature'`)
4. Push to the branch (`git push origin feature/MadrFeature`)
5. Open a Pull Request

## 📝 License

This project is under the MIT License. See the `LICENSE` file for more details.

## 👤 Author

**Jean Calmon**

- GitHub:[JeanCalmon10](https://github.com/JeanCalmon10)
- Email: jeancalmon10@gmail.com

## 🙏 Acknowledgments

- FastAPI course instructor for guidance and structure
- The Python and FastAPI communities for excellent documentation
- All contributors who helped improve this project

---

**Note**: This project was developed as part of a learning journey in web development with Python and FastAPI. It represents practical application of concepts including REST APIs, authentication, database relationships, and automated testing.