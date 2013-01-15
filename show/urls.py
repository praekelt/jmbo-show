from django.conf.urls.defaults import patterns, url

from show.view_modifiers import RadioShowDefaultViewModifier


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
        'jmbo.views.object_detail',
        {'template_name': 'show/show_detail.html', 'view_modifier': RadioShowDefaultViewModifier},
        name='radioshow_object_detail'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/about/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier': RadioShowDefaultViewModifier,
            'extra_context': {'is_about': True}
        },
        name='radio-show-about'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/polls/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier': RadioShowDefaultViewModifier,
            'extra_context': {'is_polls': True}
        },
        name='radio-show-polls'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/galleries/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier': RadioShowDefaultViewModifier,
            'extra_context': {'is_galleries': True}
        },
        name='radio-show-galleries'
    ),

    url(
        r'^contributor/(?P<slug>[\w-]+)/$', 
        'jmbo.views.object_detail',
        {},
        name='contributor_object_detail'
    ),
)
