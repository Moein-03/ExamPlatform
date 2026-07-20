# core/cookie.py
def get_cookie(headers, name):
     if not headers:
          return None
     cookie_header = headers.get('Cookie', '')
     if not cookie_header:
          return None
     for cookie in cookie_header.split(';'):
          cookie = cookie.strip()
          if cookie.startswith(f"{name}="):
               return cookie.split('=')[1]
     return None

def set_cookie(name, value, max_age=604800, path='/'):
     return f"{name}={value}; Max-Age={max_age}; Path={path}; HttpOnly"

def delete_cookie(name, path='/'):
     return f"{name}=; Max-Age=0; Path={path}; HttpOnly"