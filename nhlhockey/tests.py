from django.test import TestCase
from nhlhockey.models import Conference, Division

class DivisionTests(TestCase):

    def test_all_divisions_legit(self):
        """
        isLegitDivisionConfig() should return False illegal division configs
        """
        eastern_conference = Conference(name=Conference.EASTERN)
        western_conference = Conference(name=Conference.WESTERN)
        
        metropolitan = Division(name=Division.METROPOLITAN,conference=eastern_conference)
        atlantic = Division(name=Division.ATLANTIC,conference=eastern_conference)
        central = Division(name=Division.CENTRAL,conference=western_conference)
        pacific = Division(name=Division.PACIFIC,conference=western_conference)
        
        self.assertEqual(metropolitan.isLegitDivisionConfig(), True)
        self.assertEqual(atlantic.isLegitDivisionConfig(), True)
        self.assertEqual(central.isLegitDivisionConfig(), True)
        self.assertEqual(pacific.isLegitDivisionConfig(), True)
            
    def test_illegal_division_configs(self):
        """
        Make some possible illegal divisions and see if isLegitDivisionConfig() is false
        """
        
        eastern_conference = Conference(name=Conference.EASTERN)
        fake_division_1 = Division(name="PIZZA KIDS",conference=eastern_conference)
        fake_division_2 = Division(name=Division.CENTRAL,conference=eastern_conference)
        
        self.assertEqual(fake_division_1.isLegitDivisionConfig(), False)
        self.assertEqual(fake_division_2.isLegitDivisionConfig(), False)