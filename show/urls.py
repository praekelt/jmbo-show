from django.conf.urls import patterns, url

from jmbo.views import ObjectDetail

from show.view_modifiers import RadioShowDefaultViewModifier
from show import views


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
        views.ObjectDetail.as_view(is_landing=True),
        name='radioshow_object_detail'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/about/$',
        views.ObjectDetail.as_view(is_about=True),
        name='radio-show-about'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/polls/$',
        views.ObjectDetail.as_view(is_polls=True),
        name='radio-show-polls'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/galleries/$',
        views.ObjectDetail.as_view(is_galleries=True),
        name='radio-show-galleries'
    ),

    url(
        r'^contributor/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        {},
        name='contributor_object_detail'
    ),
)
