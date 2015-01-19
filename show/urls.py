from django.conf.urls import patterns, url

from show.view_modifiers import RadioShowDefaultViewModifier
from show.views import ObjectDetail


urlpatterns = patterns(
    '',

    url(
        r'^schedule/$',
        'show.views.schedule',
        {},
        name='show-schedule'
    ),

    url(
        r'^current/radio/$',
        'show.views.current_radio',
        {},
        name='show-current-radio'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        name='radioshow_object_detail'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/about/$',
        ObjectDetail.as_view(is_about=True),
        name='radio-show-about'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/polls/$',
        ObjectDetail.as_view(is_polls=True),
        name='radio-show-polls'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/galleries/$',
        ObjectDetail.as_view(is_galleries=True),
        name='radio-show-galleries'
    ),

    url(
        r'^contributor/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        {},
        name='contributor_object_detail'
    ),
)
