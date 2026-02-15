"""
Views for the dispatch_app application.
Handles the logic for displaying articles and newsletters
on the website front-end.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.forms import ModelChoiceField
from .models import Article, CustomUser, Publisher, Newsletter


def approve_article(request, pk):
    """
    Function-based view that allows an editor to approve an article.
    Flips the 'is_approved' flag to True.
    """
    # Ensure the user is an editor
    if not request.user.is_authenticated or request.user.role != 'EDITOR':
        return redirect('home')

    article = get_object_or_404(Article, pk=pk)
    article.is_approved = True
    article.save()  # This triggers the signals for email and X posting
    return redirect('editor_dashboard')


def reject_article(request, pk):
    """
    Allows an editor to unpublish an article, moving it back to
    the review queue.
    """
    if not request.user.is_authenticated or request.user.role != 'EDITOR':
        return redirect('home')

    article = get_object_or_404(Article, pk=pk)
    article.is_approved = False
    article.save()
    return redirect('editor_dashboard')


@login_required
def join_publisher(request, pk):
    """
    Adds the current editor or journalist to the chosen publisher.
    """
    publisher = get_object_or_404(Publisher, pk=pk)
    user = request.user

    if user.role == "EDITOR":
        publisher.editors.add(user)
    elif user.role == "JOURNALIST":
        publisher.journalists.add(user)
    return redirect("publisher_list")


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration that includes the functional
    role selection.
    """
    class Meta:
        """Meta-configuration for the registration form."""
        model = CustomUser
        # admin is handled via createsuperuser; others register here.
        # Explicitly list the fields to satisfy the IDE and ensure
        # the 'role' is included alongside default fields.
        fields = ("username", "role")


class HomeView(TemplateView):
    """
    Displays the landing page of the application with options to
    register or log in.
    """
    template_name = 'dispatch_app/home.html'


class RegisterView(CreateView):
    """
    Handles user registration. Uses a custom form if needed,
    but for now, we extend the basic UserCreationForm.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'dispatch_app/register.html'


class AboutView(TemplateView):
    """
    Displays information about the Dispatch Django platform.
    """
    template_name = 'dispatch_app/about.html'


class ArticleListView(ListView):
    """
    Displays a list of all approved articles with search functionality.
    """
    model = Article
    template_name = 'dispatch_app/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """
        Retrieves articles, filtering by approval status and optional
        search query.
        """
        # Capture the search term from the "GET" request
        query = self.request.GET.get('q')

        # Start with the base queryset of approved articles
        queryset = Article.objects.filter(is_approved=True)

        if query:
            # Apply an OR filter across Title, Content, and Author name
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            )

        return queryset.order_by('-created_at')


class ArticleDetailView(DetailView):
    """
    Displays the full content of a single article.
    """
    model = Article
    template_name = 'dispatch_app/article_detail.html'


class JournalistDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Displays a list of articles authored by the logged-in journalist.
    """
    model = Article
    template_name = 'dispatch_app/journalist_dashboard.html'
    context_object_name = 'user_articles'

    def test_func(self):
        """Ensures only journalists can access this view."""
        return self.request.user.role == 'JOURNALIST'

    def get_queryset(self):
        """Retrieves only articles authored by the current user."""
        return Article.objects.filter(author=self.request.user)


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Allows journalists to submit new articles for approval.
    """
    model = Article
    template_name = 'dispatch_app/article_form.html'
    fields = ['title', 'content', 'publisher']
    success_url = reverse_lazy('journalist_dashboard')

    def test_func(self):
        """Ensures only journalists can create articles."""
        return self.request.user.role == 'JOURNALIST'

    def get_form(self, form_class=None):
        """Customizes the form labels and choice options."""
        form = super().get_form(form_class)
        # Cast the field to ModelChoiceField so PyCharm recognizes
        # the empty_label attribute.
        publisher_field = form.fields.get('publisher')
        # Changes the '---------' label to something more descriptive
        if isinstance(publisher_field, ModelChoiceField):
            publisher_field.empty_label = "Independent (No Publisher)"
        return form

    def form_valid(self, form):
        """Automatically assigns the logged-in user as the author."""
        # noinspection PyUnresolvedReferences
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows journalists to edit their own articles."""
    model = Article
    template_name = 'dispatch_app/article_form.html'
    fields = ['title', 'content', 'publisher']
    success_url = reverse_lazy('journalist_dashboard')

    def test_func(self):
        """Only the author (journalist) can edit their article."""
        return (
            self.request.user.role == 'JOURNALIST' and
            self.get_object().author == self.request.user
        )


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows journalists to delete their own articles."""
    model = Article
    template_name = 'dispatch_app/article_confirm_delete.html'
    success_url = reverse_lazy('journalist_dashboard')

    def test_func(self):
        """Only the author (journalist) can delete their article."""
        return (
            self.request.user.role == 'JOURNALIST' and
            self.get_object().author == self.request.user
        )


class PublisherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Allows editors to create a new publisher entry."""
    model = Publisher
    fields = ["name"]
    template_name = "dispatch_app/publisher_form.html"
    success_url = reverse_lazy("publisher_list")

    def test_func(self):
        """Ensures only editors can create publishers."""
        return self.request.user.role == "EDITOR"


