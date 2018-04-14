import ijson
import eventfilter
import itertools

file = open('profile.json')
it = ijson.parse(file)

eventfilter.preprocess(it)

counted = ((i, next(eventfilter.get_pevent(it))) for i in itertools.count())

print(list(itertools.takewhile(lambda x : x[0] < 10, counted)))
