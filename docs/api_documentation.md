# AgriTech Platform - API Documentation

## Introduction

AgriTech provides a set of API endpoints that allow developers to integrate with and extend the platform's functionality. This document outlines the available endpoints, request/response formats, and authentication requirements.

## Authentication

Most API endpoints require authentication. AgriTech uses token-based authentication.

### Obtaining a Token

```
POST /api/token/
```

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using the Token

Include the token in the Authorization header of your requests:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Refreshing the Token

```
POST /api/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Base URL

All API endpoints are relative to:

```
https://yourdomain.com/api/v1/
```

## Endpoints

### User Management

#### Register a new user

```
POST /users/register/
```

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "password_confirmation": "securepassword",
  "user_type": "buyer",
  "phone_number": "+919876543210",
  "address": "123 Farm Road, Village",
  "preferred_language": "en"
}
```

**Response:**
```json
{
  "id": 123,
  "username": "newuser",
  "email": "user@example.com",
  "user_type": "buyer",
  "phone_number": "+919876543210",
  "preferred_language": "en"
}
```

#### Get user profile

```
GET /users/profile/
```

**Response:**
```json
{
  "id": 123,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "buyer",
  "phone_number": "+919876543210",
  "address": "123 Farm Road, Village",
  "preferred_language": "en",
  "profile_picture": "https://yourdomain.com/media/profiles/user123.jpg"
}
```

#### Update user profile

```
PATCH /users/profile/
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+919876543210"
}
```

**Response:**
```json
{
  "id": 123,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "buyer",
  "phone_number": "+919876543210",
  "address": "123 Farm Road, Village",
  "preferred_language": "en",
  "profile_picture": "https://yourdomain.com/media/profiles/user123.jpg"
}
```

### Government Schemes

#### List all schemes

```
GET /schemes/
```

**Query Parameters:**
- `language` (optional): Filter by language code (e.g., "en", "hi")
- `featured` (optional): Filter featured schemes (true/false)
- `search` (optional): Search in title and content
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 42,
  "next": "https://yourdomain.com/api/v1/schemes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "PM-KISAN Scheme",
      "slug": "pm-kisan-scheme",
      "content": "Pradhan Mantri Kisan Samman Nidhi...",
      "eligibility_criteria": "All landholding farmers...",
      "benefits": "Income support of Rs.6000/- per year...",
      "application_process": "Apply online through the official PM-KISAN portal...",
      "contact_information": "PM-KISAN Helpline: 011-23381092...",
      "language": "en",
      "featured": true,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    // More schemes...
  ]
}
```

#### Get scheme details

```
GET /schemes/{slug}/
```

**Response:**
```json
{
  "id": 1,
  "title": "PM-KISAN Scheme",
  "slug": "pm-kisan-scheme",
  "content": "Pradhan Mantri Kisan Samman Nidhi...",
  "eligibility_criteria": "All landholding farmers...",
  "benefits": "Income support of Rs.6000/- per year...",
  "application_process": "Apply online through the official PM-KISAN portal...",
  "contact_information": "PM-KISAN Helpline: 011-23381092...",
  "language": "en",
  "featured": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Farming Practices

#### List all farming practices

```
GET /practices/
```

**Query Parameters:**
- `language` (optional): Filter by language code
- `practice_type` (optional): Filter by practice type
- `search` (optional): Search in title and content
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 25,
  "next": "https://yourdomain.com/api/v1/practices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Crop Rotation",
      "slug": "crop-rotation",
      "content": "Crop rotation is the practice of growing...",
      "practice_type": "organic",
      "implementation_guide": "1. Identify the crops to be included...",
      "benefits": "Reduces soil erosion, increases soil fertility...",
      "success_stories": "Farmers in Karnataka reported a 40% increase...",
      "language": "en",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    // More practices...
  ]
}
```

#### Get practice details

```
GET /practices/{slug}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Crop Rotation",
  "slug": "crop-rotation",
  "content": "Crop rotation is the practice of growing...",
  "practice_type": "organic",
  "implementation_guide": "1. Identify the crops to be included...",
  "benefits": "Reduces soil erosion, increases soil fertility...",
  "success_stories": "Farmers in Karnataka reported a 40% increase...",
  "language": "en",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Agricultural Technologies

