# SnapLinked Platform - API Documentation

## Authentication

### POST /api/auth/login
Login with email and password.

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "token": "string",
  "user": {
    "id": "number",
    "email": "string",
    "name": "string",
    "plan": "string"
  }
}
```

### POST /api/auth/logout
Logout current user.

**Headers:**
- Authorization: Bearer {token}

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## LinkedIn Integration

### POST /api/linkedin/toggle
Toggle LinkedIn automation.

**Headers:**
- Authorization: Bearer {token}

**Response:**
```json
{
  "success": true,
  "connected": "boolean",
  "status": "string"
}
```

### GET /api/linkedin/stats
Get LinkedIn automation statistics.

**Headers:**
- Authorization: Bearer {token}

**Response:**
```json
{
  "success": true,
  "stats": {
    "connections": "number",
    "messages": "number",
    "engagement": "number"
  }
}
```