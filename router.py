# router.py
from core import auth, response, cookie
import settings
import db_setup
from controllers import (
     user_add, user_login, user_get_one, user_get_all, user_update_role,
     exam_add, exam_get_one, exam_get_all, exam_update, exam_delete,
     exam_submit, exam_results,
     question_add, question_get_all, question_get_by_exam, question_delete,
     question_import, question_export,
     report_stats
)

def route(path, method, data, headers):
     print(f"[DEBUG] path: '{path}', method: '{method}'")

     # گرفتن session_id از کوکی
     session_id = cookie.get_cookie(headers, "session_id")
     current_user = auth.get_current_user(session_id)
     user_id = current_user['id'] if current_user else None
     user_role = auth.get_user_role(user_id) if user_id else None

     # استخراج id از مسیر
     path_parts = path.strip("/").split("/")
     item_id = None
     if path_parts and path_parts[-1].isdigit():
          item_id = int(path_parts.pop())
     clean_path = "/" + "/".join(path_parts) if path_parts else "/"

     print(f"[DEBUG] clean_path: '{clean_path}', item_id: {item_id}")

     # پشتیبانی از _method (برای PUT/DELETE)
     if method == "POST" and data and '_method' in data:
          method = data['_method'][0].upper()

     # ============================================================
     #  مسیریابی با match/case (مثل پروژه استاد)
     # ============================================================
     match (clean_path, method):
          # ---------- صفحه اصلی ----------
          case ("/", "GET"):
               html = response.render_master("index.html", title="صفحه اصلی")
               return response.serve_html(html) if html else response._200("صفحه اصلی")

          # ---------- راه‌اندازی دیتابیس ----------
          case ("/setup", "GET"):
               db_setup.setup_database()
               return response._200("Database setup completed")

          # ---------- هدایت /exams بر اساس نقش ----------
          case ("/exams", "GET"):
               if not user_id:
                    return response.redirect("/login")
               if auth.is_admin(user_id):
                    return response.redirect("/admin/users")
               if auth.is_teacher(user_id):
                    return response.redirect("/teacher/exam")
               if auth.is_student(user_id):
                    return response.redirect("/student/exams")
               return response._403()

          # ---------- ورود (GET) ----------
          case ("/login", "GET"):
               if user_id:
                    return response.redirect("/dashboard")
               html = response.render_master("login.html", title="ورود")
               return response.serve_html(html)

          # ---------- ورود (POST) – اصلاح شده با redirect ----------
          case ("/login", "POST"):
               user = user_login.handle(data)
               if user:
                    sid = auth.create_session(user['id'])
                    cookie_header = cookie.set_cookie('session_id', sid, max_age=604800)
                    return response.redirect("/dashboard", {"Set-Cookie": cookie_header})
               else:
                    context = {'error': 'نام کاربری یا رمز عبور اشتباه است'}
                    html = response.render_master("login.html", context, "ورود")
                    return response.serve_html(html)

          # ---------- ثبت‌نام (GET) ----------
          case ("/register", "GET"):
               if user_id:
                    return response.redirect("/dashboard")
               # اطمینان از وجود قالب register.html
               html = response.render_master("register.html", title="ثبت نام")
               if html:
                    return response.serve_html(html)
               else:
                    # اگر قالب وجود نداشت، یک فرم ساده بساز
                    return response._200("""
                         <h2>ثبت نام</h2>
                         <form method="post" action="/register">
                         <input name="fullname" placeholder="نام کامل"><br>
                         <input name="email" placeholder="ایمیل"><br>
                         <input name="password" type="password" placeholder="رمز"><br>
                         <select name="role">
                              <option value="student">دانشجو</option>
                              <option value="teacher">استاد</option>
                         </select><br>
                         <button type="submit">ثبت نام</button>
                         </form>
                    """)

          # ---------- ثبت‌نام (POST) ----------
          case ("/register", "POST"):
               result = user_add.handle(data)
               if "موفقیت" in result:
                    return response.redirect("/login")
               return response._200(result)

          # ---------- خروج ----------
          case ("/logout", "GET"):
               if session_id:
                    auth.delete_session(session_id)
                    cookie_header = cookie.delete_cookie('session_id')
                    return response.redirect("/", {"Set-Cookie": cookie_header})
               return response.redirect("/")

          # ---------- داشبورد ----------
          case ("/dashboard", "GET"):
               if not user_id:
                    return response._401()
               html = response.render_master("dashboard.html", {'user': current_user}, "داشبورد")
               return response.serve_html(html)

          # ============================================================
          #  بخش ادمین
          # ============================================================
          case ("/admin/users", "GET"):
               if not user_id:
                    return response._401()
               if not auth.is_admin(user_id):
                    return response._403()
               users = user_get_all.handle()
               html = response.render_master("admin/users.html", {'users': users}, "مدیریت کاربران")
               return response.serve_html(html)

          case ("/admin/user", "GET") if item_id is not None:
               if not user_id:
                    return response._401()
               if not auth.is_admin(user_id):
                    return response._403()
               user = user_get_one.handle(item_id)
               if not user:
                    return response._404()
               html = response.render_master("admin/user-edit.html", {'user': user}, "ویرایش کاربر")
               return response.serve_html(html)

          case ("/admin/user", "POST") if item_id is not None:
               if not user_id or not auth.is_admin(user_id):
                    return response._403()
               user_update_role.handle(item_id, data)
               return response.redirect("/admin/users")

          # ============================================================
          #  بخش استاد
          # ============================================================
          case ("/teacher/question", "GET"):
               if not user_id:
                    return response._401()
               if not auth.is_teacher(user_id):
                    return response._403()
               questions = question_get_all.handle(user_id)
               html = response.render_master("teacher/questions.html", {'questions': questions}, "بانک سوالات")
               return response.serve_html(html)

          case ("/teacher/question/add", "GET"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               html = response.render_master("teacher/question-form.html", title="افزودن سوال")
               return response.serve_html(html)

          case ("/teacher/question/add", "POST"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               result = question_add.handle(data, user_id)
               if "موفقیت" in result:
                    return response.redirect("/teacher/question")
               return response._200(result)

          case ("/teacher/question/delete", "POST") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               question_delete.handle(item_id, user_id)
               return response.redirect("/teacher/question")

          case ("/teacher/question/import", "GET"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               html = response.render_master("teacher/question-import.html", title="بارگذاری سوالات")
               return response.serve_html(html)

          case ("/teacher/question/import", "POST"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               question_import.handle(data, user_id)
               return response.redirect("/teacher/question")

          case ("/teacher/question/export", "GET"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               return question_export.handle(user_id)

          # آزمون‌ها
          case ("/teacher/exam", "GET"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exams = exam_get_all.handle(user_id)
               html = response.render_master("teacher/exams.html", {'exams': exams}, "مدیریت آزمون‌ها")
               return response.serve_html(html)

          case ("/teacher/exam/add", "GET"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               questions = question_get_all.handle(user_id)
               html = response.render_master("teacher/exam-form.html", {'questions': questions}, "ساخت آزمون جدید")
               return response.serve_html(html)

          case ("/teacher/exam/add", "POST"):
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               result = exam_add.handle(data, user_id)
               if "موفقیت" in result:
                    return response.redirect("/teacher/exam")
               return response._200(result)

          case ("/teacher/exam", "GET") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exam = exam_get_one.handle(item_id, user_id)
               if not exam:
                    return response._404()
               questions = question_get_by_exam.handle(item_id)
               html = response.render_master("teacher/exam-detail.html", {'exam': exam, 'questions': questions}, "جزئیات آزمون")
               return response.serve_html(html)

          case ("/teacher/exam/edit", "GET") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exam = exam_get_one.handle(item_id, user_id)
               if not exam:
                    return response._404()
               questions = question_get_all.handle(user_id)
               html = response.render_master("teacher/exam-form.html", {'exam': exam, 'questions': questions}, "ویرایش آزمون")
               return response.serve_html(html)

          case ("/teacher/exam/edit", "POST") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exam_update.handle(item_id, data, user_id)
               return response.redirect("/teacher/exam")

          case ("/teacher/exam/delete", "POST") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exam_delete.handle(item_id, user_id)
               return response.redirect("/teacher/exam")

          case ("/teacher/exam/publish", "POST") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               exam_update.handle(item_id, {'is_published': '1'}, user_id)
               return response.redirect("/teacher/exam")

          case ("/teacher/exam/results", "GET") if item_id is not None:
               if not user_id or not auth.is_teacher(user_id):
                    return response._403()
               results = exam_results.handle(item_id)
               stats = report_stats.handle(item_id)
               html = response.render_master("teacher/results.html", {'results': results, 'stats': stats}, "نتایج آزمون")
               return response.serve_html(html)

          # ============================================================
          #  بخش دانشجو
          # ============================================================
          case ("/student/exams", "GET"):
               if not user_id or not auth.is_student(user_id):
                    return response._403()
               exams = exam_get_all.handle(None, only_published=True)
               html = response.render_master("student/exams.html", {'exams': exams}, "آزمون‌های من")
               return response.serve_html(html)

          case ("/student/exam/take", "GET") if item_id is not None:
               if not user_id or not auth.is_student(user_id):
                    return response._403()
               exam = exam_get_one.handle(item_id, only_published=True)
               if not exam or not exam.get('is_published'):
                    return response._404()
               questions = question_get_by_exam.handle(item_id)
               context = {'exam': exam, 'questions': questions, 'student_id': user_id}
               html = response.render_master("student/exam-take.html", context, exam.get('title', 'آزمون'))
               return response.serve_html(html)

          case ("/student/exam/submit", "POST") if item_id is not None:
               if not user_id or not auth.is_student(user_id):
                    return response._403()
               result = exam_submit.handle(item_id, user_id, data)
               if "موفقیت" in result:
                    return response.redirect(f"/student/exam/feedback/{item_id}")
               return response._200(result)

          case ("/student/exam/feedback", "GET") if item_id is not None:
               if not user_id or not auth.is_student(user_id):
                    return response._403()
               feedback = exam_results.handle(item_id, user_id)
               stats = report_stats.handle(item_id)
               context = {'feedback': feedback, 'stats': stats}
               html = response.render_master("student/exam-feedback.html", context, "بازخورد آزمون")
               return response.serve_html(html)

          # ---------- فایل‌های استاتیک ----------
          case _ if clean_path.startswith("/static/"):
               return response.serve_static_file(clean_path)

          # ---------- ۴۰۴ ----------
          case _:
               return response._404()