from django.template import RequestContext
from django.shortcuts import render_to_response

from show.models import Show, RadioShow
from show.utils import get_current_permitted_show


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
