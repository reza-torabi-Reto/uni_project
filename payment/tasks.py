from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    print('COMPLETE--01')
    order = Order.objects.get(id=order_id)
    print('COMPLETE--02')
    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    print('COMPLETE--03')
    out = BytesIO()
    print('COMPLETE--04')
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    print('COMPLETE--05')
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    print('COMPLETE--06')
    # attach PDF file
    # email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    print('COMPLETE--07')
    # send e-mail
    email.send()
    print('COMPLETE--08')
