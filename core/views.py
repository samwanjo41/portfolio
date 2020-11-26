from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import Project, Customer
from django.core.mail import send_mail
from django.conf import settings
import stripe


stripe.api_key = 'sk_test_1XN35gre899TYyVxQJitxGO8'


def home(request):    
    if request.method == 'POST':
        message = request.POST['message']
        email_from = request.POST['email']
        sender_name = request.POST['name']
        try:
            send_mail(
                'Contact Form',
                message,
                email_from,
                ['samwanjo41@zohomail.com'],
                fail_silently=False)   
            return redirect('home')     
        except AssertionError:
            pass
     
    projects = Project.objects.all()	 
    context = {
        'projects':projects
    }
    return render(request, 'home.html', context)

def premium(request):
     return render(request, 'premium.html')


@login_required
def project(request,pk):
    project = get_object_or_404(Project, pk=pk)
    if project.premium:
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                    return render(request, 'project.html', {'project':project})
            except Customer.DoesNotExist:
                return redirect('premium')
        
        return redirect('premium')
    else:
        return render(request, 'project.html', {'project':project})
          
@login_required
def checkout(request):    
    coupons = {'halloween':31, 'welcome':10}
    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        price = 'price_1Hr0NiHL9iQ6q7Am5aEciPLv'
        
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(),
                percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'price':price}], coupon=request.POST['coupon'].lower())
        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'price':price}])

        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()
        return redirect('home')
    else:
        coupon = 'none'
        plan = 'monthly'
        price = 1000
        og_dollar = 10
        coupon_dollar = 0
        final_dollar = 10        

        if request.method == 'GET' and 'coupon' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price = price - coupon_price
                coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + '.' + str(price)[-2:]


        return render(request, 'checkout.html',
        {'plan':plan,'coupon':coupon,'price':price,'og_dollar':og_dollar,
        'coupon_dollar':coupon_dollar,'final_dollar':final_dollar})
    return render(request, 'checkout.html')      


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project.html'