#### List all technologies

```
GET /technologies/
```

**Query Parameters:**
- `language` (optional): Filter by language code
- `min_cost` (optional): Minimum implementation cost
- `max_cost` (optional): Maximum implementation cost
- `search` (optional): Search in title and content
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 18,
  "next": "https://yourdomain.com/api/v1/technologies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Drone-Based Crop Monitoring",
      "slug": "drone-based-crop-monitoring",
      "content": "Using drones equipped with multispectral cameras...",
      "implementation_cost": 50000.00,
      "usage_instructions": "1. Plan flight path using the provided software...",
      "supplier_information": "Agri Drone Technologies, Contact: +91 98765 43210...",
      "language": "en",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    // More technologies...
  ]
}
```

#### Get technology details

```
GET /technologies/{slug}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Drone-Based Crop Monitoring",
  "slug": "drone-based-crop-monitoring",
  "content": "Using drones equipped with multispectral cameras...",
  "implementation_cost": 50000.00,
  "usage_instructions": "1. Plan flight path using the provided software...",
  "supplier_information": "Agri Drone Technologies, Contact: +91 98765 43210...",
  "language": "en",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Marketplace

#### List all marketplace categories

```
GET /marketplace/categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Seeds",
    "description": "Agricultural seeds for various crops"
  },
  {
    "id": 2,
    "name": "Tools",
    "description": "Farming tools and equipment"
  },
  // More categories...
]
```

#### List marketplace products

```
GET /marketplace/products/
```

