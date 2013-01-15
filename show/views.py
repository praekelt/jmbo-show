from django.template import RequestContext
from django.shortcuts import render_to_response

from show.models import Show


def schedule(request):
    # The template requires querysets so no way to do one query
    di = {}
    for k in ('weekdays', 'weekends', 'saturdays', 'sundays'):
        di[k] = Show.permitted.filter(repeat=k).order_by('start')
    extra = dict(intervals=di)
    return render_to_response('show/schedule.html', extra, context_instance=RequestContext(request))
