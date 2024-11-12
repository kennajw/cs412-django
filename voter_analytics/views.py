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

class GraphsListView(ListView):
    ''' view to show a list of graphs displaying voter information '''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'v'
    
    def get_context_data(self, **kwargs):
        ''' provide context variables for use in this template '''

        # call super class
        context =  super().get_context_data(**kwargs)
        v = context['v']

        # query set of all voters in the db
        all_voters = Voter.objects.all()

        # voter distribution histogram
        years = []
        dist_year = []

        for voter in all_voters:
            year = voter.dob.year

            # if the year has already been added from a prev. voter
            if year in years:
                dist_year[years.index(year)] += 1
            # else add the year since this is the first voter born in that year
            else:
                years.append(year)
                dist_year.append(1)
        
        # total number of voters
        total_year = sum(dist_year)

        # create the figure
        fig = go.Figure(data=[go.Bar(x=years, y=dist_year)])

        # create title
        title = f'voter distribution by birth year (total={total_year})'
        fig.update_layout(title=title)

        # display the figure
        graph_birth_year = plotly.offline.plot(fig, auto_open=False, output_type="div")

        # add our graph to the context data
        context['graph_birth_year'] = graph_birth_year

        # party affiliation pie chart
        parties = []
        dist_party = []

        for voter in all_voters:
            party = voter.party

            # if the party has already been added from a prev. voter
            if party in parties:
                dist_party[parties.index(party)] += 1
            # else add the party since this is the first voter's party
            else:
                parties.append(party)
                dist_party.append(1)

        # total number of voters w/ party affiliations
        total_party = sum(dist_party)

        # create the figure
        fig = go.Pie(labels=parties, values=dist_party)

        # create title
        title_party = f'voter distribution by party affiliation (total={total_party})'

        # display the figure
        graph_party = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_party,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        # add our graph to the context data
        context['graph_party'] = graph_party
        
                # voter distribution histogram
        votes = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        dist_vote = []

        # collect vote totals for each election
        v20state = all_voters.filter(v20state='TRUE')
        v21town = all_voters.filter(v21town='TRUE')
        v21primary = all_voters.filter(v21primary='TRUE')
        v22general = all_voters.filter(v22general='TRUE')
        v23town = all_voters.filter(v23town='TRUE')

        # append totals to distribution
        dist_vote.append(len(v20state))
        dist_vote.append(len(v21town))
        dist_vote.append(len(v21primary))
        dist_vote.append(len(v22general))
        dist_vote.append(len(v23town))

        print(dist_vote)
        
        # total number of votes
        total_votes = sum(dist_year)

        # create the figure
        fig = go.Figure(data=[go.Bar(x=votes, y=dist_vote)])

        # create title
        title = f'vote counts by election (total={total_votes})'
        fig.update_layout(title=title)

        # display the figure
        graph_votes = plotly.offline.plot(fig, auto_open=False, output_type="div")

        # add our graph to the context data
        context['graph_votes'] = graph_votes

        return context
        