**Query Parameters:**
- `category` (optional): Filter by category ID
- `min_price` (optional): Minimum price
- `max_price` (optional): Maximum price
- `location` (optional): Filter by location (partial match)
- `search` (optional): Search in title and description
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 150,
  "next": "https://yourdomain.com/api/v1/marketplace/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "seller": {
        "id": 42,
        "username": "farmersupplier",
        "rating": 4.8
      },
      "category": {
        "id": 1,
        "name": "Seeds"
      },
      "title": "Organic Rice Seeds",
      "description": "High-yield, disease-resistant organic rice seeds...",
      "price": 250.00,
      "quantity": 100,
      "location": "Chennai, Tamil Nadu",
      "image_url": "https://yourdomain.com/media/marketplace/product1.jpg",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    // More products...
  ]
}
```

#### Get product details

```
GET /marketplace/products/{id}/
```

**Response:**
```json
{
  "id": 1,
  "seller": {
    "id": 42,
    "username": "farmersupplier",
    "rating": 4.8,
    "phone_number": "+919876543210",
    "location": "Chennai, Tamil Nadu"
  },
  "category": {
    "id": 1,
    "name": "Seeds"
  },
  "title": "Organic Rice Seeds",
  "description": "High-yield, disease-resistant organic rice seeds...",
  "price": 250.00,
  "quantity": 100,
  "location": "Chennai, Tamil Nadu",
  "image_url": "https://yourdomain.com/media/marketplace/product1.jpg",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

#### Create a new product listing

```
POST /marketplace/products/
```

**Request Body:**
```json
{
  "category_id": 1,
  "title": "Fresh Organic Tomatoes",
  "description": "Farm-fresh organic tomatoes grown without chemicals",
  "price": 40.00,
  "quantity": 50,
  "location": "Pune, Maharashtra",
  "image_url": "https://example.com/images/tomatoes.jpg"
}
```

**Response:**
```json
{
  "id": 151,
  "seller": {
    "id": 123,
    "username": "newuser",
    "rating": null
  },
  "category": {
    "id": 1,
    "name": "Seeds"
  },
  "title": "Fresh Organic Tomatoes",
  "description": "Farm-fresh organic tomatoes grown without chemicals",
  "price": 40.00,
  "quantity": 50,
  "location": "Pune, Maharashtra",
  "image_url": "https://example.com/images/tomatoes.jpg",
  "created_at": "2025-04-12T12:34:56Z",
  "updated_at": "2025-04-12T12:34:56Z"
}
```

#### Update a product listing

```
PATCH /marketplace/products/{id}/
```

**Request Body:**
```json
{
  "price": 45.00,
  "quantity": 40
}
```

**Response:**
```json
{
  "id": 151,
  "seller": {
    "id": 123,
    "username": "newuser",
    "rating": null
  },
  "category": {
    "id": 1,
    "name": "Seeds"
  },
  "title": "Fresh Organic Tomatoes",
  "description": "Farm-fresh organic tomatoes grown without chemicals",
  "price": 45.00,
  "quantity": 40,
  "location": "Pune, Maharashtra",
  "image_url": "https://example.com/images/tomatoes.jpg",
  "created_at": "2025-04-12T12:34:56Z",
  "updated_at": "2025-04-12T12:40:23Z"
}
```

#### Delete a product listing

```
DELETE /marketplace/products/{id}/
```

**Response:**
```
204 No Content
```

### Orders

#### List user orders

```
GET /marketplace/orders/
```

**Query Parameters:**
- `status` (optional): Filter by order status
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "product": {
        "id": 42,
        "title": "Organic Rice Seeds",
        "price": 250.00
      },
      "buyer": {
        "id": 123,
        "username": "newuser"
      },
      "quantity": 2,
      "total_price": 500.00,
      "status": "pending",
      "shipping_address": "123 Farm Road, Village",
      "created_at": "2025-04-10T15:30:00Z",
      "updated_at": "2025-04-10T15:30:00Z"
    },
    // More orders...
  ]
}
```

#### Get order details

```
GET /marketplace/orders/{id}/
```

**Response:**
```json
{
  "id": 1,
  "product": {
    "id": 42,
    "title": "Organic Rice Seeds",
    "price": 250.00,
    "seller": {
      "id": 42,
      "username": "farmersupplier",
      "phone_number": "+919876543210"
    }
  },
  "buyer": {
    "id": 123,
    "username": "newuser",
    "phone_number": "+919876543210",
    "address": "123 Farm Road, Village"
  },
  "quantity": 2,
  "total_price": 500.00,
  "status": "pending",
  "shipping_address": "123 Farm Road, Village",
  "created_at": "2025-04-10T15:30:00Z",
  "updated_at": "2025-04-10T15:30:00Z"
}
```

#### Create a new order

```
POST /marketplace/orders/
```

**Request Body:**
```json
{
  "product_id": 42,
  "quantity": 2,
  "shipping_address": "123 Farm Road, Village"
}
```

**Response:**
```json
{
  "id": 6,
  "product": {
    "id": 42,
    "title": "Organic Rice Seeds",
    "price": 250.00
  },
  "buyer": {
    "id": 123,
    "username": "newuser"
  },
  "quantity": 2,
  "total_price": 500.00,
  "status": "pending",
  "shipping_address": "123 Farm Road, Village",
  "created_at": "2025-04-12T13:15:00Z",
  "updated_at": "2025-04-12T13:15:00Z"
}
```

#### Update order status (for sellers)

```
PATCH /marketplace/orders/{id}/
```

**Request Body:**
```json
{
  "status": "shipped"
}
```

**Response:**
```json
{
  "id": 6,
  "product": {
    "id": 42,
    "title": "Organic Rice Seeds",
    "price": 250.00
  },
  "buyer": {
    "id": 123,
    "username": "newuser"
  },
  "quantity": 2,
  "total_price": 500.00,
  "status": "shipped",
  "shipping_address": "123 Farm Road, Village",
  "created_at": "2025-04-12T13:15:00Z",
  "updated_at": "2025-04-12T13:30:00Z"
}
```

### Blog

#### List all blog posts

```
GET /blog/posts/
```

**Query Parameters:**
- `language` (optional): Filter by language code
- `category` (optional): Filter by category ID
- `tag` (optional): Filter by tag ID
- `featured` (optional): Filter featured posts (true/false)
- `search` (optional): Search in title and content
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 25,
  "next": "https://yourdomain.com/api/v1/blog/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "New Organic Farming Subsidies Announced",
      "slug": "new-organic-farming-subsidies-announced",
      "content": "The Ministry of Agriculture has announced...",
      "author": {
        "id": 42,
        "username": "admin"
      },
      "category": {
        "id": 1,
        "name": "News",
        "slug": "news"
      },
      "tags": [
        {
          "id": 1,
          "name": "Organic",
          "slug": "organic"
        }
      ],
      "featured": true,
      "language": "en",
      "image_url": null,
      "created_at": "2025-04-12T10:00:00Z",
      "updated_at": "2025-04-12T10:00:00Z"
    },
    // More posts...
  ]
}
```

