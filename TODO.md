# TODO

- [] Contributing.md
- [] Remove ruff from pre-commit and replace with tox
- [] Add CI workflows for dev, staging and prod branches
- [] Feat: Blog category, Blog Comment, Blog Status, Search and Filter, Add more fields to Blog model
- Change id to uuid

# Project Setup

## Prerequisites

Before you begin, ensure you have the following:

- A Linux environment, or WSL (if using Windows)
- Python 3.10 or later installed

## Step-by-Step Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Pythonian/fastapi_web.git
cd fastapi_web
```

### 2. Create a Virtual Environment

```bash
make venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
make install
```

### 4. Configure Environment

Update the `.env` file with your specific configuration values.

### 5. Database Migrations

Run the migrations to set up your database tables:

```bash
make migrate
```

### 6. Running Checks

Ensure everything is set up correctly:

```bash
make check
```

### 7. Start the Development Server

```bash
make run
```

### 8. Cleaning Up

To clean up the project directory:

```bash
make clean
```

You can run `make` to see all available commands.

### 4. API Endpoints

---

# API Endpoints

Detailed documentation of available API endpoints.

## Blog Endpoints

### Create a Blog Post

- **URL**: `/v1/blog/`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "title": "string",
    "content": "string",
    "author": "string"
  }
  ```

- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Get Blog Posts

- **URL**: `/v1/blog/`
- **Method**: `GET`
- **Response**:

  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "content": "string",
      "author": "string",
      "created_at": "datetime"
    }
  ]
  ```

### Get a Single Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Update a Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `PUT`
- **Request Body**:

  ```json
  {
    "title": "string",
    "content": "string",
    "author": "string"
  }
  ```

- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Delete a Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "message": "Blog post deleted successfully"
  }
  ```

### 3. API Endpoints

The "API Endpoints" page should document the available API endpoints, their purposes, and how to use them. Here's an example:

This page provides detailed documentation of the available API endpoints in the project.

## Blog Endpoints

### Create a Blog Post

- **URL**: `/v1/blog/`
- **Method**: `POST`
- **Description**: Create a new blog post.
- **Request Body**:

  ```json
  {
    "title": "string",
    "content": "string",
    "author": "string"
  }
  ```

- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Get Blog Posts

- **URL**: `/v1/blog/`
- **Method**: `GET`
- **Description**: Retrieve a list of blog posts.
- **Response**:

  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "content": "string",
      "author": "string",
      "created_at": "datetime"
    }
  ]
  ```

### Get a Single Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `GET`
- **Description**: Retrieve a single blog post by its ID.
- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Update a Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `PUT`
- **Description**: Update an existing blog post.
- **Request Body**:

  ```json
  {
    "title": "string",
    "content": "string",
    "author": "string"
  }
  ```

- **Response**:

  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "created_at": "datetime"
  }
  ```

### Delete a Blog Post

- **URL**: `/v1/blog/{id}`
- **Method**: `DELETE`
- **Description**: Delete a blog post by its ID.
- **Response**:

  ```json
  {
    "message": "Blog post deleted successfully"
  }
  ```

Rate limiting
Caching
PATCH to PUT?
read_blog - 400 bad request?
