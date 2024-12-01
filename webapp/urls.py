from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('', views.page1, name = 'page1'),
    path('page1', views.page1, name = 'page1'),
    path('page2/<int:category_id>/', views.page2, name = 'page2'),
    path('logout/', views.logout_view, name='logout'),
    path('userPage.html', views.userPage, name='userPage'),  # 기존 URL 패턴
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('add_favorite_keyword/', views.add_favorite_keyword, name='add_favorite_keyword'),
    path('remove_favorite_keyword/', views.remove_favorite_keyword, name='remove_favorite_keyword'),
    path('add_recent_keyword/', views.add_recent_keyword, name='add_recent_keyword'),
    path('page3/<int:ranking_id>/', views.page3, name = 'page3'),
]