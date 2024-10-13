# Flu Metrics Collector API

## Overview

The **Flu Metrics Collector API** is a serverless RESTful API built with Python and the Serverless Framework. It is designed to receive and provide health metrics data collected by IoT devices such as the [**Flu Metrics Collector**](https://github.com/RafaelBahiense/flu-metrics-collector) (an ESP32-based device). The API provides endpoints for devices to submit data like heart rate, oxygen saturation (SpO₂), and temperature. The collected data is stored in a PostgreSQL database for analysis and monitoring.

This project is part of a college assignment aimed at collecting health data during specific times of the year and in regions identified by FIOCRUZ (Info Gripe) where flu outbreaks are common.

## Prerequisites

To deploy and run the **Flu Metrics Collector API**, you need:

- **AWS Account**: To deploy the serverless functions and resources.
- **AWS CLI**: Configured with your AWS credentials.
- **Serverless Framework**: Installed globally on your machine.
- **Python 3.11**: The runtime environment for the Lambda functions (ensure compatibility with AWS Lambda).
- **Node.js and Yarn**: For managing JavaScript dependencies.
- **Docker**: For packaging Python dependencies compatible with AWS Lambda.
- **PostgreSQL Database**: An Aurora PostgreSQL Serverless instance for production or a local PostgreSQL database for development.

## Configuration

The application uses environment variables and configuration files to set up the API endpoints, database connections, and other settings.

### Environment Variables

Create a `.env` file at the root of your project to store environment-specific variables for local development.

**Example `.env` file:**

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fluapidatabase
DB_USER=postgres
DB_PASSWORD=123456
DB_URL=postgresql://postgres:123456@localhost:5432
```

### Serverless Configuration

- **`serverless.yml`**: Configuration for deploying to AWS.
- **`serverless.offline.yml`**: Configuration for running the application locally.

### Database Configuration

The application uses an Aurora PostgreSQL Serverless database in production and a local PostgreSQL database for development. Ensure your database credentials and connection details are correctly set in your environment variables.

To create the db locally

```sh
docker build -t my-postgres-db .
docker run -d --name postgres-db -p 5432:5432 my-postgres-db
```

## Usage

### Running Locally

#### 1. Install Dependencies

**Node.js Dependencies:**

```sh
yarn install
```

**Python Dependencies:**

Create and activate a virtual environment:

```sh
python3.11 -m venv venv
source venv/bin/activate
```

Install required Python packages:

```sh
pip install -r requirements.txt
```

#### 2. Set Up Environment Variables

Create a `.env` file with the necessary variables (see the Configuration section).

#### 3. Run Database Migrations

```sh
yarn migrate:dev
```

Ensure the `DB_URL` environment variable is set correctly in your `.env` file:

```dotenv
DB_URL=postgresql://admin:123456@localhost:5432/mydatabase
```

#### 4. Download Info Gripe data

**Run Migrations:**

```sh
yarn load:dev
```

#### 5. Seed the database with data

**Run Migrations:**

```sh
yarn seed:dev
```

#### 4. Start the Server Locally

```sh
yarn dev
```

#### 5. Access the API

The API will be available at `http://localhost:4000`. You can test the endpoints using tools like `curl` or Postman.

### Deploying to AWS

#### 1. Configure AWS Credentials

Ensure your AWS CLI is configured with the necessary credentials:

```sh
aws configure
```

#### 2. Set Up Parameters

When deploying, provide the database master username and password for the Aurora PostgreSQL cluster:

```sh
serverless deploy --param="DBMasterUserPassword=YourSecurePassword" --param="DBMasterUsername=YourUsername" --verbose
```

#### 3. Run Database Migrations in Production

Invoke the migration function to run database migrations on the production database:

```sh
yarn migrate:prod
```

#### 3. Download Info Gripe data in Production

Invoke the load function to download the Info Gripe data

```sh
yarn load:prod
```

## API Endpoints

### `POST /metrics`

Endpoint to receive health metrics data from devices.

**Request:**

- **Method:** `POST`
- **URL:** `/metrics`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

```json
{
  "device_id": "device123",
  "timestamp": "2024-01-01T12:00:00Z",
  "heart_rate": 72,
  "spo2": 98,
  "temperature": 36.5
}
```

**Response:**

- **Status Code:** `200 OK` on success.
- **Body:**

```json
{
  "message": "Data received successfully."
}
```

### `GET /metrics`

Endpoint to get stored health metrics.

**Request:**

- **Method:** `GET`
- **URL:** `/metrics?page=1&limit=10`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

**Response:**

- **Status Code:** `200 OK` on success.
- **Body:**

```json
[
    {
       "id": 1
      "device_id": "device123",
      "timestamp": "2024-01-01T12:00:00Z",
      "heart_rate": 72,
      "spo2": 98,
      "temperature": 36.5
    }
]
```

### `GET /metrics/info-gripe-aggregate`

Endpoint to get stored health metrics.

**Request:**

- **Method:** `GET`
- **URL:** `/metrics/info-gripe-aggregate`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

**Response:**

- **Status Code:** `200 OK` on success.
- **Body:**

```json
[
    {
        "Estado": "RJ",
        "Ano Epidemiológico": 2024,
        "Período do Mês": "Primeira metade de Janeiro",
        "Casos de SRAG": 626
    }
]
```

### `GET /status/hello`

Endpoint for check the API and DB.

**Request:**

- **Method:** `GET`
- **URL:** `/status/hello`

**Response:**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "message": "Hello, World!"
}
```

## Database Migrations

The project uses **Alembic** for managing database migrations.

### Generating Migrations

To create a new migration:

```sh
alembic revision -m "Your migration message"
```

### Applying Migrations

To apply migrations:

```sh
alembic upgrade head
```

### Migrations Configuration

Ensure that `alembic.ini` and `alembic/env.py` are configured to use the `DB_URL` environment variable.

## Contributing

Contributions to the project are welcome! Please follow the standard Git workflow:

1. **Fork** the repository.
2. **Create** a new branch for your feature or bugfix.
3. **Make** your changes.
4. **Submit** a pull request with a clear description of your changes.

## License

The **Flu Metrics Collector API** is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Disclaimer:** Ensure you comply with all local regulations and ethical guidelines when collecting health data. The use of this API should respect privacy laws and obtain necessary consents.

---
