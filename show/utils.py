from django.utils import timezone

from show.models import Show


def get_current_permitted_show(klass=Show):
    # does_not_repeat requires a datetime match. All the others operate on
    # time.

    # todo: may need to fall back to SQL since we can't cast datetime to date
    # using the ORM. Or use time fields instead of date fields for a future
    # release. For now it is safe to iterate over all shows since there are not
    # many show objects.

    now = timezone.now()
    now_time = now.time()
    shows = klass.permitted.filter().order_by('start')
    for show in shows:
        if show.repeat == 'does_not_repeat':
            if (show.start <= now) and (show.end > now):
                return show
        else:
            if (show.start.time() <= now_time) and (show.end.time() > now_time):
                return show
    return None 
