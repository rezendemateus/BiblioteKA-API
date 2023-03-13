from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


def reminder_devolution():
    loans = Loan.objects.all()

    for loan in loans:
        reminder_day = loan.loan_term_at
        user_email = loan.user.email
        day_before = timezone.now() + timedelta(days=1)

        if reminder_day.day is day_before.day:
            send_mail(
                subject="ATENÇÃO: Lembrete de devolução!",
                message="O livro que você emprestou"
                f' "{loan.copy.book.title}" '
                "deve ser devolvido até amanhã! Lembre-se: há taxa de multa caso não seja devolvido no dia, e esse valor é atualizado diariamente! Caso precise de mais tempo, renove seu empréstimo!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )

        elif reminder_day.day < timezone.now().day:
            send_mail(
                subject="ATENÇÃO: Você possui livro(s) em atraso!",
                message="O livro que você emprestou"
                f' "{loan.copy.book.title}" '
                "já deveria ter sido devolvido! Lembre-se: há multa por atraso na devolução e você pode renovar o empréstimo!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )


scheduler = BackgroundScheduler()
scheduler.add_job(
    reminder_devolution,
    "cron",
    day_of_week="mon-fri",
    hour=10,
)

scheduler.start()
