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
        r'^radio/(?P<slug>[\w-]+)/$', 
        'jmbo.views.object_detail',
        {'view_modifier':RadioShowDefaultViewModifier},
        name='radioshow_object_detail'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/about/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier':RadioShowDefaultViewModifier,
            'extra_context':{'is_about':True}
        },
        name='radio-show-about'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/polls/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier':RadioShowDefaultViewModifier,
            'extra_context':{'is_polls':True}
        },
        name='radio-show-polls'
    ),

    url(
        r'^radio/(?P<slug>[\w-]+)/galleries/$', 
        'jmbo.views.object_detail',
        {
            'view_modifier':RadioShowDefaultViewModifier,
            'extra_context':{'is_galleries':True}
        },
        name='radio-show-galleries'
    ),

    url(
        r'^contributor/(?P<slug>[\w-]+)/$', 
        'jmbo.views.object_detail',
        {},
        name='contributor_object_detail'
    ),

    
#    url(
#        r'^show/entrylist/$', 'show.views.show_entryitem_list',
#        name='show_entryitem_list'
#    ),
#    url(
#        r'^showcontributor/list/(?P<slug>[\w-]+)/$',
#        'showcontributor_content_list',
#        name='showcontributor_content_list'
#    ),
#    url(
#        r'^showcontributor/appearance/(?P<slug>[\w-]+)/$',
#        'showcontributor_appearance_list',
#        name='showcontributor_appearance_list'
#    ),
#    url(
#        r'^showcontributor/(?P<slug>[\w-]+)/$',
#        'showcontributor_detail',
#        name='showcontributor_detail'
#    ),
#    url(
#        r'^showcontributor/content/(?P<slug>[\w-]+)/$',
#        'showcontributor_content_detail',
#        name='showcontributor_content_detail'
#    ),
#    url(
#        r'^showcontributor/contact/(?P<slug>[\w-]+)/$',
#        'showcontributor_contact',
#        name='showcontributor_contact'
#    ),
)
