import sqlite3, os, bcrypt, uuid
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

DB = os.environ.get('VIDCRAFT_DB', 'backend/users.db')
SECRET_KEY = os.environ.get('JWT_SECRET', 'change-me-please')
ALGO = 'HS256'
bearer = HTTPBearer()

def _get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    return conn

def register_user(username, email, password):
    conn = _get_conn()
    uid = str(uuid.uuid4())
    pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id,username,email,password) VALUES (?,?,?,?)", (uid, username, email, pw))
    conn.commit()
    return {"id": uid, "username": username, "email": email}

def authenticate_user(email, password):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    if not row:
        return None
    uid, username, pw = row
    if bcrypt.checkpw(password.encode(), pw.encode()):
        return {"id": uid, "username": username, "email": email}
    return None

def create_access_token(data, expires_minutes=60*24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire.isoformat()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
