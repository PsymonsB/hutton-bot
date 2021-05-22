import vars

graph_count = 0
api_count = 0

def display_time(seconds, granularity=4):
    result = []

    for name, count in vars.INTERVALS:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])


def inf_emoji(inf):
    result = ""

    if inf >= 61:
        result = vars.EMOJIS["high"]
    elif inf <= 40:
        result = vars.EMOJIS["low"]
    else:
        result = vars.EMOJIS["ok"]

    return result

def graph_increment():
    global graph_count
    graph_count = graph_count + 1

def api_increment():
    global api_count
    api_count = api_count + 1

def progress(count, total, status=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '░' * (bar_len - filled_len)

    finishedbar = "[" + bar + "]...." + str(percents) + "%...." + status

    return finishedbar

def split_lines(str, limit, sep="\n"):
    lines = str.rsplit("\n")
    if max(map(len, lines)) > limit:
        raise ValueError("limit is too small")
    res, part, others = [], lines[0], lines[1:]
    for line in others:
        if len(sep)+len(line) > limit-len(part):
            res.append(part)
            part = line
        else:
            part += sep+line
    if part:
        res.append(part)
    return res
