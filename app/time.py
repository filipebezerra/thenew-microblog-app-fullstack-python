TIME_DURATION_UNITS = (
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('minute', 60),
    ('second', 1)
)


def to_human_readable_time(seconds):
    if seconds < 1:
        return 'no time'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{" " if amount == 1 else "s"}')
    return ', '.join(parts)
