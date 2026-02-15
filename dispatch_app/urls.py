"""
URL routing for the dispatch_app application.
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views, api_views

# Router to register views and api_views
router = DefaultRouter()
router.register(
    r'articles', api_views.ArticleViewSet, basename='article-api'
)

urlpatterns = [
    # Website Paths
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.ArticleListView.as_view(), name='article_list'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Explicitly directing login/logout to use your app's templates
    path('login/', auth_views.LoginView.as_view(
        template_name='dispatch_app/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Journalist-specific paths
    path('dashboard/', views.JournalistDashboardView.as_view(),
         name='journalist_dashboard'),
    path('article/new/', views.ArticleCreateView.as_view(),
         name='article_create'),
    path('article/<int:pk>/edit/', views.ArticleUpdateView.as_view(),
         name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(),
         name='article_delete'),
    path('newsletter/new/', views.NewsletterCreateView.as_view(),
         name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', views.NewsletterUpdateView.as_view(),
         name='newsletter_update'),
    path('newsletter/<int:pk>/delete/', views.NewsletterDeleteView.as_view(),
         name='newsletter_delete'),
    # Publisher paths
    path('publishers/', views.PublisherListView.as_view(),
         name='publisher_list'),
    path('publishers/new/', views.PublisherCreateView.as_view(),
         name='publisher_create'),
    path('publishers/<int:pk>/join/', views.join_publisher,
         name='publisher_join'),
    # Editor-specific paths
    path('editor/dashboard/', views.EditorDashboardView.as_view(),
         name='editor_dashboard'),
    path('article/<int:pk>/approve/', views.approve_article,
         name='approve_article'),
    path('article/<int:pk>/reject/', views.reject_article,
         name='reject_article'),
    # Reader-specific paths
    path('subscriptions/', views.SubscriptionsView.as_view(),
         name='subscriptions'),
    path('newsletters/', views.NewsletterListView.as_view(),
             name='newsletter_list'),
    path(
        'article/<int:pk>/',
        views.ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path('api/', include(router.urls)),
]
