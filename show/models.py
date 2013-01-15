from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext

from ckeditor.fields import RichTextField
from preferences.models import Preferences
from jmbo.models import ModelBase
from jmbo_calendar.models import Event


class Contributor(ModelBase):
    profile = RichTextField(
        help_text='Full profile for this contributor.',
        blank=True,
        null=True,
    )
    shows = models.ManyToManyField(
        'show.Show',
        through='show.Credit',
        related_name='show_contributors',
    )

    @property
    def permitted_shows(self):
        return Show.permitted.filter(contributor__in=[self]).order_by('title')

    @property
    def permitted_credits(self):
        return [o for o in self.credits.all() if o.show.is_permitted]

    @property
    def permitted_related_items(self):
        return self.get_permitted_related_items(direction='both')


class Credit(models.Model):
    contributor = models.ForeignKey(
        'show.Contributor',
        related_name='credits'
    )
    show = models.ForeignKey(
        'show.Show',
        related_name='credits'
    )
    credit_option = models.ForeignKey('show.CreditOption')

    def __unicode__(self):
        return "%s credit for %s" % (self.contributor.title, self.show.title)


class Show(ModelBase):
    """Show is intended to be a superclass but cannot be marked abstract due 
    to the many-to-many fields."""
    content = RichTextField(
        help_text="Full article detailing this show.",
        blank=True,
        null=True,
    )
    contributors = models.ManyToManyField(
        'show.Contributor',
        through='show.Credit',
    )
    start = models.DateTimeField(
        db_index=True, 
        help_text="""If only the time of day is applicable then set the day \
to today. It will be ignored."""
    )
    end = models.DateTimeField(
        db_index=True,
        help_text="""If only the time of day is applicable then set the day \
to today. It will be ignored."""
    )
    repeat = models.CharField(
        max_length=64,
        choices=(
            ('does_not_repeat', 'Does Not Repeat'),
            ('daily', 'Daily'),
            ('weekdays', 'Weekdays'),
            ('weekends', 'Weekends'),
            ('saturdays', 'Saturdays'),
            ('sundays', 'Sundays'),
            ('weekly', 'Weekly'),
            ('monthly_by_day_of_month', 'Monthly By Day Of Month'),
        ),
        default='does_not_repeat',
        db_index=True,
    )
    repeat_until = models.DateField(
        blank=True,
        null=True,
    )

    def get_primary_contributors(self):
        """
        Returns a list of primary contributors, with primary being defined
        as those contributors that have the highest role assigned (in terms
        of priority). Only permitted contributors are returned.
        """
        primary_credits = []
        credits = self.credits.exclude(credit_option=None).order_by('credit_option__role_priority')
        if credits:
            primary_role_priority = credits[0].credit_option.role_priority
            for credit in credits:
                if credit.credit_option.role_priority == primary_role_priority:
                    primary_credits.append(credit)

        contributors = []
        for credit in primary_credits:
            contributor = credit.contributor
            if contributor.is_permitted:
                contributors.append(contributor)

        return contributors
    
    @property
    def duration(self):
        return self.end - self.start

    @property
    def next(self):
        now = timezone.now()
        # if the first iteration of the show has not yet ended
        if now < self.end:
            return self.start
        # calculate next repeat of show
        elif self.repeat != 'does_not_repeat' and \
                (self.repeat_until is None or now.date() <= self.repeat_until):
            if now.timetz() < self.end.timetz() or self.duration > \
                    (self.start.replace(hour=23, minute=59, second=59,
                    microsecond=999999) - self.start):
                date = self._next_repeat(now.date())
            else:
                date = self._next_repeat(now.date() + timedelta(days=1))

            if self.repeat_until is None or date <= self.repeat_until:
                return datetime.combine(date, self.start.timetz())
        return None

    # calculate the next repeat, ignores repeat_until and assumes repetition
    def _next_repeat(self, date):
        if self.repeat == 'daily':
            return date
        elif self.repeat == 'monthly_by_day_of_month':
            if date.day > self.start.day:  # skip to next month
                date = date.replace(day=1, month=(date.month + 1) % 12,
                        year=date.year + int(math.floor((date.month + 1) / 12)))

            if self.start.day > calendar.monthrange(date.year, date.month)[1]:
                date = date.replace(day=calendar.monthrange(date.year,
                        date.month)[1])
            else:
                date = date.replace(day=self.start.day)
        else:
            weekday = date.weekday()
            if self.repeat == 'weekdays':
                date = date + timedelta(days=7 - weekday) \
                    if (weekday == 5 or weekday == 6) else date
            elif self.repeat == 'weekends':
                date = date + timedelta(days=5 - weekday) \
                    if (0 <= weekday <= 4) else date
            # todo: saturday and sunday
            else:  # must be weekly
                date = date + timedelta(days=self.start.weekday() - weekday) \
                    if self.start.weekday() >= weekday else \
                    date + timedelta(days=7 - weekday + self.start.weekday())
        return date

    def save(self, *args, **kwargs):
        # set repeat_until to the exact date of the final repetition
        if self.repeat != 'does_not_repeat':
            if self.repeat_until is not None:
                next = self._next_repeat(self.repeat_until)
                if next > self.repeat_until:
                    if self.repeat == 'daily':
                        raise ValueError('This should not be possible')
                    elif self.repeat == 'weekly':
                        self.repeat_until = next - timedelta(days=7)
                    elif self.repeat == 'weekdays':
                        self.repeat_until = self.repeat_until - \
                            timedelta(days=self.repeat_until.weekday() - 4)
                    elif self.repeat == 'weekends':
                        self.repeat_until = self.repeat_until - \
                            timedelta(days=self.repeat_until.weekday() + 1)
                    else:  # must be 'monthly_by_day_of_month'
                        self.repeat_until = next - timedelta(days=
                                calendar.monthrange(self.repeat_until.year,
                                self.repeat_until.month)[1])
                elif next < self.repeat_until:
                    raise ValueError('''The repeat_until date is too early
                            and the show will never be repeated.''')
        else:
            self.repeat_until = None

        super(Show, self).save(*args, **kwargs)


class RadioShow(Show):
    pass


class ShowPreferences(Preferences):
    __module__ = 'preferences.models'

    class Meta:
        verbose_name = 'Show preferences'
        verbose_name_plural = 'Show preferences'


class CreditOption(models.Model):
    show_preferences = models.ForeignKey('preferences.ShowPreferences')
    role_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    role_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="""The priority assigned to this role, with lower values \
being more important.""",
    )

    def __unicode__(self):
        return self.role_name


class Appearance(models.Model):
    event = models.ForeignKey(
        Event,
        related_name='appearances'
    )
    show_contributor = models.ForeignKey(
        Contributor,
        related_name='appearances'
    )
