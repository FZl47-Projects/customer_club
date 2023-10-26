from django.contrib import messages
from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q, Value
from django.db.models.functions import Concat
from apps.account.models import User
from apps.account.auth.decorators import user_role_required_cbv
from apps.club.models import ClubInfo, ClubConfig
from apps.core.utils import form_validate_err, random_str, add_prefix_phonenum
from . import forms, models


class Dashboard(LoginRequiredMixin, View):
    TEMPLATES_ROLE = {
        'admin_user': 'club/dashboard/admin.html',
        'operator_user': 'club/dashboard/operator.html',
    }
    CONTEXT_ROLE_HANDLER = {
        'admin_user': 'context_handler_admin_user',
        'operator_user': 'context_handler_operator_user',
    }

    @classmethod
    def context_handler_admin_user(cls, request):

        def search(users):
            search_q = request.GET.get('search', None)
            if not search_q:
                return users
            users = users.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            lookup = Q(phonenumber__icontains=search_q) | Q(full_name__icontains=search_q)
            users = users.filter(lookup)
            return users

        users = User.normal_user.all()
        # search in users
        users = search(users)
        return {
            'club_info': ClubInfo.objects.first(),
            'club_config': ClubConfig.objects.first(),
            'users': users,
        }

    @classmethod
    def context_handler_operator_user(cls, request):

        def get_user():
            search_q = request.GET.get('search', None)
            if not search_q:
                return None
            try:
                return User.normal_user.get(phonenumber=add_prefix_phonenum(search_q))
            except User.DoesNotExist:
                return None

        user = get_user()
        context = {
            'user_searched': user
        }
        return context

    def get_context_by_role(self, request):
        handler_name = self.CONTEXT_ROLE_HANDLER.get(request.user.role, None)
        if not handler_name:
            raise ValueError('You must define context handler for the role or Context handler name is not correct')
        handler = getattr(self, handler_name, None)
        if not handler:
            raise ValueError('You must define context handler for the role or Context handler is not defined')
        return handler(request)

    def get_template_by_role(self, request):
        t = self.TEMPLATES_ROLE.get(request.user.role, None)
        if not t:
            raise Http404
        return t

    def get(self, request):
        template = self.get_template_by_role(request)
        context = self.get_context_by_role(request)
        return render(request, template, context)


class TransactionAdd(View):

    def get_or_create_user(self, data):
        phonenumber = data.get('phonenumber')
        try:
            user = User.normal_user.get(phonenumber=add_prefix_phonenum(phonenumber))
        except User.DoesNotExist:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user = User.objects.create(phonenumber=phonenumber, password=random_str(15), first_name=first_name,
                                       last_name=last_name)
        return user

    @user_role_required_cbv(['operator_user'])
    def post(self, request):
        data = request.POST.copy()
        # validation fields
        f = forms.TransactionAddForm(data)
        if form_validate_err(request, f) is False:
            return redirect('club:dashboard')
        data = f.cleaned_data
        user = self.get_or_create_user(data)
        wallet = user.get_wallet()
        amount = data.get('amount')
        amount_refund = models.Transaction.get_amount_refund(amount)
        models.Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            amount_refund=amount_refund,
            discount_percentage=models.Transaction.get_discount_percentage()
        )
        # update amount wallet
        wallet.amount += amount_refund
        wallet.save()
        messages.success(request, 'تراکنش خرید با موفقیت ثبت شد')
        return redirect('club:dashboard')


class WithdrawWallet(LoginRequiredMixin, View):

    @user_role_required_cbv(['operator_user'])
    def post(self, request, user_id):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST
        user = get_object_or_404(User, id=user_id)
        wallet = user.get_wallet()
        amount = data.get('amount')
        # validation fields
        if (not amount) or (not amount.isdigit()):
            messages.error(request, 'لطفا فیلد مبلغ را به درستی پر نمایید')
            return redirect(referer_url)
        amount = int(amount)
        # check wallet amount
        if amount > wallet.amount:
            messages.error(request, 'موجودی کیف پول کافی نیست')
            return redirect(referer_url)
        # set new amount
        wallet.amount -= amount
        wallet.save()
        messages.success(request, 'مبلغ با موفقیت از کیف پول کسر شد')
        return redirect(referer_url)
