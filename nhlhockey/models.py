from django.db import models

class Conference(models.Model):
    EASTERN = 'E'
    WESTERN = 'W'
    NHL_CONFERENCES = (
                       (EASTERN, 'eastern'),
                       (WESTERN, 'western'),
                       )
    
    name = models.CharField(max_length=1,
                            choices=NHL_CONFERENCES,
                            default=EASTERN)
    
    def __unicode__(self):
        return dict(Conference.NHL_CONFERENCES)[self.name]
    
    def display_name(self):
        return dict(Conference.NHL_CONFERENCES)[self.name].title()

class Division(models.Model):
    METROPOLITAN = 'M'
    ATLANTIC = 'A'
    CENTRAL = 'C'
    PACIFIC = 'P'
    NHL_DIVISIONS = (
                     (Conference.EASTERN, (
                                           (METROPOLITAN, 'metropolitan'),
                                           (ATLANTIC, 'atlantic'),
                                           )
                      ),
                     (Conference.WESTERN, (
                                           (CENTRAL, 'central'),
                                           (PACIFIC, 'pacific'),
                                           )
                      ),
                     )
    
    name = models.CharField(max_length=1,
                            choices=NHL_DIVISIONS,
                            default=METROPOLITAN)
    
    conference = models.ForeignKey(Conference)
    
    def __unicode__(self):
        if self.isLegitDivisionConfig():
            return dict(dict(Division.NHL_DIVISIONS)[self.conference.name])[self.name]
        else:
            return "illegal division"
    
    def display_name(self):
        return dict(dict(Division.NHL_DIVISIONS)[self.conference.name])[self.name].title()
    
    def isLegitDivisionConfig(self):
        if self.name == Division.METROPOLITAN or self.name == Division.ATLANTIC:
            return self.conference.name == Conference.EASTERN
        elif self.name == Division.CENTRAL or self.name == Division.PACIFIC:
            return self.conference.name == Conference.WESTERN
        else:
            return False
        
class Team(models.Model):
    location = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=3)
    division = models.ForeignKey(Division)
    
    def __unicode__(self):
        return unicode(self.location) + ' ' +  unicode(self. name) or u''
    
    def display_name(self):
        return self.location.title() + ' ' + self.name.title()
    
    def url_name(self):
        return self.name.replace (" ", "-")