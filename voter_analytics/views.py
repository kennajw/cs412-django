# voter_analytics/views.py
from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

# Create your views here.
class VotersListView(ListView):
    ''' view to show a list of voters '''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        ''' limit the voters to a small number of records '''

        # qs = super().get_queryset()
        qs = Voter.objects.all()

        # handle search party parameters:
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']

            # filter the voters by this parameter
            qs = qs.filter(party__icontains=party)

        # handle search min. dob year parameters:
        if 'min_dob_year' in self.request.GET:
            min = self.request.GET['min_dob_year']
            min_fields = min.split('-')
            min_year = '' + min_fields[0] +'-01-01'

            # filter the voters by this parameter
            qs = qs.filter(dob__gt=min_year)

        # handle search max. dob year parameters:
        if 'max_dob_year' in self.request.GET:
            max = self.request.GET['max_dob_year']
            max_fields = max.split('-')
            max_year = '' + max_fields[0] +'-01-01'

            # filter the voters by this parameter
            qs = qs.filter(dob__lt=max_year)

        # handle search voter score parameters:
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']

            # filter the voters by this parameter
            qs = qs.filter(v_score=score)

        # handle search for all past participation option parameters:
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state='TRUE')
        
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town='TRUE')

        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary='TRUE')

        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general='TRUE')

        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town='TRUE')
        
        return qs
    
class VoterDetailView(DetailView):
    ''' view to show detail page for one voter '''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'