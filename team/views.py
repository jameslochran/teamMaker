
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Player, Skills

from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib
import requests
import pandas as pd
from django_pandas.io import read_frame

import numpy as np
from .forms import RosterForm



def index(request):


    return render(request, 'home.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

def dashboard(request):
    # members = Player.objects.all()
    members = Player.objects.filter(user=request.user)
    has_skills = []
    for m in members:
        mem_id = m.id
        qs1 = Skills.objects.filter(player_id = mem_id)
        if(not(qs1)):
            pass
        else:
            has_skills.append(mem_id)
    return render(request,'dashboard.html', {'members':members, 'has_skills':has_skills})





def Teams(request):
    #collect players

    if request.method == 'POST':
        if request.POST.getlist('checks[]'):
             selecteditems = request.POST.getlist('checks[]')

    else:
        pass


    player_list = list(map(int, selecteditems))
    # Get all getPlayers
    model = Player
    getPlayers = Player.objects.filter(id__in=player_list)

    # Get all players with skills
    #qs = Skills.objects.all()
    qs = Skills.objects.values_list("shooting","defense","rebounding", "passing","id", "player")
    # print(qs)



    df = read_frame(getPlayers)
    # print(df)
    ds = read_frame(qs)
    # print(ds)
    #create dataframe with players and skills
    ds.rename(columns={'player':'name'},inplace=True)

    #full_roster = pd.concat([df, ds], axis=1, sort=False)
    full_roster = pd.merge(df, ds, on='name')
    full_roster.drop(columns=['id_y'],inplace=True)
    full_roster.drop(columns=['id_x'],inplace=True)


    #sum columns to create score for each player
    # full_roster['score']= full_roster.sum(axis=1)
    full_roster['score']= (full_roster.defense*2)+(full_roster.rebounding*2)+(full_roster.passing*2)+(full_roster.shooting)
    

    # full_roster.drop(columns=['id', 'player'],inplace=True)
#sort into various dataframes
    df_score = full_roster.copy()
    df_score.sort_values(by=['score'], inplace=True)
    #df_score.drop(columns=['id', 'player'],inplace=True)
    df_height = full_roster.copy()
    df_height.sort_values(by=['height'], inplace=True)
    #df_height.drop(columns=['id', 'player'],inplace=True)
    df_age = full_roster.copy()
    df_age.sort_values(by=['age'], inplace=True)
    df_shooting = full_roster.copy()
    df_shooting.sort_values(by=['shooting'], inplace=True)
# create teams for each sorting
    #score
    score_1 = df_score.iloc[::2]
    score_2 = df_score.iloc[1::2]
    score1Total = score_1['score'].sum()
    score2Total = score_2['score'].sum()
    score_dif = abs(score1Total - score2Total)
    score_1.drop(columns=[ 'age' , 'height',  'shooting',  'defense',  'passing' , 'rebounding', 'user'], inplace=True)
    score_2.drop(columns=[ 'age' , 'height',  'shooting',  'defense',  'passing' , 'rebounding',  'user'], inplace=True)
    score_1.set_index('name',inplace=True)
    score_2.set_index('name',inplace=True)
    s1_table = score_1.to_html(classes='table table-hover table-bordered table-striped', index_names=False)
    s2_table = score_2.to_html(classes='table table-hover table-bordered table-striped', index_names=False)
    # score1Total = score_1['score'].sum()
    # score2Total = score_2['score'].sum()
    # score_dif = score1Total - score2Total


    #height
    height_1 = df_height.iloc[::2]
    height_2 = df_height.iloc[1::2]
    height1Total = height_1['score'].sum()
    height2Total = height_2['score'].sum()
    height_dif = abs(height1Total - height2Total)
    height_1.drop(columns=[ 'age' ,   'shooting',  'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    height_2.drop(columns=[ 'age' ,   'shooting',  'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    height_1.set_index('name',inplace=True)
    height_2.set_index('name',inplace=True)
    h1_table = height_1.to_html(classes='table table-hover table-bordered table-striped', index_names=False)
    h2_table = height_2.to_html(classes='table table-hover table-bordered table-striped', index_names=False)


#age
    age_1 = df_age.iloc[::2]
    age_2 = df_age.iloc[1::2]
    age1Total = age_1['score'].sum()
    age2Total = age_2['score'].sum()
    age_dif = abs(age1Total - age2Total)
    age_1 .drop(columns=[  'height',  'shooting',  'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    age_2.drop(columns=[  'height',  'shooting',  'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    age_1.set_index('name',inplace=True)
    age_2.set_index('name',inplace=True)
    age1_table = age_1.to_html(classes='table table-hover table-bordered table-striped', index_names=False)
    age2_table = age_2.to_html(classes='table table-hover table-bordered table-striped', index_names=False)


#shooting
    shooting_1 = df_shooting.iloc[::2]
    shooting_2 = df_shooting.iloc[1::2]
    shooting1Total = shooting_1['score'].sum()
    shooting2Total = shooting_2['score'].sum()
    shooting_dif = abs(shooting1Total - shooting2Total)
    shooting_1.drop(columns=[ 'age' , 'height',    'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    shooting_2.drop(columns=[ 'age' , 'height',   'defense',  'passing' , 'rebounding',  'score','user'], inplace=True)
    shooting_1.set_index('name',inplace=True)
    shooting_2.set_index('name',inplace=True)
    shooting1_table = shooting_1.to_html(classes='table table-hover table-bordered table-striped', index_names=False)
    shooting2_table = shooting_2.to_html(classes='table table-hover table-bordered table-striped', index_names=False)





    return render(request,'teams.html', {'s1_table':s1_table, 's2_table':s2_table, 'score_dif':score_dif, 'score1Total':score1Total, 'score2Total':score2Total,
                                            'h1_table':h1_table, 'h2_table':h2_table, 'height_dif':height_dif, 'height1Total':height1Total, 'height2Total':height2Total,
                                            'age1_table':age1_table, 'age2_table':age2_table, 'age_dif':age_dif, 'age1Total':age1Total, 'age2Total':age2Total,
                                            'shooting1_table':shooting1_table, 'shooting2_table':shooting2_table, 'shooting_dif':shooting_dif, 'shooting1Total':shooting1Total, 'shooting2Total':shooting2Total })


class CreatePlayer(LoginRequiredMixin, generic.CreateView):
    model = Player
    fields = ['name', 'age', 'height']
    template_name = 'create_player.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreatePlayer, self).form_valid(form)
        return redirect('dashboard')



def add_Skill(request, pk):
    player = Player.objects.get(pk=pk)
    SkillFormset = inlineformset_factory(Player, Skills, fields = ('shooting', 'defense', 'passing', 'rebounding'), max_num=1)

    if request.method == 'POST':
        formset = SkillFormset(request.POST,instance=player)
        if formset.is_valid():
            formset.save()

            return redirect('detail', pk=pk)

    formset = SkillFormset(instance=player)


    return render(request, 'add_skill.html', {'formset': formset,'player':player})


class DetailPlayer(generic.DetailView):
    model = Player
    qs = Player.objects.all()
    # df = read_frame(qs)
    template_name = 'detail.html'


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view
