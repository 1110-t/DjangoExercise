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
    # GETパラメータを使ってみましょう
    if request.method == "GET":
        # GETパラメータ
        # if "name" in request.GET: # nameパラメータから値を取得
        #     name = request.GET['name']
        # return render(request, 'katachi/input.html', {"name":name})
        return render(request, 'katachi/input.html', {"form":form,"name":name})
    # POSTパラメータを使ってみましょう
    elif request.method == "POST":
        # POSTパラメータ
        # if "name" in request.POST: # nameパラメータから値を取得
        #     name = request.POST['name']
        # return render(request, 'katachi/profile.html', {"name":name})

        # フォームオブジェクトを生成
        form = ProfileForm(request.POST)
        # バリデーションを行う
        if form.is_valid():
            context = {
                'form': form,
                'changed_birthday': form.cleaned_data['birthday'],
                'changed_gender': form.cleaned_data['gender'],
                'changed_bloodtype': form.cleaned_data['bloodtype'],
                'changed_learning' : form.cleaned_data['learning'],
            }
            return render(request, 'katachi/profile.html', context)
        # バリデーションにエラーが生じた場合、入力画面に戻す
        else:
            return render(request, 'katachi/input.html', {'form': form})
# プロジェクトからデータベースの利用
def user(request):
    users = User.objects.all() # ユーザーをすべて取得する
    context = {"users":users} # ユーザーを全て表示する
    return render(request,'katachi/user.html',context)
# ユーザー登録
def user_add(request):
    # フォームオブジェクトを生成
    form = UserForm()
    # ユーザー追加画面を表示する
    if request.method == "GET":
        return render(request, 'katachi/user_add_form.html', {"form":form})
    # ユーザーをテーブルに追加する
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save() # テーブルに保存する
            return redirect('/user')
        else:
            # バリデーションにエラーが生じた場合、入力画面に戻す
            return render(request, 'katachi/user_add_form.html', {"form":form})
def user_delete(request,number):
    if request.method == "GET":
        print(number)
        user = User.objects.get(pk=number)
        user.delete()
        return redirect('/user')