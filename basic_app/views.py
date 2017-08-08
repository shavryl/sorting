# -*- coding: utf8 -*-
import os
from django.conf import settings
import json

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.template.response import TemplateResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ProfileForm, UserPasswordChangeForm
from .models import Profile, MyVeroKey
from django.contrib.auth.forms import PasswordChangeForm

from django.http import HttpResponse
from .resources import ProfileResource
from tablib import Dataset
from django.shortcuts import render, get_object_or_404, resolve_url

from .forms import UserForm, VeroKeyForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect

import csv





class IndexView(TemplateView):
    template_name = 'basic_app/index.html'



class SettingsView(LoginRequiredMixin,TemplateView):
    template_name = 'basic_app/user_settings.html'

    def get_context_data(self, **kwargs):
        data = MyVeroKey.objects.filter(user=self.request.user).values('verokey', 'id')
        if data:
            return data[0]
        return {'id': '', 'verokey': ''}



class UsersList110(LoginRequiredMixin,TemplateView):
    template_name = 'basic_app/users_list_1_10.html'


class UsersList110Json(LoginRequiredMixin, BaseDatatableView):
    def get_columns(self):
        return super().get_columns()

    model = Profile
    columns = ['name', 'lastname', 'city', 'country', 'phonenumber', 'email', 'date_of_birth', 'date_of_addition', 'id']
    order_columns = ['name', 'lastname', 'city', 'country', 'phonenumber', 'email', 'date_of_birth', 'date_of_addition', 'id']


    def filter_queryset(self, qs):
        qs = qs.filter(Q(user=self.request.user))
        sSearch_2 = self.request.GET.get('sSearch_2', None)
        sSearch_3 = self.request.GET.get('sSearch_3', None)
        if sSearch_2:
            qs = qs.filter(city=sSearch_2)
        if sSearch_3:
            qs = qs.filter(country=sSearch_3)

        return qs




class TableSortData(ListView):

    def get(self, request, *args, **kwargs):
        # result={'city':None, 'country':None}
        result = {}
        data = Profile.objects.filter(user=request.user).values('city').distinct()
        result['city'] = [u['city'] for u in data]

        data = Profile.objects.filter(user=request.user).values('country').distinct()
        result['country'] = [u['country'] for u in data]

        return JsonResponse(result)


@login_required
@csrf_protect
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
    else:
        form = ProfileForm()
    return save_profile_form(request, form, 'basic_app/partial_profile_create.html')


@csrf_protect
def save_profile_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            add = form.save(commit=False)
            add.user = request.user
            add.save()
        data['form_is_valid'] = True
        profiles = Profile.objects.all()
        data['html_profile_list'] = render_to_string('basic_app/users_list_1_10.html', {
            'profiles': profiles
        })
    else:
        data['form_is_valid']= False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



@csrf_protect
def profile_update(request):
    data = dict()
    pk = request.POST.get('pk')
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            add = form.save(commit=False)
            add.user = request.user
            add.save()
        data['form_is_valid'] = True
        profiles = Profile.objects.all()
        data['html_profile_list'] = render_to_string('basic_app/users_list_1_10.html', {
            'profiles': profiles
        })
    else:
        data['form_is_valid']= False
    context = {'form': form}
    data['html_form'] = render_to_string(context, request=request)
    return JsonResponse(data)




class ProfileHandsome(LoginRequiredMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        result = dict()
        pk = request.GET.get('pk',None)
        if request.method == 'GET' and pk:
            data = Profile.objects.filter(id=pk, user=request.user).values('name', 'lastname', 'city', 'country', 'phonenumber', 'email', 'date_of_birth')
            result = data[0]
        return JsonResponse(result)

    def post(self, *args, **kwargs):
        request = self.request
        form = ProfileForm(request.POST)
        msg=""
        status=200
        try:
            currentProfile = Profile.objects.filter(id=request.POST['id'], user=request.user)
            if not currentProfile.exists():
                raise Exception("You don't have this profile")

            if not form.is_valid():
                raise Exception("Form not valid")

            currentProfile.update(**form.cleaned_data)

        except Exception as e:
            msg = str(e)
            status = 400

        return HttpResponse(json.dumps(msg), status=status, content_type="application/json")






def register(request):
# remove
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)


        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'basic_app/registration.html',{'user_form':user_form,'registered':registered})



class ProfileDelete(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        status=200
        msg=''
        pk = request.POST.get('pk')
        profile = get_object_or_404(Profile, pk=pk)
        if request.method == 'POST':
            try:
                currentProfile = Profile.objects.filter(id=request.POST['pk'], user=request.user)
                if not currentProfile.exists():
                    raise Exception("You don't have this profile")
                currentProfile.delete()
            except Exception as e:
                msg = str(e)
                status=400

            return HttpResponse(json.dumps(msg), status=status, content_type="application/json")



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('basic_app:index'))

            else:
                return HttpResponse("Account not active")
        else:
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'basic_app/user_login.html',{})



@login_required
def export(request):
    profile_resource = ProfileResource()
    queryset = Profile.objects.filter(user=request.user)
    dataset = profile_resource.export(queryset=queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'
    return response



@csrf_protect
def import_data(request):
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        with open('media/' + myfile.name) as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i > 0:
                    _, created = Profile.objects.get_or_create(
                        user=request.user,
                        name=row[0],
                        lastname=row[1],
                        city=row[2],
                        country=row[3],
                        phonenumber=row[4],
                        email=row[5],
                        date_of_birth=row[6] if row[6] else None,
                        date_of_addition=row[7])

            os.remove('media/' + myfile.name)

        return render(request, 'basic_app/users_list_1_10.html')





@csrf_protect
@login_required
def password_change(request):

    if request.method == "POST":
        form = UserPasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            update_session_auth_hash(request, form.user)
            form.save()
            return redirect('basic_app:user_settings')

        else:
            return redirect('basic_app:user_settings')

    else:
        form = UserPasswordChangeForm(user=request.user)

    context = {
        'form': form,
        'title': ('Password was changed'),
    }

    return render(request, 'basic_app/user_settings.html', context)







@csrf_protect
@login_required
def vero_key_create(request):
    form = VeroKeyForm()
    if request.method == 'POST':
        form = VeroKeyForm(data=request.POST)
        if form.is_valid():
            verokey = form.save(commit=False)
            if form.cleaned_data['id']:
                verokey.id = form.cleaned_data['id']
            verokey.user = request.user
            verokey.save()

        return redirect('/settings/')



def vero_add_profiles(request):
    from vero import VeroEventLogger


    context = ''

    if request.method == 'GET':
        try:
            auth_token = MyVeroKey.objects.filter(user=request.user)

            if not auth_token[0].verokey:
                raise Exception("Fill in get vero token form")

            currentProfile = Profile.objects.filter(user=request.user)
            if not currentProfile.exists():
                raise Exception("You don't have this profile")


            for profile in currentProfile:
                user_data = {
                    'name': profile.name,
                    'lastname': profile.lastname,
                    'city': profile.city,
                    'country': profile.country,
                    'phonenumber': profile.phonenumber,
                }
                logger = VeroEventLogger(auth_token[0].verokey)
                logger.add_user(profile.id, user_data, user_email=profile.email)



            context = {
                'title': 'Profiles data was send to vero account'
            }

        except Exception as e:
            msg = str(e)
            context = {
            'title': "Profiles data was not send to vero account :'("
        }

    return TemplateResponse(request, "basic_app/user_settings.html", context)



