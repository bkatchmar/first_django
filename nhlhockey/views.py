from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from nhlhockey.models import Conference, Division, Team

class IndexView(generic.ListView):
    template_name = 'nhlhockey/index.html'
    context_object_name = 'all_conferences'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Conference.objects.all()

def conference(request, conference):
    selected_conference = get_object_or_404(Conference, name=conference[0].upper())
    return render(request,
                  'nhlhockey/conferences.html',
                  {
                   'conference': selected_conference,
                   'divisions': selected_conference.division_set.all()
                   }
                  )

def division(request, conference, division):
    selected_division = get_object_or_404(Division, name=division[0].upper())
    return render(request, 
                  'nhlhockey/divisions.html',
                  {
                   'division': selected_division,
                   'teams': selected_division.team_set.all()
                   }
                  )

def team(request, conference, division, teamname):
    selected_team = get_object_or_404(Team, abbreviation=teamname)
    
    # Make this presentable for the view (technically we can probably use CSS here, but I'm in a rush
    selected_team.location = selected_team.location.title()
    selected_team.name = selected_team.name.title()
    selected_team.abbreviation = selected_team.abbreviation.upper()
    
    return render(request, 
                  'nhlhockey/team.html',
                  {
                   'team': selected_team
                   }
                  )