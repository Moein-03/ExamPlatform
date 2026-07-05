# router.py
import json
from pathlib import Path
from urllib.parse import parse_qs
import mimetypes
import settings
import db_setup
from controllers import (
     message_add, user_add, exam_add,
     user_show, message_show, exam_show,
     user_get_one, user_update,
     exam_get_one, exam_update
)

def render_template(filename, context=None):
     template_path = settings.TEMPLATE_DIR / filename
     if not template_path.exists():
          return None
     html = template_path.read_text(encoding="utf-8")
     if context is None:
          context = {}
     if 'base_path' not in context:
          context['base_path'] = settings.BASE_PATH
     for key, value in context.items():
          html = html.replace(f"{{{{ {key} }}}}", str(value))
     return html

def serve_html(html):
     return (html or "Template not found", 200, {"Content-Type": "text/html; charset=utf-8"})

def serve_static_file(path):
     file_path = settings.BASE_DIR / path.lstrip('/')
     if not file_path.exists():
          return _404()
     content_type, _ = mimetypes.guess_type(file_path)
     if not content_type:
          content_type = "application/octet-stream"
     return (file_path.read_bytes(), 200, {"Content-Type": content_type})

def extract_id_and_clean_path(path):
     parts = path.strip("/").split("/")
     id_val = None
     if parts and parts[-1].isdigit():
          id_val = int(parts.pop())
     clean_path = "/" + "/".join(parts) if parts else "/"
     return clean_path, id_val

def _404():
     html = render_template("errors/404.html") or "404 - صفحه یافت نشد"
     return (html, 404, {"Content-Type": "text/html; charset=utf-8"})

def _403():
     html = render_template("errors/403.html") or "403 - دسترسی ممنوع"
     return (html, 403, {"Content-Type": "text/html; charset=utf-8"})

def _500():
     html = render_template("errors/500.html") or "500 - خطای سرور"
     return (html, 500, {"Content-Type": "text/html; charset=utf-8"})

def route(path, method, body=None):
     """
          ورودی‌ها:
               path: مسیر درخواستی (بدون نام پروژه) مثل '/exams'
               method: 'GET' یا 'POST'
               body: می‌تواند رشته خام یا دیکشنری (از web_server) باشد
          خروجی: (response_body, status_code, headers)
     """

     if isinstance(body, str):
          data = parse_qs(body) if body else {}
     elif isinstance(body, dict):
          data = body
     else:
          data = {}

     if method == "POST" and '_method' in data:
          method = data['_method'][0].upper()

     clean_path, item_id = extract_id_and_clean_path(path)

     match (clean_path, method):
          case ("/", "GET"):
               html = render_template("index.html") or "<h1>خوش آمدید</h1>"
               return serve_html(html)

          case ("/setup", "GET"):
               db_setup.setup_database()
               return ("Database setup completed", 200, {"Content-Type": "text/html"})

          case ("/contact", "GET"):
               html = render_template("contact.htm")
               return serve_html(html)

          case ("/contact", "POST"):
               result = message_add.handle(data)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/register", "GET"):
               html = render_template("register.htm")
               return serve_html(html)

          case ("/register", "POST"):
               result = user_add.handle(data)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/teacher/exam", "GET") if not item_id:
               html = render_template("exam_form.htm")
               return serve_html(html)

          case ("/teacher/exam", "POST"):
               result = exam_add.handle(data)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/teacher/exam", "GET") if item_id:
               exam = exam_get_one.handle(item_id)
               if not exam:
                    return _404()
               html = render_template("edit_exam.html", exam)
               return serve_html(html)

          case ("/teacher/exam", "PUT") if item_id:
               result = exam_update.handle(item_id, data)
               return (result or "ویرایش با موفقیت انجام شد", 200, {"Content-Type": "text/html"})

          case ("/admin/user", "GET") if item_id:
               user = user_get_one.handle(item_id)
               if not user:
                    return _404()
               html = render_template("edit_user.html", user)
               return serve_html(html)

          case ("/admin/user", "PUT") if item_id:
               result = user_update.handle(item_id, data)
               return (result or "ویرایش کاربر با موفقیت", 200, {"Content-Type": "text/html"})

          case ("/exams", "GET"):
               #exams = exam_show.handle()
               #rows = ''.join(render_template("partials/exam_row.htm", exam) for exam in exams)
               #html = render_template("show_exams.htm", {"rows": rows})
               #return serve_html(html)
               exams = exam_show.handle()
               if not exams:
                    rows = "<tr><td colspan='5' style='text-align:center;'>هیچ آزمونی ثبت نشده است.</td></tr>"
               else:
                    rows = ''.join(render_template("partials/exam_row.htm", exam) for exam in exams)
               html = render_template("show_exams.htm", {"rows": rows})
               return serve_html(html)

          case ("/users", "GET"):
               users = user_show.handle()
               rows = ''.join(render_template("partials/user_row.htm", user) for user in users)
               html = render_template("show_users.htm", {"rows": rows})
               return serve_html(html)

          case ("/messages", "GET"):
               messages = message_show.handle()
               rows = ''.join(render_template("partials/message_row.htm", msg) for msg in messages)
               html = render_template("show_messages.htm", {"rows": rows})
               return serve_html(html)

          case _ if clean_path.startswith("/static/"):
               return serve_static_file(clean_path)

          case _:
               return _404()