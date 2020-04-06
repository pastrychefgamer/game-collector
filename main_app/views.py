from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Game, Console
from .forms import OutcomeForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def games_index(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games': games})


@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    consoles_game_unassoc = Console.objects.exclude(
        id__in=game.consoles.all().values_list('id'))
    outcome_form = OutcomeForm()
    return render(request, 'games/detail.html', {'game': game, 'outcome_form': outcome_form, 'consoles': consoles_game_unassoc})


@login_required
def add_outcome(request, game_id):
    form = OutcomeForm(request.POST)
    if form.is_valid():
        new_outcome = form.save(commit=False)
        new_outcome.game_id = game_id
        new_outcome.save()
        return redirect('detail', game_id=game_id)


@login_required
def assoc_console(request, game_id, console_id):
    Game.objects.get(id=game_id).consoles.add(console_id)
    return redirect('detail', game_id=game_id)


@login_required
def unassoc_console(request, game_id, console_id):
    Game.objects.get(id=game_id).consoles.remove(console_id)
    return redirect('detail', game_id=game_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['name', 'genre', 'description', 'rating']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/games/'


class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['genre', 'description', 'rating']


class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games/'


class ConsoleList(LoginRequiredMixin, ListView):
    model = Console


class ConsoleDetail(LoginRequiredMixin, DetailView):
    model = Console


class ConsoleCreate(LoginRequiredMixin, CreateView):
    model = Console
    fields = ['name', 'color']
    success_url = '/consoles/'


class ConsoleUpdate(LoginRequiredMixin, UpdateView):
    model = Console
    fields = ['name', 'color']
    success_url = '/consoles/'


class ConsoleDelete(LoginRequiredMixin, DeleteView):
    model = Console
    success_url = '/consoles/'
