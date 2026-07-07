# core/response.py
import mimetypes
import settings
import json
from pathlib import Path

def render_template(filename, context=None):
     template_path = settings.TEMPLATE_DIR / filename
     if not template_path.exists():
          print(f"[ERROR] Template not found: {template_path}")
          return None
     html = template_path.read_text(encoding="utf-8")
     if context is None:
          context = {}
     context['base_url'] = settings.BASE_URL
     for key, value in context.items():
          html = html.replace(f"{{{{ {key} }}}}", str(value))
     data_json = json.dumps(context, ensure_ascii=False)
     script = f'<script>window.__DATA__ = {data_json};</script>'
     if '</body>' in html:
          html = html.replace('</body>', script + '</body>')
     else:
          html += script
     return html

def render_master(main_filename, main_context=None, title='', master='master.html'):
     main_content = render_template(main_filename, main_context)
     if main_content is None:
          return None
     master_context = {'content': main_content, 'title': title}
     return render_template(master, master_context)

def serve_html(html, headers=None):
     if html is None:
          html = "صفحه پیدا نشد (قالب وجود ندارد)"
     response_headers = {"Content-Type": "text/html; charset=utf-8"}
     if headers:
          response_headers.update(headers)
     return (html, 200, response_headers)

def serve_static_file(path):
     rel_path = path[len(settings.STATIC_URL_PREFIX):]
     file_path = settings.STATIC_DIR / rel_path
     if not file_path.exists():
          return _404()
     content_type, _ = mimetypes.guess_type(file_path)
     if not content_type:
          content_type = "application/octet-stream"
     return (file_path.read_bytes(), 200, {"Content-Type": content_type})

def _200(message):
     return (message, 200, {"Content-Type": "text/html; charset=utf-8"})

def _401(message="401 - نیاز به احراز هویت"):
     html = render_template("errors/401.html") or message
     return (html, 401, {"Content-Type": "text/html; charset=utf-8"})

def _403(message="403 - دسترسی ممنوع"):
     html = render_template("errors/403.html") or message
     return (html, 403, {"Content-Type": "text/html; charset=utf-8"})

def _404(message="404 - صفحه یافت نشد"):
     html = render_template("errors/404.html") or message
     return (html, 404, {"Content-Type": "text/html; charset=utf-8"})

def redirect(location, headers=None):
     if not location.startswith("/"):
          location = "/" + location
     if not location.startswith(settings.BASE_URL):
          location = settings.BASE_URL + location
     response_headers = {"Location": location}
     if headers:
          response_headers.update(headers)
     return ("", 302, response_headers)