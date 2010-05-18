from django.conf import settings
from django.db import models

from ckeditor.fields import RichTextField
from content.models import ModelBase
from options.models import Options

# Content Models
class ShowContributor(ModelBase):
    profile = RichTextField(help_text='Full profile for this contributor.')
    shows = models.ManyToManyField(
        'show.Show', 
        through='show.Credit',
        related_name='show_contributors',
    )

    class Meta:
        verbose_name = 'Show Contributor'
        verbose_name_plural = 'Show Contributors'

class Credit(models.Model):
    contributor = models.ForeignKey(
        'show.ShowContributor', 
        related_name='credits'
    )
    show = models.ForeignKey(
        'show.Show', 
        related_name='credits'
    )
    role = models.IntegerField(
        blank=True, 
        null=True,
    )

    def __unicode__(self):
        return "%s credit for %s" % (self.contributor.title, self.show.title)

class Show(ModelBase):
    content = RichTextField(
        help_text="Full article detailing this show.",
        blank=True,
        null=True,
    )
    contributor = models.ManyToManyField(
        'show.ShowContributor', 
        through='show.Credit',
    )

    def get_primary_contributors(self):
        """
        Returns a list of primary contributors, with primary being defined as those contributors that have the highest role assigned(in terms of priority). Only premitted contributors are returned.
        """
        primary_credits = []
        credits = self.credits.exclude(role=None).order_by('role')
        if credits:
            primary_role = credits[0].role
            for credit in credits:
                if credit.role == primary_role:
                    primary_credits.append(credit)

        contributors = []
        for credit in primary_credits:
            contributor = credit.contributor
            if contributor.is_permitted:
                contributors.append(contributor)

        return contributors

    def is_contributor_title_in_title(self, contributor):
        """
        Checks whether or not a contributors title is already present in the show's title.
        """
        return contributor.title.lower().lstrip().rstrip() in self.title.lower()

class RadioShow(Show):
    pass

# Option Models
class ShowOptions(Options):
    __module__ = 'options.models'

    class Meta():
        verbose_name = 'Show Options'
        verbose_name_plural = 'Show Options'

class CreditOption(models.Model):
    show_options = models.ForeignKey('options.ShowOptions')
    role_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    role_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="The priority assigned to this role, with lower values being more importent.",
    )
