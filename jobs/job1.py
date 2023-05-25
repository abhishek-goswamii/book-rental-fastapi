from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_book_rental_expiring_email,send_book_rental_due_amount_mail

scheduler = BackgroundScheduler()
scheduler.add_job(send_book_rental_expiring_email, 'cron',
                  day_of_week='mon-sun', hour=0, minute=0, second=0)

scheduler.add_job(send_book_rental_due_amount_mail, 'cron',
                  day_of_week='mon-sun', hour=0, minute=0, second=0)