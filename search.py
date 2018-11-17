import scholarly
from typing import List, Dict, Tuple


keywords = ['orientation', 'assault', 'campuses', 'sexual', 'consent',
            'violence', 'college', 'training', 'program', 'effectiveness',
            'campus', 'program', 'prevent', 'education', 'prevention']

queries = ['sexual assault prevention education',
           'sexual assault prevention program',
           'sexual assault prevention program campus',
           'effectiveness campus sexual assault prevention',
           "college orientation programs against sexual assault",
           "how to prevent sexual assault on college campuses",
           "sexual assault prevention training campus",
           "orientation sexual consent training",
           'sexual assault training program',
           'sexual violence prevention education',
           'sexual violence prevention'
           ]





search_query = scholarly.search_pubs_query('Perception of physical stability and center of mass of 3D objects')
print(next(search_query))
