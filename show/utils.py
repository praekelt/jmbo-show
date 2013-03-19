from django.utils import timezone

from show.models import Show


def get_current_permitted_show(klass=Show, now=None):
    # does_not_repeat requires a datetime match. All the others operate on
    # time.

    # todo: may need to fall back to SQL since we can't cast datetime to date
    # using the ORM. Or use time fields instead of date fields for a future
    # release. For now it is safe to iterate over all shows since there are not
    # many show objects.

    if now is None:
        now = timezone.now()
    now_time = now.time()
    shows = klass.permitted.filter().order_by('start')
    for show in shows:
        if show.repeat == 'does_not_repeat':
            if (show.start <= now) and (show.end > now):
                return show
        elif show.repeat == 'weekdays':
            if (now.weekday() in (0, 1, 2, 3, 4)) \
                and (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
        elif show.repeat == 'weekends':
            if (now.weekday() in (5, 6)) \
                and (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
        elif show.repeat == 'saturdays':
            if (now.weekday() == 5) \
                and (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
        elif show.repeat == 'sundays':
            if (now.weekday() == 6) \
                and (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
        elif show.repeat == 'monthly_by_day_of_month':
            if (show.start.day == now.day) \
                and (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
        else:
            if (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
    return None 
