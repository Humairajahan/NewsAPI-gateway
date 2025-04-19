# NewsAPI-gateway

This repository aims at building a gateway for the third-party API [NewsAPI](https://newsapi.org/). It securely fetches and serves real-time news using OAuth2 client credentials authentication.

## Table of contents

- [Setup and installation](#setup-and-installation)
- [Docker Deployment](#-docker-deployment)
- [Running Unittests](#running-unittests)
- [Running Pylint in Docker Container](#running-pylint-in-docker-container)
- [API Usage Examples](#api-usage-examples)
- [Future scope](#future-scope)

## Setup and installation

1. **Docker**

   Ensure [Docker Compose](https://docs.docker.com/engine/install/ubuntu/) is installed on your device.

2. **Clone the repository**

   ```bash
   git clone https://github.com/Humairajahan/NewsAPI-gateway.git
   cd NewsAPI-gateway
   ```

## 🐋 Docker Deployment

```bash
docker compose up --build -d
```

## Running Unittests

```bash
docker ps -a
docker exec -it <CONTAINER ID> python3 -m unittest discover -s src/tests
```

## Running Pylint in Docker Container

```bash
docker ps -a
docker exec -it <CONTAINER ID> pylint src/.
```

## API Usage Examples

### User Registration

```bash
curl -X 'POST' \
  'http://localhost:3000/api/v1/auth/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "confirm_password": "string"
}'
```

### Generate Access Token

```bash
curl -X 'POST' \
  'http://localhost:3000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=string&password=string&scope=&client_id=string&client_secret=string'
```

which will return the following response body:

```json
{
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1000,
      "uuid": "9a62c634-87e2-423a-8f38-b3e3cecbddb8",
      "username": "string",
      "email": "user@example.com"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1Njg3MTU1fQ.ELVZ8AgMo5xQBoIixcD6DSTzYauhtWraD9eybodyGVs",
    "token_type": "bearer"
  }
}
```

### Fetch all news with pagination

```bash
curl --location --request GET \
    'http://localhost:3000/api/v1/news?domains=bbc.co.uk&skip=1&limit=100' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

### Fetch the latest and save the top 3

```bash
curl --location 'http://localhost:3000/api/v1/news/save-latest?skip=1&domains=bbc.co.uk' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

### Fetch the top headlines by country code

```bash
curl --location --request GET 'http://localhost:3000/api/v1/news/headlines/country/us?skip=1&limit=10' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

### Fetch the top headlines by source id

```bash
curl --location --request GET 'http://localhost:3000/api/v1/news/headlines/source/bbc-news?skip=1&limit=10' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

### Fetch top headlines by filtering both country and source

```bash
curl --location --request GET 'http://localhost:3000/api/v1/news/headlines/filter?country={country_code}&source={source_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

**Implementing** this API was **not possible** due to a restriction in [NewsAPI Documentation](https://newsapi.org/docs/endpoints/top-headlines) that, country and sources parameters are not be mixed with each other.

### Fetch all the sources

```bash
curl --location --request GET 'http://localhost:3000/api/v1/news/sources?country_code=us' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MDg1OTU1fQ.Ya-_hlFKeuYfw8xiUyX0vFS-dD2RmghSLVOswIC72ZI'
```

## Future scope
