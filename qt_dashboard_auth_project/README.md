# Authentication System: FastAPI Backend + PyQt6 Frontend

A complete authentication system with a FastAPI backend (user registration, JWT login) and a PyQt6 desktop frontend with responsive UI.

## Project Structure

```
qt_dashboard_auth_project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # User model
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT & password hashing
│   ├── requirements.txt      # Python dependencies
│   └── users.db             # SQLite database (auto-created)
└── frontend/
    ├── app.py               # PyQt6 main application
    ├── auth_client.py       # HTTP client for backend API
    └── requirements.txt      # Python dependencies
```

## Features

### Backend (FastAPI)
- **User Registration**: Create new users with name, email, password
- **User Login**: Authenticate and receive JWT token
- **Token Verification**: Validate JWT tokens
- **Password Hashing**: Secure bcrypt hashing
- **SQLite Database**: Persist user data
- **CORS Support**: Allow frontend to communicate

### Frontend (PyQt6)
- **Login Tab**: Email and password login
- **Register Tab**: Name, email, password registration with validation
- **Dashboard Tab**: Shows logged-in user info
- **Email Validation**: Client-side validation
- **Password Strength**: Minimum 6 characters
- **Error Handling**: User-friendly error messages
- **Responsive UI**: Clean layout with proper spacing

## Installation & Setup

### 1. Clone or Navigate to the Project

```bash
cd d:\PyQt_gui_dashboard\qt_dashboard_auth_project
```

### 2. Backend Setup

```powershell
# Navigate to backend
cd backend

# Create a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```powershell
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies (PyQt6 should be available from your existing venv)
pip install -r requirements.txt
```

## Running the Application

### Terminal 1: Start Backend Server

```powershell
# From d:\PyQt_gui_dashboard\qt_dashboard_auth_project\backend
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend Application

```powershell
# From d:\PyQt_gui_dashboard\qt_dashboard_auth_project\frontend
# Use your project's existing venv
python app.py
```

## Usage Workflow

1. **Backend Running**: Server should be at `http://localhost:8000`
2. **Frontend Running**: PyQt6 window appears
3. **Register**:
   - Click "Register" tab
   - Enter name, email, password (min 6 chars)
   - Click "Register"
   - See confirmation message
4. **Login**:
   - Click "Login" tab
   - Enter email and password
   - Click "Login"
   - See user info and JWT token in "Dashboard" tab
5. **Logout**:
   - Click "Logout" button on Dashboard
   - Return to Login tab

## API Endpoints

| Method | Endpoint | Purpose | Body |
|--------|----------|---------|------|
| POST | `/register` | Register new user | `{name, email, password}` |
| POST | `/login` | Login user | `{email, password}` |
| GET | `/verify?token=...` | Verify JWT token | Query param: `token` |
| GET | `/` | Health check | - |

## Testing

### Example cURL Requests

```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Verify Token (replace TOKEN with actual token)
curl http://localhost:8000/verify?token=TOKEN
```

## Security Notes

- **Change SECRET_KEY**: In `backend/auth.py`, change `SECRET_KEY` to a strong random string in production
- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Expiration**: Tokens expire after 30 minutes
- **CORS**: Currently allows all origins; restrict in production to your frontend URL

## Database

- **Type**: SQLite (automatic)
- **Location**: `backend/users.db`
- **Tables**: `users` (id, name, email, hashed_password, created_at)
- **Reset**: Delete `users.db` to start fresh

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Run `pip install -r requirements.txt` in backend folder |
| `ModuleNotFoundError: No module named 'PyQt6'` | Use your existing project's venv or install PyQt6 |
| `Connection refused` | Ensure backend is running on port 8000 |
| `Email already registered` | Use a different email for registration |
| `Invalid email or password` | Check email and password are correct |

## Future Enhancements

- [ ] Add password reset functionality
- [ ] Implement refresh tokens
- [ ] Add role-based access control
- [ ] Move to PostgreSQL for production
- [ ] Add email verification
- [ ] Implement 2FA (two-factor authentication)
- [ ] Add user profile editing
- [ ] Implement token blacklist for logout

## License

MIT License - Feel free to use and modify
