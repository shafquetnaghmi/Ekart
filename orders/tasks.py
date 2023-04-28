from django.core.mail import send_mail
from .models import Order
from celery import shared_task

@shared_task
def order_created(order_id):
    order=Order.objects.get(id=order_id)
    subject = 'order confirmed on Ekart'
    message=f'Dear {order.first_name}  {order.last_name} \n\n' \
            f'You have successfully placed an order \n\n' \
            f'Order id is {order.id} \n\n' \
            f'Thank You for shopping with us'
    return send_mail(subject,message,'abcxyzalpha42@gmail.com',[order.email],fail_silently=False)
                                                                                   