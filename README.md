# Flask Email Processing with Celery and SQLAlchemy

This project demonstrates a Flask application for sending emails asynchronously using Celery and storing email details in a SQLite database using SQLAlchemy.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Setup](#setup)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Endpoints](#endpoints)
  - [Example Requests](#example-requests)
- [Contributing](#contributing)

## Features

- Sends emails asynchronously using Celery workers.
- Stores sent email details (email address, body, timestamp, status) in a SQLite database.
- Provides RESTful API endpoints for retrieving email details based on filters.
- Configurable through environment variables for Gmail SMTP authentication.

## Dependencies

- Flask: Web framework for Python.
- Flask-Mail: Extension for email sending in Flask.
- Flask-RESTful: Extension for creating REST APIs in Flask.
- Celery: Distributed task queue for asynchronous processing.
- SQLAlchemy: ORM (Object-Relational Mapping) for database interactions.
- Python-dotenv: For loading environment variables from a .env file.

## Setup

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/flask-email-processing.git
cd flask-email-processing
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
### Configuration 
    
```
.env file
user_email=your_email@gmail.com
email_password=your_email_password
```

## Running the Application
1. Start a Celery worker:
```bash
      celery -A app.celery worker --loglevel=info
```
2. Run the Flask application:
```bash
      python app.py
```

## Usage

The application provides functionality to send emails asynchronously and store details of sent emails in a database. It exposes RESTful API endpoints for interacting with the email processing system.

## Endpoints

- **GET /:**
  Retrieves sent email details filtered by parameters (email, status, start_timestamp, end_timestamp).

- **POST /:**
  Initiates email sending process with provided email and body JSON payload.

## Example Requests

### Retrieve Sent Email Details

Retrieve sent email details filtered by parameters (email, status, start_timestamp, end_timestamp).

**Request:**

```http
GET http://localhost:5000/?email=recipient@example.com&status=success&start_timestamp=2024-01-01&end_timestamp=2024-06-30
```

**Response:**
```{
    "is_success": true,
    "code": 200,
    "message": "Success",
    "data": [
        {
            "email": "recipient@example.com",
            "body": "Email body content.",
            "event_time": "2024-06-15T12:30:00Z",
            "status": "success"
        },
        {
            "email": "recipient@example.com",
            "body": "Another email body.",
            "event_time": "2024-06-20T10:15:00Z",
            "status": "success"
        }
    ]
}
```

### Send an Email
Initiate the email sending process with the provided email and body JSON payload.

**Request**
```POST http://localhost:5000/
Content-Type: application/json

{
    "email": "recipient@example.com",
    "body": "This is the email body."
}
```

**Response**
```{
    "is_success": true,
    "code": 200,
    "message": "Process Initiated"
}
```



## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. Fork the repository on GitHub.
2. Clone your forked repository (`git clone https://github.com/your_username/flask-email-processing.git`).
3. Create a new branch (`git checkout -b feature/new-feature`).
4. Make your changes and commit them (`git commit -am 'Add new feature'`).
5. Push your branch to GitHub (`git push origin feature/new-feature`).
6. Submit a pull request.

Please ensure your code adheres to the project's coding standards and includes necessary tests.