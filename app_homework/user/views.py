from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from .forms import AddAuthor, AddQuote
from quotes.models import Tag



# Create your views here.


class RegisterView(View):
    template_name = 'user/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='user:addQuote')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account {username} was created')
            return redirect(to='user:login')
        return render(request, self.template_name, context={'form': self.form_class})


@login_required
def add_quote(request):
    author_form = AddAuthor()
    quotes_form = AddQuote()
    if request.method == 'POST':
        author_form = AddAuthor(request.POST)
        quotes_form = AddQuote(request.POST)
        if quotes_form.is_valid():
            quote = quotes_form.save(commit=False)
            if author_form.is_valid():
                author = author_form.save()
                quote.author = author
            author_form.save()
            quote.save()
            tag_data = request.POST.getlist('tags')
            for tag_name in tag_data:
                tag, created = Tag.objects.get_or_create(tag=tag_name)
                quote.tags.add(tag)  # Добавляем тег к цитате
            messages.success(request, 'Quote add')
            return redirect(to='user:addQuote')
    return render(request, 'user/add_quote.html', context={'quote_form': quotes_form, 'author_form': author_form})
