import ijson

def preprocess(parse_event_filter):
    """preprocess the stream"""
    # go into the array
    next(parse_event_filter)

def get_map_or_array(parse_event_filter, last_event):
    """get a map or array while advancing the iterator, used when the map or array is not huge
        last_event: a string used to indicate what happened last time
    """
    if last_event == 'start_array':
        ar = []
        while True:
            prefix, event, value = next(parse_event_filter)
            if event == 'end_array':
                return ar
            elif event == 'start_map':
                ar.append(get_map_or_array(parse_event_filter, event))
            elif event == 'start_array':
                ar.append(get_map_or_array(parse_event_filter, event))
            else:
                ar.append(value)
    elif last_event == 'start_map':
        mp = {}
        key = None
        while True:
            prefix, event, value = next(parse_event_filter)
            if event == 'end_map':
                return mp
            elif event == 'map_key':
                key = value
            elif event == 'start_map':
                mp[key] = get_map_or_array(parse_event_filter, event)
                key = None
            elif event == 'start_array':
                mp[key] = get_map_or_array(parse_event_filter, event)
                key = None
            else:
                mp[key] = value
                key = None

def get_event(parse_event_iter):
    """fetch an event from the stream of events, ignore incomplete event
        iterator: the iterator of parsing events(refer to ijson.common.parse for more details),
         must be preprocessed with eventfilter.preprocess
        returns the event as a dict, otherwise raises StopIteration
    """
    while True:
        prefix, event, value = next(parse_event_iter)
        if event == 'start_map':
            # event to return
            yield get_map_or_array(parse_event_iter, event)
        elif event == 'end_array':
            # the array of events got to its end
            return
        else:
            continue
        
def get_pevent(parse_event_iter):
    """fetch a pair of event from the stream of events
    """
    evg = get_event(parse_event_iter)
    while True:
        eva = next(evg)
        while eva["ph"] not in ('b', 'B'):
            eva = next(evg)
        evb = next(evg)
        while evb["ph"] not in ('e', 'E') and evb["name"] != eva["name"]:
            evb = next(evg)
        yield eva, evb


def get_filtered_event(parse_event_iter, fun):
    """fetch a pair of event satisfying the condition
        parse_event_filter: see eventfilter.get_event
        fun: the function, fun(pevent) should be True if the pair of event satisfies the condition, False otherwise
        yields a filtered event
    """
    evpg = get_pevent(parse_event_iter)
    while True:
        evp = next(evpg)
        if (fun(evp)):
            yield evp
        else:
            continue