#### Get blog post details

```
GET /blog/posts/{slug}/
```

**Response:**
```json
{
  "id": 1,
  "title": "New Organic Farming Subsidies Announced",
  "slug": "new-organic-farming-subsidies-announced",
  "content": "The Ministry of Agriculture has announced...",
  "author": {
    "id": 42,
    "username": "admin"
  },
  "category": {
    "id": 1,
    "name": "News",
    "slug": "news"
  },
  "tags": [
    {
      "id": 1,
      "name": "Organic",
      "slug": "organic"
    }
  ],
  "featured": true,
  "language": "en",
  "image_url": null,
  "comments": [
    {
      "id": 1,
      "user": {
        "id": 123,
        "username": "newuser"
      },
      "content": "This is great news for organic farmers!",
      "created_at": "2025-04-12T11:30:00Z"
    }
  ],
  "created_at": "2025-04-12T10:00:00Z",
  "updated_at": "2025-04-12T10:00:00Z"
}
```

#### Add a comment to a blog post

```
POST /blog/posts/{slug}/comments/
```

**Request Body:**
```json
{
  "content": "This is great news for organic farmers!"
}
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 123,
    "username": "newuser"
  },
  "content": "This is great news for organic farmers!",
  "created_at": "2025-04-12T11:30:00Z"
}
```

### Search

#### Global search

```
GET /search/
```

**Query Parameters:**
- `query` (required): Search term
- `category` (optional): Category to search in (schemes, practices, technologies, marketplace, educational, blog)
- `language` (optional): Filter by language code
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

**Response:**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": {
    "schemes": [
      {
        "id": 1,
        "title": "PM-KISAN Scheme",
        "slug": "pm-kisan-scheme",
        "content_preview": "Pradhan Mantri Kisan Samman Nidhi...",
        "url": "/schemes/pm-kisan-scheme/"
      }
    ],
    "practices": [
      {
        "id": 1,
        "title": "Crop Rotation",
        "slug": "crop-rotation",
        "content_preview": "Crop rotation is the practice of growing...",
        "url": "/practices/crop-rotation/"
      }
    ],
    "blog": [
      {
        "id": 1,
        "title": "New Organic Farming Subsidies Announced",
        "slug": "new-organic-farming-subsidies-announced",
        "content_preview": "The Ministry of Agriculture has announced...",
        "url": "/blog/new-organic-farming-subsidies-announced/"
      }
    ],
    // Other categories...
  }
}
```

## Error Handling

All API errors follow a consistent format:

```json
{
  "error": {
    "code": "invalid_credentials",
    "message": "Unable to log in with provided credentials."
  }
}
```

Common error codes:
- `authentication_required`: Authentication is required for this endpoint
- `permission_denied`: You don't have permission to perform this action
- `invalid_credentials`: Login credentials are invalid
- `validation_error`: Request data is invalid
- `not_found`: The requested resource was not found
- `method_not_allowed`: The HTTP method is not allowed for this endpoint

## Rate Limiting

To ensure system stability, API requests are rate-limited:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit information is included in response headers:
- `X-RateLimit-Limit`: The number of requests allowed in the current period
- `X-RateLimit-Remaining`: The number of requests remaining in the current period
- `X-RateLimit-Reset`: The timestamp when the current rate limit period resets

When the rate limit is exceeded, the API will respond with status code 429 (Too Many Requests).