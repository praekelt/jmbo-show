from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from category.models import Category
from jmbo.view_modifiers import ViewModifier
from jmbo.view_modifiers.items import URLPatternItem

from show.models import Show
from show.view_modifiers.items import CategoryRelatedItem


class BaseShowDefaultViewModifier(ViewModifier):

    prefix = ''

    def __init__(self, request, slug, *args, **kwargs):
        show = Show.objects.get(slug=slug)
        base_url = show.get_absolute_url()
        self.items = [
            CategoryRelatedItem(
                request=request,
                title=_("All"),
                get={'name': 'category', 'value': 'all'},
                base_url=base_url,
                default=True,
                content_type=None
            )
        ]

        # Find set of categories for all relations on show
        ids = []
        for obj in show.get_permitted_related_items(direction='both'):
            if obj.primary_category:
                ids.append(obj.primary_category.id)
        for obj in Category.objects.filter(id__in=ids).order_by('title'):
            self.items.append(
                CategoryRelatedItem(
                    request=request,
                    title=obj.title,
                    get={'name': 'category', 'value': obj.slug},
                    base_url=base_url,
                )
            )

        self.items.append(
            URLPatternItem(
                request,
                title=_("Polls"),
                path=reverse(self.prefix + 'show-polls', kwargs={'slug': slug}),
                matching_pattern_names=[self.prefix + 'show-polls'],
                default=False
            ),
        )
        self.items.append(
            URLPatternItem(
                request,
                title=_("Galleries"),
                path=reverse(self.prefix + 'show-galleries', kwargs={'slug': slug}),
                matching_pattern_names=[self.prefix + 'show-galleries'],
                default=False
            ),
        )
        self.items.append(
            URLPatternItem(
                request,
                title=_("About"),
                path=reverse(self.prefix + 'show-about', kwargs={'slug': slug}),
                matching_pattern_names=[self.prefix + 'show-about'],
                default=False
            ),
        )
        super(BaseShowDefaultViewModifier, self).__init__(
            request,
            *args,
            **kwargs
        )


class RadioShowDefaultViewModifier(BaseShowDefaultViewModifier):
    prefix = 'radio-'


class ShowContributorViewModifier(ViewModifier):
    def __init__(self, request, slug, *args, **kwargs):
        self.items = []
        '''
        self.items = [
            URLPatternItem(
                request,
                title=_("About"),
                path=reverse('showcontributor_content_list', kwargs={'slug': \
                        slug}),
                matching_pattern_names=['showcontributor_content_list', \
                        'showcontributor_content_detail', ],
                default=False
            ),
        ]
        '''
        '''
        self.items = [
            URLPatternItem(
                request,
                title="Blog",
                path=reverse('showcontributor_content_list', kwargs={'slug': \
                        slug}),
                matching_pattern_names=['showcontributor_content_list', \
                        'showcontributor_content_detail', ],
                default=False
            ),
            URLPatternItem(
                request,
                title="Profile",
                path=reverse('showcontributor_detail', kwargs={'slug': slug}),
                matching_pattern_names=['showcontributor_detail', ],
                default=False
            ),
            URLPatternItem(
                request,
                title="Contact",
                path=reverse('showcontributor_contact', kwargs={'slug': slug}),
                matching_pattern_names=['showcontributor_contact', ],
                default=False
            ),
            URLPatternItem(
                request,
                title="Appearances",
                path=reverse('showcontributor_appearance_list', \
                        kwargs={'slug': slug}),
                matching_pattern_names=['showcontributor_appearance_list', ],
                default=False
            ),
        ]
        '''
        super(ShowContributorViewModifier, self).__init__(request)
