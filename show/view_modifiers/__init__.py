from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from category.models import Category
from jmbo.view_modifiers import ViewModifier
from jmbo.view_modifiers.items import URLPatternItem

from show.models import Show
from show.view_modifiers.items import CategoryItem


class ShowDefaultViewModifier(ViewModifier):

    def __init__(self, request, slug, *args, **kwargs):
        show = Show.objects.get(slug=slug)
        base_url = show.get_absolute_url()
        self.items = [
            CategoryItem(
                request=request,
                title=_("All"),
                get={'name': 'content_type', 'value': 'all'},
                base_url=base_url,
                default=True,
                content_type=None
            )
        ]
        for obj in Category.objects.all():
            self.items.append(
                CategoryItem(
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
                path=reverse('show-polls', kwargs={'slug': slug}),
                matching_pattern_names=['show-polls'],
                default=False
            ),
        )
        self.items.append(
            URLPatternItem(
                request,
                title=_("Galleries"),
                path=reverse('show-galleries', kwargs={'slug': slug}),
                matching_pattern_names=['show-galleries'],
                default=False
            ),
        )
        self.items.append(
            URLPatternItem(
                request,
                title=_("About"),
                path=reverse('show-about', kwargs={'slug': slug}),
                matching_pattern_names=['show-about'],
                default=False
            ),
        )
        super(ShowDefaultViewModifier, self).__init__(
            request,
            *args,
            **kwargs
        )


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
