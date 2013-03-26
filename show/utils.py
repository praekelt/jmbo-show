from django.utils import timezone

from show.models import Show


def get_current_next_permitted_show(klass=Show, now=None):
    # does_not_repeat requires a datetime match. All the others operate on
    # time.

    # todo: may need to fall back to SQL since we can't cast datetime to date
    # using the ORM. Or use time fields instead of date fields for a future
    # release. For now it is safe to iterate over all shows since there are not
    # many show objects.

    if now is None:
        now = timezone.now()
    now_time = now.time()
    today_weekday = now.weekday()
    tomorrow_weekday = (today_weekday + 1) % 7
    shows = klass.permitted.filter().order_by('start')

    # First pass groups shows for today and tomorrow
    slots = {'today': [], 'tomorrow': []}
    for show in shows:
        if show.repeat == 'does_not_repeat':
            if (show.start.year == now.year) \
                and (show.start.month == now.month) \
                and (show.start.day == now.day):
                slots['today'].append(show)
            tomorrow = now + timedelta(days=1)
            if (show.start.year == tomorrow.year) \
                and (show.start.month == tomorrow.month) \
                and (show.start.day == tomorrow.day):
                slots['tomorrow'].append(show)

        elif show.repeat == 'weekdays':
            if today_weekday in (0, 1, 2, 3, 4):
                slots['today'].append(show)
            if tomorrow_weekday in (0, 1, 2, 3, 4):
                slots['tomorrow'].append(show)

        elif show.repeat == 'weekends':
            if today_weekday in (5, 6):
                slots['today'].append(show)
            if tomorrow_weekday in (5, 6):
                slots['tomorrow'].append(show)

        elif show.repeat == 'saturdays':
            if today_weekday == 5:
                slots['today'].append(show)
            if tomorrow_weekday == 5:
                slots['tomorrow'].append(show)

        elif show.repeat == 'sundays':
            if today_weekday == 6:
                slots['today'].append(show)
            if tomorrow_weekday == 6:
                slots['tomorrow'].append(show)

        elif show.repeat == 'monthly_by_day_of_month':
            if show.start.day == now.day:
                slots['today'].append(show)
            tomorrow = now + timedelta(days=1)
            if show.start.day == tomorrow.day:
                slots['tomorrow'].append(show)

        else:
            # Daily
            slots['today'].append(show)
            slots['tomorrow'].append(show)

    # Second pass finds current and next show
    current_show = None
    next_show = None
    for show in slots['today']:
        if current_show is not None:
            next_show = show
            break
        # No need to check end time since list is ordered. This also handles
        # case where show is over midnight.
        if show.start.time() <= now_time:
            current_show = show       
    # Use tomorrow's first show if next show not set
    if next_show is None:        
        next_show = slots['tomorrow'] and slots['tomorrow'][0] or None

    return current_show, next_show


def get_current_permitted_show(klass=Show, now=None):
    result, dc = get_current_next_permitted_show(klass, now)
    return result


def get_next_permitted_show(klass=Show, now=None):
    dc, result = get_current_next_permitted_show(klass, now)
    return result
