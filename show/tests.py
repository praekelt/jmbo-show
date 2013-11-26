from datetime import datetime
from datetime import timedelta

from django.core import management
from django.utils import unittest, timezone

from show.models import Show
from show.utils import get_current_next_permitted_show


class TestCase(unittest.TestCase):

    def setUp(self):

        # Post-syncdb steps

        monday = datetime(year=2013,month=3,day=25,hour=0, minute=0)
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)

        the_house = {
            'title': 'The House',
            'start': monday.replace(hour=21),
            'end': tuesday,
            'repeat': 'weekends'
        }

        #the_network = {
        #    'title': 'The Network',
        #    'start': tuesday.replace(hour=21),
        #    'end': wednesday,
        #    'repeat': 'weekdays'
        #}

        lebo_m = {
            'title': 'Lebo M',
            'start': tuesday.replace(hour=3),
            'end': tuesday.replace(hour=6),
            'repeat': 'weekends'
        }

        wez_reddy_show = {
            'title': 'Wez Reddy Show',
            'start': monday,
            'end': monday.replace(hour=3),
            'repeat': 'weekends'
        }

        the_breakfast_stack = {
            'title': 'The Breakfast Stack',
            'start': wednesday.replace(hour=6),
            'end': wednesday.replace(hour=9),
            'repeat': 'weekdays'
        }

        the_workzone_part_1 = {
            'title': 'The Workzone Part 1',
            'start': tuesday.replace(hour=9),
            'end': tuesday.replace(hour=12),
            'repeat': 'weekdays'
        }

        the_workzone_part_2 = {
            'title': 'The Workzone Part 2',
            'start': monday.replace(hour=12),
            'end': monday.replace(hour=15),
            'repeat': 'weekdays'
        }

        the_drive = {
            'title': 'The Drive',
            'start': monday.replace(hour=15),
            'end': monday.replace(hour=18),
            'repeat': 'weekdays'
        }

        the_pulse_with_abi_ray = {
            'title': 'The Pulse with Abi Ray',
            'start': monday.replace(hour=18),
            'end': monday.replace(hour=21),
            'repeat': 'weekdays'
        }

        ndumiso_at_9 = {
            'title': 'Ndumiso @ 9',
            'start': monday.replace(hour=21),
            'end': monday.replace(hour=23),
            'repeat': 'weekdays'
        }

        the_late_night_show = {
            'title': 'The Late Night Show',
            'start': wednesday.replace(hour=23),
            'end': wednesday.replace(hour=2),
            'repeat': 'weekdays'
        }

        the_right_start = {
            'title': 'The Right Start',
            'start': monday.replace(hour=2),
            'end': monday.replace(hour=5),
            'repeat': 'weekdays'
        }

        the_weekend_breakfast = {
            'title': 'The Weekend Breakfast',
            'start': monday.replace(hour=6),
            'end': monday.replace(hour=10),
            'repeat': 'weekends'
        }

        global_hot_hits_weekends = {
            'title': 'Global Hot Hits Weekends',
            'start': monday.replace(hour=10),
            'end': monday.replace(hour=13),
            'repeat': 'weekends'
        }

        in_the_house = {
            'title': 'In The House',
            'start': monday.replace(hour=14),
            'end': monday.replace(hour=17),
            'repeat': 'saturdays'
        }

        ecr_top_20 = {
            'title': 'ECR Top 20',
            'start': monday.replace(hour=13),
            'end': monday.replace(hour=14),
            'repeat': 'sundays'
        }

        the_lounge = {
            'title': 'The Lounge',
            'start': monday.replace(hour=17),
            'end': monday.replace(hour=21),
            'repeat': 'weekends'
        }

        #the_pulse = {
        #    'title': 'The Pulse',
        #    'start': monday.replace(hour=21),
        #    'end': monday.replace(hour=23),
        #    'repeat': 'weekdays'
        #}

        sam_till_6 = {
            'title': 'Sam till 6',
            'start': monday.replace(hour=5),
            'end': monday.replace(hour=6),
            'repeat': 'weekdays'
        }

        sunday_mix = {
            'title': 'Sunday Mix',
            'start': monday.replace(hour=14),
            'end': monday.replace(hour=16),
            'repeat': 'sundays'
        }

        # Use a "random" order
        # the_network was at 2 (0-indexed)
        shows = (the_house, sunday_mix, sam_till_6, lebo_m,
            wez_reddy_show, the_lounge, the_breakfast_stack, ecr_top_20,
            the_workzone_part_1, in_the_house, the_workzone_part_2,
            global_hot_hits_weekends, the_drive, the_weekend_breakfast,
            the_pulse_with_abi_ray, the_right_start, ndumiso_at_9, the_late_night_show,
        )

        self.shows = {}
        for di in shows:
            di['state'] = 'published'
            show, dc = Show.objects.get_or_create(**di)
            show.sites = [1]
            show.save()
            self.shows[di['title']] = show

    def test_current_next_permitted_show(self):
        monday = datetime(year=2013,month=3,day=25,hour=0, minute=0)
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = monday + timedelta(days=6)

        # Simple case
        current_show, next_show = get_current_next_permitted_show(now=monday.replace(hour=8, minute=30))
        self.assertEqual(current_show, self.shows['The Breakfast Stack'])
        self.assertEqual(next_show, self.shows['The Workzone Part 1'])

        # Monday edge cases
        current_show, next_show = get_current_next_permitted_show(now=monday.replace(hour=21, minute=30))
        self.assertEqual(current_show, self.shows['Ndumiso @ 9'])
        self.assertEqual(next_show, self.shows['The Late Night Show'])
        current_show, next_show = get_current_next_permitted_show(now=monday.replace(hour=23, minute=30))
        self.assertEqual(current_show, self.shows['The Late Night Show'])
        self.assertEqual(next_show, self.shows['The Right Start'])
        current_show, next_show = get_current_next_permitted_show(now=tuesday.replace(hour=0, minute=30))
        self.assertEqual(current_show, self.shows['The Late Night Show'])
        self.assertEqual(next_show, self.shows['The Right Start'])
        current_show, next_show = get_current_next_permitted_show(now=tuesday.replace(hour=2, minute=30))
        self.assertEqual(current_show, self.shows['The Right Start'])
        self.assertEqual(next_show, self.shows['Sam till 6'])

        # Friday edge cases
        current_show, next_show = get_current_next_permitted_show(now=friday.replace(hour=21, minute=30))
        self.assertEqual(current_show, self.shows['Ndumiso @ 9'])
        self.assertEqual(next_show, self.shows['The Late Night Show'])
        current_show, next_show = get_current_next_permitted_show(now=friday.replace(hour=23, minute=30))
        self.assertEqual(current_show, self.shows['The Late Night Show'])
        self.assertEqual(next_show, self.shows['Wez Reddy Show'])
        current_show, next_show = get_current_next_permitted_show(now=saturday.replace(hour=0, minute=30))
        self.assertEqual(current_show, self.shows['Wez Reddy Show'])
        self.assertEqual(next_show, self.shows['Lebo M'])
        current_show, next_show = get_current_next_permitted_show(now=saturday.replace(hour=3, minute=30))
        self.assertEqual(current_show, self.shows['Lebo M'])
        self.assertEqual(next_show, self.shows['The Weekend Breakfast'])

        # Show only on a Sunday
        current_show, next_show = get_current_next_permitted_show(now=sunday.replace(hour=13, minute=30))
        self.assertEqual(current_show, self.shows['ECR Top 20'])
        self.assertEqual(next_show, self.shows['Sunday Mix'])

        # Sunday edge cases
        current_show, next_show = get_current_next_permitted_show(now=sunday.replace(hour=21, minute=30))
        self.assertEqual(current_show, self.shows['The House'])
        self.assertEqual(next_show, self.shows['The Right Start'])
