# core/cookie.py
import uuid

def get_cookie(headers, name):
     cookie_header = headers.get("Cookie")
     if not cookie_header:
          return None
     for item in cookie_header.split(";"):
          item = item.strip()
          if "=" not in item:
               continue
          key, value = item.split("=", 1)
          if key == name:
               return value
     return None

def set_cookie(name, value, path="/", max_age=None, http_only=True):
     cookie = f"{name}={value}; Path={path}"
     if max_age:
          cookie += f"; Max-Age={max_age}"
     if http_only:
          cookie += "; HttpOnly"
     return cookie

def delete_cookie(name, path="/"):
     return f"{name}=; Path={path}; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly"

def generate_session_id():
     return str(uuid.uuid4())