class PublisherListView(LoginRequiredMixin, ListView):
    """Lists all publishers so users can join one."""
    model = Publisher
    template_name = "dispatch_app/publisher_list.html"
    context_object_name = "publishers"


class EditorDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Displays all articles that are pending approval for Editors to review.
    """
    model = Article
    template_name = 'dispatch_app/editor_dashboard.html'
    context_object_name = 'pending_articles'

    def test_func(self):
        """Ensures only editors can access the approval dashboard."""
        return self.request.user.role == 'EDITOR'

    def get_queryset(self):
        """Retrieves articles that have not yet been approved."""
        return Article.objects.filter(is_approved=False).order_by('created_at')


class SubscriptionsView(LoginRequiredMixin, TemplateView):
    """
    Allows readers to view and manage their subscriptions to
    journalists and publishers.
    """
    template_name = 'dispatch_app/subscriptions.html'

    def get_context_data(self, **kwargs):
        """
        Adds available journalists and publishers
        to the template context.
        """
        context = super().get_context_data(**kwargs)
        # Fetch all available journalists and publishers
        context['journalists'] = CustomUser.objects.filter(role='JOURNALIST')
        context['publishers'] = Publisher.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """Handles the subscription toggle logic."""
        user = self.request.user
        journalist_id = self.request.POST.get('journalist_id')
        publisher_id = self.request.POST.get('publisher_id')

        if journalist_id:
            journalist = get_object_or_404(CustomUser, id=journalist_id)
            if journalist in user.subscribed_journalists.all():
                user.subscribed_journalists.remove(journalist)
            else:
                user.subscribed_journalists.add(journalist)

        if publisher_id:
            publisher = get_object_or_404(Publisher, id=publisher_id)
            if publisher in user.subscribed_publishers.all():
                user.subscribed_publishers.remove(publisher)
            else:
                user.subscribed_publishers.add(publisher)

        return redirect('subscriptions')


class NewsletterListView(LoginRequiredMixin, ListView):
    """
    Displays newsletters for readers or
    the journalist's own newsletters.
    """
    model = Newsletter
    template_name = 'dispatch_app/newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        """Filters newsletters based on the current user role."""
        user = self.request.user
        if user.role == 'JOURNALIST':
            return Newsletter.objects.filter(
                author=user).order_by('-created_at')
        return Newsletter.objects.filter(
            author__in=user.subscribed_journalists.all()
        ).order_by('-created_at')


class NewsletterCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    """
    Allows journalists to write and publish newsletters.
    """
    model = Newsletter
    template_name = 'dispatch_app/newsletter_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('newsletter_list')

    def test_func(self):
        """Ensures only journalists can create newsletters."""
        return self.request.user.role == 'JOURNALIST'

    def form_valid(self, form):
        """Assigns the journalist as the author automatically."""
        # noinspection PyUnresolvedReferences
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    """Allows journalists to edit their own newsletters."""
    model = Newsletter
    template_name = 'dispatch_app/newsletter_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('newsletter_list')

    def test_func(self):
        """Only the author (journalist) can edit their newsletter."""
        return (
            self.request.user.role == 'JOURNALIST' and
            self.get_object().author == self.request.user
        )


class NewsletterDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    """Allows journalists to delete their own newsletters."""
    model = Newsletter
    template_name = 'dispatch_app/newsletter_confirm_delete.html'
    success_url = reverse_lazy('newsletter_list')

    def test_func(self):
        """Only the author (journalist) can delete their newsletter."""
        return (
            self.request.user.role == 'JOURNALIST' and
            self.get_object().author == self.request.user
        )
