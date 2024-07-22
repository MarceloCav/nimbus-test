import os
import json
import logging
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ReportForm
from .models import Report
from .utils import generate_random_weather_data, generate_pdf_report
from datareceiver.models import ReceivedData
from datetime import datetime

logger = logging.getLogger(__name__)

def create_report(request):
    if request.method == 'POST':
        logger.info('Create report POST request received')
        form = ReportForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')
            phones = form.cleaned_data['phones'].split(',')
            report_date = form.cleaned_data['report_date']
            send_email = form.cleaned_data['send_email']

            emails_sent = []
            emails_not_found = []

            for phone in phones:
                phone = phone.strip()
                try:
                    user = ReceivedData.objects.get(phone=phone)
                    logger.debug(f'User found: {user}')
                    name = user.name

                    weather_data = generate_random_weather_data()

                    base_dir = 'raw_data'
                    if not os.path.exists(base_dir):
                        os.makedirs(base_dir)
                    raw_data_path = os.path.join(base_dir, f'{phone}_{report_date}.json')

                    with open(raw_data_path, 'w') as f:
                        json.dump(weather_data, f)

                    pdf_dir = 'reports'
                    if not os.path.exists(pdf_dir):
                        os.makedirs(pdf_dir)
                    pdf_path = os.path.join(pdf_dir, f'{phone}_{report_date}.pdf')

                    generate_pdf_report(weather_data, pdf_path, name)

                    Report.objects.create(
                        phone=phone,
                        report_date=report_date,
                        raw_data_path=raw_data_path,
                        pdf_path=pdf_path
                    )

                    if send_email:
                        email = EmailMessage(
                            subject=f'Relatório para {datetime.now().strftime("%d/%m/%Y")}',
                            body=f'Prezado {user.name},\n\nPor favor, encontre em anexo o relatório referente à data {report_date}.',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[user.email],
                        )
                        email.attach_file(pdf_path)
                        email.send(fail_silently=False)
                        emails_sent.append(user.email)
                        logger.info(f'Email sent to: {user.email}')
                except ReceivedData.DoesNotExist:
                    emails_not_found.append(phone)
                    logger.warning(f'User with phone {phone} not found')

            return render(request, 'reports/report_success.html', {
                'emails_sent': emails_sent,
                'emails_not_found': emails_not_found,
                'phones': phones
            })
        else:
            logger.warning('Form is not valid')
    else:
        logger.info('Create report GET request received')
        form = ReportForm()

    return render(request, 'reports/create_report.html', {'form': form})
