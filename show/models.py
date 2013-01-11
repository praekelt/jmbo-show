from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

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
    content = RichTextField(
        help_text="Full article detailing this show.",
        blank=True,
        null=True,
    )
    contributor = models.ManyToManyField(
        'show.Contributor',
        through='show.Credit',
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
