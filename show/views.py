from django.template import RequestContext
from django.shortcuts import render_to_response

from show.models import Show, RadioShow
from show.utils import get_current_permitted_show


def schedule(request):

    # Get shows but do a manual order on start time
    def mysort(a, b):
        return cmp(a.start.time(), b.start.time())
    shows = [o for o in Show.permitted.all().order_by('start')]
    shows.sort(mysort)

    di = {}
    for show in shows:
        di.setdefault(show.repeat, [])
        di[show.repeat].append(show.id)

    # Convert values into querysets. The template requires it.
    for k, v in di.items():
        di[k] = Show.permitted.filter(id__in=v)

    extra = dict(intervals=di)
    return render_to_response('show/schedule.html', extra, context_instance=RequestContext(request))


def current_radio(request):
    extra = dict(object=get_current_permitted_show(RadioShow))
    return render_to_response('show/current_radio.html', extra, context_instance=RequestContext(request))
