from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import schedule
import time


def reminder_devolution():
    loans = Loan.objects.all()

    for loan in loans:
        reminder_day = loan.loan_term_at - timedelta(days=1)
        user_email = loan.user.email
        if reminder_day.strftime("%d, %b, %Y") is timezone.now().strftime("%d, %b, %Y"):
            send_mail(
                subject="ATENÇÃO: Lembrete de devolução!",
                message="O livro que você emprestou"
                f' "{loan.copy.book.title}" '
                "deve ser devolvido até amanhã! Lembre-se: há taxa de multa caso não seja devolvido no dia, e esse valor é atualizado diariamente! Caso precise de mais tempo, renove seu empréstimo!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )
            print("roda a roda jequiti")


schedule.every().day.at("10:00").do(reminder_devolution)

while True:
    schedule.run_pending()
    print("roda")
    time.sleep(3600)
