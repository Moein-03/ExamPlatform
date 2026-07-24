from core import auth, response, cookie
import settings
import json
import db_setup
from controllers import (
     user_add, user_login, user_get_one, user_get_all, user_update_role,
     exam_add, exam_get_one, exam_get_all, exam_update, exam_delete,
     exam_submit, exam_results, question_update,
     question_add, question_get_all, question_get_by_exam, question_delete, question_get_one,
     question_import, question_export, answer_get_by_question,
     report_stats
)

def route(path, method, data, headers):
     print(f"[DEBUG] path: '{path}', method: '{method}'")

     session_id = cookie.get_cookie(headers, "session_id")
     current_user = auth.get_current_user(session_id)
     user_id = current_user['id'] if current_user else None
     user_role = auth.get_user_role(user_id) if user_id else None

     path_parts = path.strip("/").split("/")
     item_id = None
     if path_parts and path_parts[-1].isdigit():
          item_id = int(path_parts.pop())
     clean_path = "/" + "/".join(path_parts) if path_parts else "/"

     if method == "POST" and data and '_method' in data:
          method = data['_method'][0].upper()

     match (clean_path, method):
          # ---------- عمومی ----------
          case ("/", "GET"):
               html = response.render_template("index.html")
               return response.serve_html(html) if html else response._200("صفحه اصلی")

          case ("/setup", "GET"):
               db_setup.setup_database()
               return response._200("Database setup completed")

          # ---------- احراز هویت ----------
          case ("/login", "GET"):
               if user_id:
                    return response.redirect("/dashboard")
               context = {'base_url': settings.BASE_URL, 'error': ''}
               html = response.render_template("login.html", context)
               return response.serve_html(html)

          case ("/login", "POST"):
               user = user_login.handle(data)
               if user:
                    sid = auth.create_session(user['id'])
                    cookie_header = cookie.set_cookie('session_id', sid, max_age=604800)
                    return response.redirect("/dashboard", {"Set-Cookie": cookie_header})
               else:
                    context = {'error': 'نام کاربری یا رمز عبور اشتباه است', 'base_url': settings.BASE_URL}
                    html = response.render_template("login.html", context)
                    return response.serve_html(html)

          case ("/register", "GET"):
               if user_id:
                    return response.redirect("/dashboard")
               html = response.render_template("register.html", {'base_url': settings.BASE_URL})
               return response.serve_html(html) if html else response._200("فرم ثبت نام")

          case ("/register", "POST"):
               result = user_add.handle(data)
               if "موفقیت" in result:
                    return response.redirect("/login")
               return response._200(result)

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

               # آماده‌سازی داده‌های آماری بر اساس نقش
               dashboard_data = {}
               if user_role == 'admin':
                    dashboard_data['users_count'] = len(user_get_all.handle())
                    dashboard_data['exams_count'] = len(exam_get_all.handle(None))
                    dashboard_data['questions_count'] = len(question_get_all.handle())
               elif user_role == 'teacher':
                    dashboard_data['exams_count'] = len(exam_get_all.handle(user_id))
                    dashboard_data['questions_count'] = len(question_get_all.handle(user_id))
               else:
                    dashboard_data['exams_count'] = len(exam_get_all.handle(None, only_published=True))

               user_json = json.dumps(current_user, ensure_ascii=False)
               dashboard_json = json.dumps(dashboard_data, ensure_ascii=False)

               context = {
                    'user_json': user_json,
                    'dashboard_json': dashboard_json,
                    'base_url': settings.BASE_URL
               }
               html = response.render_master("dashboard.html", context, "داشبورد")
               return response.serve_html(html)

          # ---------- مدیریت کاربران  ----------
          case ("/users", "GET"):
               if not user_id or user_role != 'admin':
                    return response._403()
               users = user_get_all.handle()
               users_json = json.dumps(users, ensure_ascii=False)
               context = {
                    'users_json': users_json,
                    'base_url': settings.BASE_URL
               }
               html = response.render_master("users.html", context, "مدیریت کاربران")
               return response.serve_html(html)

          case ("/user", "GET") if item_id is not None:
               if not user_id or user_role != 'admin':
                    return response._403()
               user = user_get_one.handle(item_id)
               if not user:
                    return response._404()
               html = response.render_master("user-edit.html", {
                    'target_user': user,
                    'base_url': settings.BASE_URL
               }, "ویرایش کاربر")
               return response.serve_html(html)

          case ("/user", "POST") if item_id is not None:
               if not user_id or user_role != 'admin':
                    return response._403()
               user_update_role.handle(item_id, data)
               return response.redirect("/users")

          # ---------- مدیریت آزمون‌ها (یکپارچه) ----------
          #case ("/exams", "GET"):
          #     if not user_id:
          #          return response.redirect("/login")
               # دریافت داده بر اساس نقش
          #     if user_role == 'admin':
          #          exams = exam_get_all.handle(None)
          #     elif user_role == 'teacher':
          #          exams = exam_get_all.handle(user_id)
          #     elif user_role == 'student':
          #          exams = exam_get_all.handle(None, only_published=True)
          #     else:
          #          return response._403()
          #     exams_json = json.dumps(exams, ensure_ascii=False)
          #     html = response.render_master("exams.html", {
          #          'exams_json': exams_json,
          #          'user_role': user_role,
          #          'base_url': settings.BASE_URL
          #     }, "لیست آزمون‌ها")
          #     return response.serve_html(html)

          case ("/exams", "GET"):
               if not user_id:
                    return response.redirect("/login")

               if user_role == 'admin':
                    exams = exam_get_all.handle(None)
               elif user_role == 'teacher':
                    exams = exam_get_all.handle(user_id)
               elif user_role == 'student':
                    exams = exam_get_all.handle(None, only_published=True, student_id=user_id)
               else:
                    return response._403()
               
               exams_json = json.dumps(exams, ensure_ascii=False)
               html = response.render_master("exams.html", {
                    'exams_json': exams_json,
                    'user_role': user_role,
                    'base_url': settings.BASE_URL
               }, "لیست آزمون‌ها")
               return response.serve_html(html)

          case ("/exam/add", "GET"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               questions = question_get_all.handle(user_id if user_role == 'teacher' else None)
               students = user_get_all.handle(role='student')
               
               exam_json = 'null'
               questions_json = json.dumps(questions, ensure_ascii=False)
               students_json = json.dumps(students, ensure_ascii=False)
               
               context = {
                    'exam_json': exam_json,
                    'questions_json': questions_json,
                    'students_json': students_json,
                    'base_url': settings.BASE_URL
               }
               html = response.render_master("exam-form.html", context, "ساخت آزمون جدید")
               return response.serve_html(html)


          case ("/exam/add", "POST"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = exam_add.handle(data, user_id)
               if "موفقیت" in result:
                    return response.redirect("/exams")
               return response._200(result)

          #case ("/exam", "GET") if item_id is not None:
          #     if not user_id:
          #          return response._401()
          #     exam = exam_get_one.handle(item_id, user_id, only_published=(user_role == 'student'))
          #     if not exam:
          #          return response._404()
               # دانشجو فقط آزمون‌های منتشر شده را ببیند
          #     if user_role == 'student' and not exam.get('is_published'):
          #          return response._403()
          #     questions = question_get_by_exam.handle(item_id)
          #     html = response.render_master("exam-detail.html", {
          #          'exam': exam,
          #          'questions': questions,
          #          'user_role': user_role,
          #          'base_url': settings.BASE_URL
          #     }, exam.get('title', 'جزئیات آزمون'))
          #     return response.serve_html(html)
          #case ("/exam", "GET") if item_id is not None:
          #     if not user_id or user_role not in ['admin', 'teacher']:
          #          return response._403()
          #     exam = exam_get_one.handle(item_id, user_id if user_role == 'teacher' else None)
          #     if not exam:
          #          return response._404()
          #     exam_json = json.dumps(exam, ensure_ascii=False)
          #     context = {
          #          'exam_json': exam_json,
          #          'base_url': settings.BASE_URL
          #     }
          #     html = response.render_master("exam-detail.html", context, "جزئیات آزمون")
          #     return response.serve_html(html)

          case ("/exam", "GET") if item_id is not None:
               if not user_id:
                    return response._401()
               exam = exam_get_one.handle(item_id, None, only_published=(user_role == 'student'))
               if not exam:
                    return response._404()
               if user_role == 'student':
                    if exam.get('is_published') != 1:
                         return response._403()
                    if user_id not in exam.get('student_ids', []):
                         return response._403()
               elif user_role not in ['admin', 'teacher']:
                    return response._403()
               exam_json = json.dumps(exam, ensure_ascii=False)
               context = {
                    'exam_json': exam_json,
                    'base_url': settings.BASE_URL,
                    'user_role': user_role
               }
               html = response.render_master("exam-detail.html", context, "جزئیات آزمون")
               return response.serve_html(html)

          case ("/exam/edit", "GET") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               exam = exam_get_one.handle(item_id, user_id)
               if not exam:
                    return response._404()
               questions = question_get_all.handle(user_id if user_role == 'teacher' else None)
               students = user_get_all.handle(role='student')
               
               exam_json = json.dumps(exam, ensure_ascii=False)
               questions_json = json.dumps(questions, ensure_ascii=False)
               students_json = json.dumps(students, ensure_ascii=False)
               
               context = {
                    'exam_json': exam_json,
                    'questions_json': questions_json,
                    'students_json': students_json,
                    'base_url': settings.BASE_URL
               }
               html = response.render_master("exam-form.html", context, "ویرایش آزمون")
               return response.serve_html(html)

          # ===== غیرفعال کردن آزمون (تغییر به پیش‌نویس) =====
          case ("/exam/unpublish", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = exam_update.handle(item_id, {'is_published': '0'}, user_id)
               if "موفقیت" in result or "تغییر" in result:
                    return response.redirect("/exams")
               return response._200(f"خطا: {result}")

          case ("/exam/edit", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               exam_update.handle(item_id, data, user_id)
               return response.redirect("/exams")

          case ("/exam/delete", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = exam_delete.handle(item_id, user_id)
               if "موفقیت" in result or "حذف" in result:
                    return response.redirect("/exams")
               return response._200(f"خطا: {result}")

          case ("/exam/publish", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = exam_update.handle(item_id, {'is_published': '1'}, user_id)
               if "موفقیت" in result or "تغییر" in result:
                    return response.redirect("/exams")
               return response._200(f"خطا: {result}")

          case ("/exam/results", "GET") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               results = exam_results.handle(item_id)
               stats = report_stats.handle(item_id)
               html = response.render_master("exam-results.html", {
                    'results': results,
                    'stats': stats,
                    'base_url': settings.BASE_URL
               }, "نتایج آزمون")
               return response.serve_html(html)

          # ---------- شرکت در آزمون (دانشجو) ----------
          case ("/exam/take", "GET") if item_id is not None:
               if not user_id or user_role != 'student':
                    return response._403()
               exam = exam_get_one.handle(item_id, only_published=True)
               if not exam or not exam.get('is_published'):
                    return response._404()
               questions = question_get_by_exam.handle(item_id)
               questions_json = json.dumps(questions, ensure_ascii=False)
               html = response.render_master("exam-take.html", {
                    'exam': exam,
                    'questions_json': questions_json,
                    'base_url': settings.BASE_URL
               }, exam.get('title', 'آزمون'))
               return response.serve_html(html)

          case ("/exam/submit", "POST") if item_id is not None:
               if not user_id or user_role != 'student':
                    return response._403()
               result = exam_submit.handle(item_id, user_id, data)
               if "موفقیت" in result:
                    return response.redirect(f"/exam/feedback/{item_id}")
               return response._200(result)

          case ("/exam/feedback", "GET") if item_id is not None:
               if not user_id or user_role != 'student':
                    return response._403()
               feedback = exam_results.handle(item_id, user_id)
               stats = report_stats.handle(item_id)
               feedback_json = json.dumps(feedback, ensure_ascii=False)
               stats_json = json.dumps(stats, ensure_ascii=False)
               html = response.render_master("exam-feedback.html", {
                    'feedback_json': feedback_json,
                    'stats_json': stats_json,
                    'base_url': settings.BASE_URL
               }, "بازخورد آزمون")
               return response.serve_html(html)

          # ---------- مدیریت سوالات (یکپارچه) ----------
          case ("/questions", "GET"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               questions = question_get_all.handle(user_id if user_role == 'teacher' else None)
               questions_json = json.dumps(questions, ensure_ascii=False)
               html = response.render_master("questions.html", {
                    'questions_json': questions_json,
                    'user_role': user_role,
                    'base_url': settings.BASE_URL
               }, "بانک سوالات")
               return response.serve_html(html)

          case ("/question/add", "GET"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               context = {
                    'mode': 'add',
                    'question_json': 'null',
                    'answers_json': 'null',
                    'base_url': settings.BASE_URL,
                    'error': ''
               }
               html = response.render_master("question-form.html", context, "افزودن سوال")
               return response.serve_html(html)

          case ("/question/add", "POST"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               
               answers_json = data.get('answers', [''])[0]
               answers = []
               if answers_json:
                    try:
                         answers = json.loads(answers_json)
                    except:
                         pass
               data['answers'] = answers
               
               result = question_add.handle(data, 0)
               if "موفقیت" in result:
                    return response.redirect("/questions")
               else:
                    context = {
                         'mode': 'add',
                         'question_json': 'null',
                         'answers_json': 'null',
                         'base_url': settings.BASE_URL,
                         'error': result
                    }
                    html = response.render_master("question-form.html", context, "افزودن سوال")
                    return response.serve_html(html)

          case ("/question/edit", "GET") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               question = question_get_one.handle(item_id)
               if not question:
                    return response._404()
               answers = answer_get_by_question.handle(item_id)
               
               question_json = json.dumps(question, ensure_ascii=False)
               answers_json = json.dumps(answers, ensure_ascii=False)
               question_id_json = json.dumps(question['id'])
               
               context = {
                    'question_json': question_json,
                    'answers_json': answers_json,
                    'question_id_json': question_id_json,
                    'base_url': settings.BASE_URL,
                    'error': '' 
               }
               html = response.render_master("question-edit.html", context, "ویرایش سوال")
               return response.serve_html(html)

          case ("/question/edit", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               
               answers_json = data.get('answers', [''])[0]
               answers = []
               if answers_json:
                    try:
                         answers = json.loads(answers_json)
                    except:
                         pass
               data['answers'] = answers
               
               result = question_update.handle(item_id, data)
               if "موفقیت" in result or "ویرایش" in result:
                    return response.redirect("/questions")
               else:
                    question = question_get_one.handle(item_id)
                    answers = answer_get_by_question.handle(item_id)
                    question_json = json.dumps(question, ensure_ascii=False)
                    answers_json = json.dumps(answers, ensure_ascii=False)
                    question_id_json = json.dumps(question['id'])
                    context = {
                         'question_json': question_json,
                         'answers_json': answers_json,
                         'question_id_json': question_id_json,
                         'base_url': settings.BASE_URL,
                         'error': result
                    }
                    html = response.render_master("question-edit.html", context, "ویرایش سوال")
                    return response.serve_html(html)

          case ("/question/delete", "POST") if item_id is not None:
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = question_delete.handle(item_id, user_id)
               if "موفقیت" in result or "حذف" in result:
                    return response.redirect("/questions")
               return response._200(result)

          case ("/question/import", "GET"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               html = response.render_master("question-import.html", {
                    'base_url': settings.BASE_URL
               }, "بارگذاری سوالات")
               return response.serve_html(html)

          case ("/question/import", "POST"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = question_import.handle(data, user_id)
               if "موفقیت" in result:
                    return response.redirect("/questions")
               return response._200(result)

          case ("/question/export", "GET"):
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               return question_export.handle(user_id)

          # ---------- مدیریت گزینه‌ها (برای سوالات تستی) ----------
          case ("/answer/add", "POST") if item_id is not None:  # item_id = question_id
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               result = answer_add.handle(data, item_id)
               return response.redirect(f"/question/edit/{item_id}")

          case ("/answer/delete", "POST") if item_id is not None:  # item_id = answer_id
               if not user_id or user_role not in ['admin', 'teacher']:
                    return response._403()
               answer_delete.handle(item_id)
               # برای بازگشت به صفحه ویرایش سوال، باید question_id را داشته باشید
               # بهتر است از referer استفاده کنید یا در فرم hidden field بگذارید
               return response.redirect(request.headers.get('Referer', '/questions'))

          # ---------- استاتیک و ۴۰۴ ----------
          case _ if clean_path.startswith("/static/"):
               return response.serve_static_file(clean_path)

          case _:
               return response._404()