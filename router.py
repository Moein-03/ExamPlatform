# ExamPlatform/router.py
import json
from pathlib import Path
import importlib.util
from urllib.parse import parse_qs

import settings
import db_setup
from controllers import message_add
from controllers import user_add
from controllers import exam_add
from controllers import user_show
from controllers import message_show
from controllers import exam_show
from controllers import user_get_one
from controllers import user_update
from controllers import exam_get_one
from controllers import exam_update

def render_template(filename, context=None):
     template_path = settings.TEMPLATE_DIR / filename
     if not template_path.exists():
          return None
     html = template_path.read_text(encoding="utf-8")
     if context:
          for key, value in context.items():
               html = html.replace(f"{{{{ {key} }}}}", str(value))
     return html

def extract_id_and_clean_path(path):
     parts = path.strip("/").split("/")
     id = None
     if parts and parts[-1].isdigit():
          id = int(parts.pop())
     clean_path = "/" + "/".join(parts) if parts else "/"
     return clean_path, id

def route(path, method, body):
     clean_path, extracted_id = extract_id_and_clean_path(path)
     
     if method == "POST" and body:
          data = parse_qs(body)
          if '_method' in data and data['_method'][0]:
               method = data['_method'][0]
     
     match (clean_path, method):
          case ("/setup", "GET"):
               db_setup.setup_database()
               return ("<p>Database setup completed</p>", 200, {"Content-Type": "text/html"})

          case ("/contact", "GET"):
               html = render_template("contact.htm")
               return (html, 200, {"Content-Type": "text/html"}) if html else ("Template not found", 404, {})

          case ("/contact", "POST"):
               result = message_add.handle(body)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/register", "GET"):
               html = render_template("register.htm")
               return (html, 200, {"Content-Type": "text/html"}) if html else ("Template not found", 404, {})

          case ("/register", "POST"):
               result = user_add.handle(body)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/teacher/exam", "GET"):
               html = render_template("exam_form.htm")
               return (html, 200, {"Content-Type": "text/html"}) if html else ("Template not found", 404, {})

          case ("/teacher/exam", "POST"):
               result = exam_add.handle(body)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/messages", "GET"):
               messages = message_show.handle()
               html = ""
               for msg in messages:
                    html += render_template("partials/message_row.htm", msg)
               full = render_template("show_messages.htm", {"messages_content": html})
               return (full, 200, {"Content-Type": "text/html"}) if full else ("Template error", 500, {})

          case ("/users", "GET"):
               users = user_show.handle()
               html = ""
               for user in users:
                    html += render_template("partials/user_row.htm", user)
               full = render_template("show_users.htm", {"users_content": html})
               return (full, 200, {"Content-Type": "text/html"}) if full else ("Template error", 500, {})

          case ("/exams", "GET"):
               exams = exam_show.handle()
               html = ""
               for exam in exams:
                    html += render_template("partials/exam_row.htm", exam)
               full = render_template("show_exams.htm", {"exams_content": html})
               return (full, 200, {"Content-Type": "text/html"}) if full else ("Template error", 500, {})

          case ("/admin/user", "GET") if not extracted_id:
               return ("لطفاً شناسه کاربر را مشخص کنید", 400, {"Content-Type": "text/plain"})

          case ("/admin/user", "GET") if extracted_id:
               user = user_get_one.handle(extracted_id)
               if not user:
                    return ("کاربر یافت نشد", 404, {"Content-Type": "text/plain"})
               html = render_template("edit_user.html", user)
               return (html, 200, {"Content-Type": "text/html"})

          case ("/admin/user", "PUT") if extracted_id:
               result = user_update.handle(extracted_id, body)
               return (result, 200, {"Content-Type": "text/html"})

          case ("/teacher/getExam", "GET") if not extracted_id:
               return ("لطفاً شناسه آزمون را مشخص کنید", 400, {"Content-Type": "text/plain"})

          case ("/teacher/getExam", "GET") if extracted_id:
               exam = exam_get_one.handle(extracted_id)
               if not exam:
                    return ("آزمون یافت نشد", 404, {"Content-Type": "text/plain"})
               html = render_template("edit_exam.html", exam)
               return (html, 200, {"Content-Type": "text/html"})

          case ("/teacher/getExam", "PUT") if extracted_id:
               result = exam_update.handle(extracted_id, body)
               return (result, 200, {"Content-Type": "text/html"})

          case _:
               return ("Not Found", 404, {"Content-Type": "text/plain"})