from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem


# from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #aktyvuojam user
            current_site = get_current_site(request)
            mail_subject = "Aktyvuokite savo paskyrą"
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)


                    # product_variation = []
                    # for item in cart_item:
                    #     variation = item.variations.all()
                    #     product_variation.append(list(variation))
                    #
                    # cart_item = CartItem.objects.filter(user=user)
                    # ex_var_list = []
                    # id = []
                    # for item in cart_item:
                    #     existing_variation = item.variations.all()
                    #     ex_var_list.append(list(existing_variation))
                    #     id.append(item.id)
                    #
                    # for pr in product_variation:
                    #     if pr in ex_var_list:
                    #         index = ex_var_list.index(pr)
                    #         item_id = id[index]
                    #         item = CartItem.objects.get(id=item_id)
                    #         item.quantity += 1
                    #         item.user = user
                    #         item.save()
                    #     else:
                    #         cart_item = CartItem.objects.filter(cart=cart)
                    #         for item in cart_item:
                    #             item.user = user
                    #             item.save()
                    for item in cart_item:
                        item.user = user
                        item.save()
                        # print(f"spausdinam {item}")

            except:
                pass
            auth.login(request, user)
            messages.success(request, "Jūs prisijungėte!")
            return redirect('home')
        else:
            messages.error(request, "Jums nepavyko prisijungti!")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Sėkmingai atsijungėte!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Sveikiname! Jūsų paskyra aktyvuota.')
        return redirect('login')
    else:
        messages.error(request, 'Jūsų paskyros aktyvuoti nepavyko. Bandykite dar kartą!')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = "Slaptažodžio priminimas"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Slaptažodžio priminimas išsiųstas!")
            return redirect('login')
        else:
            messages.error(request, 'Jūs neturite paskyros!')
            return redirect('register')

    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request, 'Atnaujinkite savo slaptažodį')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Šios nuorodos galiojimo laikas baigėsi!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Slaptažodis atnaujintas, galite prisijungti! ")
            return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('resetPassword')

    else:
        return render(request, 'accounts/resetPassword.html')