from django.template import RequestContext
from django.shortcuts import render_to_response

from jmbo.views import ObjectDetail as JmboObjectDetail

from show.models import Show, RadioShow
from show.utils import get_current_permitted_show
from show.view_modifiers import RadioShowDefaultViewModifier


def schedule(request):
    di = {}
    for show in Show.permitted.all():
        di.setdefault(show.repeat, [])
        di[show.repeat].append(show.id)

    # Convert values into querysets. The template requires it.
    for k, v in di.items():
        di[k] = Show.permitted.filter(id__in=v).order_by('start_time')

    extra = dict(intervals=di)
    return render_to_response(
        'show/schedule.html', extra, context_instance=RequestContext(request)
    )


def current_radio(request):
    extra = dict(object=get_current_permitted_show(RadioShow))
    return render_to_response(
        'show/current_radio.html', extra,
        context_instance=RequestContext(request)
    )


class ObjectDetail(JmboObjectDetail):
    template_name = "show/show_detail.html"
    view_modifier = RadioShowDefaultViewModifier
    is_about = False
    is_polls = False
    is_galleries = False

    def get_context_data(self, **kwargs):
        context = super(ObjectDetail, self).get_context_data(**kwargs)
        context["is_about"] = self.is_about
        context["is_polls"] = self.is_polls
        context["is_galleries"] = self.is_galleries
        return context
