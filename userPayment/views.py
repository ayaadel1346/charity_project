from django.shortcuts import render,reverse
from paypal.standard.forms import PayPalPaymentsForm
import project
from .models import Payment
from project.models import *
from charityProject.settings import PAYPAL_RECEIVER_EMAIL


def payment(request):

    if request.method == 'POST':
        form = PayPalPaymentsForm(request.POST)
        if form.is_valid():
            payment = Payment(
                amount=form.cleaned_data['amount'],
                item_name=form.cleaned_data['item_name'],
                currency_code=form.cleaned_data['currency_code'],
                invoice=form.cleaned_data['invoice'],
                custom=form.cleaned_data['custom']
            )
            payment.save()
            return render(request, 'success.html')
    else:
        paypal_dict = {
            
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": "100.00",
            "currency_code": "USD",
            "item_name": "name of the item",
            "invoice": "unique-invoice-id",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('project:appView')),
            "cancel_return": request.build_absolute_uri(reverse('payment:cancelled')),
        }
        form = PayPalPaymentsForm()

    context = {"form": form}
    return render(request, "payment.html", context)



def payment_failed(request):
    return render(request, 'cancel.html')


def paypal_ipn(request):
   
    pass
