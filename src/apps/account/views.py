from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout as logout_handler
from apps.core.utils import add_prefix_phonenum, random_num, form_validate_err
from apps.account.auth.decorators import user_role_required_cbv

User = get_user_model()


class Login(View):

    def get(self, request):
        return render(request,'account/login.html')

    def post(self, request):
        data = request.POST
        phonenumber = data.get('phonenumber', None)
        password = data.get('password', None)
        remember_me = data.get('remember_me')
        remember_me = True if remember_me == 'on' else False
        if not (phonenumber or password):
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:login')
        phonenumber = add_prefix_phonenum(phonenumber)
        user = authenticate(request, username=phonenumber, password=password)
        if user is None:
            messages.error(request, 'کاربری با این مشخصات یافت نشد یا حساب غیر فعال میباشد')
            return redirect('account:login')
        if user.is_active is False:
            messages.error(request, 'حساب شما غیر فعال میباشد')
            return redirect('account:login')
        login(request, user)
        # set session expire(remember me)
        if not remember_me:
            request.session.set_expiry(0)
        messages.success(request, 'خوش امدید')
        # redirect to url or dashboard
        next_url = request.GET.get('next')
        try:
            # maybe next url not valid
            if next_url:
                return redirect(next_url)
        except Exception as e:
            pass
        return redirect('club:dashboard')


class Logout(View):

    def get(self, request):
        logout_handler(request)
        return redirect('account:login')


class UserDetail(LoginRequiredMixin, View):
    template_name = 'account/user/detail.html'

    @user_role_required_cbv(['admin_user'])
    def get(self, request, user_id):
        context = {
            'user': get_object_or_404(User, id=user_id)
        }
        return render(request, self.template_name, context)
