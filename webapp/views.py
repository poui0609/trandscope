import json

from django.http import JsonResponse
from django.utils import timezone, translation
import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import MainNews, RecentKeyword, UserFavoriteKeywords
from itertools import groupby


# Create your views here.

def get_data() :
    news = MainNews.objects.all()
    return news

def userPage(request):
    
    return render(request, 'webapp/userPage.html')
    
def page2(request, category_id):
    news_data = MainNews.objects.filter(category=category_id).order_by('ranking')
    
    grouped_rank_data = []
    for key, group in groupby(news_data, key=lambda x: x.ranking):
        group_list = list(group)
        if all(item.img_link == '0' for item in group_list):
            grouped_rank_data.append(group_list[0])
        else:
            for item in group_list:
                if item.img_link != '0':
                    grouped_rank_data.append(item)
                    break

    context = {
        'news_data': grouped_rank_data,
        'category_name': get_category_name(category_id), 
    }
    return render(request, 'webapp/page2.html', context)

def get_category_name(category_id):
    categories = {
        0: "정치",
        1: "경제",
        2: "사회",
        3: "생활/문화",
        4: "세계",
        5: "IT/과학",
    }
    return categories.get(category_id, "Unknown")


def page1(request):
    news = get_data()
    rank_data = MainNews.objects.filter(ranking__gte=1, ranking__lte=5).order_by('ranking')

    grouped_rank_data = []
    for key, group in groupby(rank_data, key=lambda x: x.ranking):
        group_list = list(group)
        if all(item.img_link == '0' for item in group_list):
            grouped_rank_data.append(group_list[0])
        else:
            for item in group_list:
                if item.img_link != '0':
                    grouped_rank_data.append(item)
                    break

    if request.user.is_authenticated:
        favorite_keywords = UserFavoriteKeywords.objects.filter(user=request.user)
        favorite_keywords_set = json.dumps([fav.keyword for fav in favorite_keywords])  # JSON 문자열로 변환
    else:
        favorite_keywords_set = json.dumps([])  # 빈 리스트 반환

    now = timezone.now()
    with translation.override('en'):
        context = {
            'current_date': now,
            'news_data': grouped_rank_data,
            'favorite_keywords_set': favorite_keywords_set
        }
        return render(request, 'webapp/page1.html', context)


# 사용자 정의 폼 클래스
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("이름에는 숫자가 포함될 수 없습니다.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError("이름에는 숫자가 포함될 수 없습니다.")
        return last_name

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('page1')  # 로그인 후 page1.html로 리디렉션
        else:
            return render(request, 'webapp/userpage.html', {
                'login_error': '존재하지 않는 아이디 또는 비밀번호입니다!'
            })
    return render(request, 'webapp/userpage.html')


def logout_view(request):
    logout(request)
    return redirect('page1')  # 로그아웃 후 리디렉션할 페이지

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            if User.objects.filter(username=username).exists():
                return render(request, 'webapp/userpage.html', {
                    'signup_error': '중복되는 아이디입니다!',
                    'form': form
                })
            elif User.objects.filter(email=email).exists():
                return render(request, 'webapp/userpage.html', {
                    'signup_error': '중복되는 이메일입니다!',
                    'form': form
                })
            elif password1 != password2:
                return render(request, 'webapp/userpage.html', {
                    'signup_error': '비밀번호가 일치하지 않습니다!',
                    'form': form
                })
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)

                # 사용자 로그인 처리
                login(request, user)

                # 사용자 이름으로 빈 찜 목록 생성

                return redirect('page1')  # 회원가입 후 page1.html로 리디렉션
        else:
            return render(request, 'webapp/userpage.html', {
                'signup_error': form.errors,
                'form': form
            })
    else:
        form = SignUpForm()
    return render(request, 'webapp/userpage.html', {'form': form})


def page3(request, ranking_id):
    news_data = MainNews.objects.filter(ranking=ranking_id).order_by('ranking')

    grouped_rank_data = []
    for key, group in groupby(news_data, key=lambda x: x.ranking):
        group_list = list(group)
        if all(item.img_link == '0' for item in group_list):
            grouped_rank_data.append(group_list[0])
        else:
            for item in group_list:
                if item.img_link != '0':
                    grouped_rank_data.append(item)
                    break

    now = timezone.now()
    context = {
        'current_date': now.strftime("%A, %B %d"),
        'news_data': grouped_rank_data,
    }

    return render(request, 'webapp/page3.html', context)


@login_required
def add_favorite_keyword(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        title = request.POST.get('title')
        content = request.POST.get('content')
        url = request.POST.get('url')
        user = request.user

        if not (keyword and title and content and url): return JsonResponse(
            {'status': 'error', 'message': 'Missing required fields'}, status=400)

        # 이미 찜한 키워드가 존재하는지 확인
        if UserFavoriteKeywords.objects.filter(user=user, keyword=keyword).exists():
            return JsonResponse({'status': 'error', 'message': 'Keyword already exists'}, status=400)

        # 찜한 키워드 개수 제한
        if UserFavoriteKeywords.objects.filter(user=user).count() >= 15:
            oldest_favorite = UserFavoriteKeywords.objects.filter(user=user).first()
            if oldest_favorite:
                oldest_favorite.delete()


        # 새로운 찜한 키워드 저장
        UserFavoriteKeywords.objects.create(user=user, username=user.username, keyword=keyword, title=title, content=content, url=url)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



@login_required
def remove_favorite_keyword(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        user = request.user

        favorite = UserFavoriteKeywords.objects.filter(user=user, keyword=keyword).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Keyword not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def add_recent_keyword(request):
    if request.method == 'POST':
        user = request.user
        keyword = request.POST.get('keyword')
        title = request.POST.get('title')
        content = request.POST.get('content')
        url = request.POST.get('url')

        existing_keyword = RecentKeyword.objects.filter(user=user, keyword=keyword).first()
        if existing_keyword:
            existing_keyword.delete()

        if RecentKeyword.objects.filter(user=user).count() >= 15:
            oldest_keyword = RecentKeyword.objects.filter(user=user).first()
            if oldest_keyword:
                oldest_keyword.delete()

        RecentKeyword.objects.create(user=user, keyword=keyword, title=title, content=content, url=url)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def page3(request, ranking_id):
    news_data = MainNews.objects.filter(ranking=ranking_id).order_by('ranking')

    grouped_rank_data = []
    for key, group in groupby(news_data, key=lambda x: x.ranking):
        group_list = list(group)
        if all(item.img_link == '0' for item in group_list):
            grouped_rank_data.append(group_list[0])
        else:
            for item in group_list:
                if item.img_link != '0':
                    grouped_rank_data.append(item)
                    break

    now = timezone.now()
    context = {
        'current_date': now.strftime("%A, %B %d"),
        'news_data': grouped_rank_data,
    }

    return render(request, 'webapp/page3.html', context)
