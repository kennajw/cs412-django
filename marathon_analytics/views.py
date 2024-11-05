from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

# Create your views here.
class ResultsListView(ListView):
    ''' view to show a list of results '''

    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        ''' limit the results to a small number of records '''

        qs = super().get_queryset()
        # return qs[:25] # limit to 25 records

        # handle search form/url parameters:
        if 'city' in self.request.GET:
            city = self.request.GET['city']

            #filter the results by this parameter, make case-sensitive
            qs = Result.objects.filter(city__icontains=city)
        return qs