from django import forms
from django.utils import timezone
from .service import itemIter
import datetime
from .models import User

genders = [
    (0,'男性'),
    (1,'女性'),
    (2,'その他')
]

bloodtypes = [
    ('a','A型'),
    ('b','B型'),
    ('o','O型'),
    ('ab','AB型'),
    ('etc','不明')
]

learnings = [
    ('j','JAVA'),
    ('p','PHP'),
    ('h','HTML'),
    ('d','デザイン')
]

class ProfileForm(forms.Form):
    name = forms.CharField(label="名前", required=True,max_length=20,widget=forms.DateInput(attrs={"class":"form-control"}))
    birthday = forms.DateTimeField(label="誕生日",required=True,widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
    gender = forms.ChoiceField(label="性別",required=True,widget=forms.RadioSelect,choices=genders,initial=0)
    bloodtype = forms.fields.ChoiceField(label="血液型",required=True,widget=forms.widgets.Select(attrs={'class': 'form-select form-select-lg'}),choices=bloodtypes)
    learning = forms.MultipleChoiceField(label="学習内容",initial=['j','p'],required=True,choices=learnings, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select form-select-lg'}                                                                                                                 ))
    remark = forms.CharField(label="備考",required=True,widget=forms.Textarea(attrs={"class":"form-control"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields['learning'].initial)
    # 期限日に対するバリデーション
    # 形式に合わないデータであればエラー
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        try:
            birthday = birthday.strftime('%Y/%m/%d')
        except:
            if birthday is None:
                self.add_error('birthday', '期限日が入力されていません')
            else:
                self.add_error('birthday', '日付の形式で入力してください')
        return birthday
    # 備考が100文字を超えていたらエラー
    def clean_remark(self):
        remark = self.cleaned_data.get('remark')
        if len(remark) > 100:
            self.add_error('remark', '100文字以内で入力してください')
    # 性別を男女に変換
    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        iter = itemIter(genders)
        gender = iter.search(gender)
        return gender
    # 血液型を変換
    def clean_bloodtype(self):
        bloodtype = self.cleaned_data.get('bloodtype')
        iter = itemIter(bloodtypes)
        bloodtype = iter.search(bloodtype)
        return bloodtype
    # 学習内容を変更
    def clean_learning(self):
        learning = self.cleaned_data.get('learning')
        iter = itemIter(learnings)
        learning = iter.searchLearning(learning)
        return learning

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name','team')
        labels = {
            'name': '名前',
            'team': 'チーム',
        }
        # 基本的なバリデーション
        error_messages = {
            "name": {
                "required": "項目名が入力されていません",
            },
            "team": {
                "required": "担当者名が入力されていません",
            },
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
    def clean_name(self):
        name = self.cleaned_data.get('name')
        nameresult = self.Meta.model.objects.filter(name=name)
        if len(nameresult):
            self.add_error('name', 'この名前はすでに登録されています')
        return name