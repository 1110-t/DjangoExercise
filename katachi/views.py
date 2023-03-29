from django.shortcuts import render,redirect
from .forms import ProfileForm
from .forms import UserForm
from .models import User
# リダイレクト、レスポンス、戻る処理
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, 'katachi/index.html', {})
def input(request):
    name = ''
    form = ProfileForm()
    if request.method == "GET":
        if "name" in request.GET:
            name = request.GET['name']
        return render(request, 'katachi/input.html', {"form":form})
    elif request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'changed_birthday': form.cleaned_data['birthday'],
                'changed_gender': form.cleaned_data['gender'],
                'changed_bloodtype': form.cleaned_data['bloodtype'],
                'changed_learning' : form.cleaned_data['learning'],
            }
            for field in form:
                if field.label == '学習内容':
                    for item in field:
                        print(context["changed_learning"])
            return render(request, 'katachi/profile.html', context)
        else:
            return render(request, 'katachi/input.html', {'form': form})
def user(request):
    users = User.objects.all()
    user = User.objects.get(pk=1)
    print(user.name)
    context = {"users":users}
    return render(request,'katachi/user.html',context)
def user_add(request):
    form = UserForm()
    for field in form:
        print(field)
    if request.method == "GET":
        return render(request, 'katachi/user_add_form.html', {"form":form})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            return redirect('/user')
        else:
            return render(request, 'katachi/user_add_form.html', {"form":form})
def user_delete(request,number):
    if request.method == "GET":
        print(number)
        user = User.objects.get(pk=number)
        user.delete()
        return redirect('/user')