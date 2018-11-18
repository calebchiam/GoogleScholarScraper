import scholarly
import re
from typing import List, Dict, Tuple
from random import shuffle

class Study():
    def __init__(self, title: str, url: str, author: str):
        self.title = title
        self.url = url
        self.author = author.split("-")[0].strip()

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_author(self):
        return self.author

    def __str__(self):
        return self.title + ", " + self.author + ", " + self.url


def get_all_studies(keywords: List[str]) -> List[Study]:
    retval = []
    shuffle(keywords)
    shuffled = ' '.join(keywords)
    print(shuffled)
    query = scholarly.search_pubs_query(shuffled)
    #
    # for i in range(10):
    #     try:
    #         res = next(query)
    #         retval.append(Study(res.bib['title'], res.bib['url'], res.bib['author']))
    #     except KeyError:
    #         retval.append(Study(res.bib['title'], "", res.bib['author']))
    #     except StopIteration:
    #         pass

    while True:
        try:
            res = next(query)
            retval.append(Study(res.bib['title'], res.bib['url'], res.bib['author']))
        except KeyError:
            retval.append(Study(res.bib['title'], "", res.bib['author']))
        except StopIteration:
            break

    return retval

def passes_filters(study: Study, includes: List[List[str]], excludes: List[str]) -> bool:
    title = re.sub('[,?!;]', " ", study.get_title())
    study_kw = set(title.lower().split())
    for f in includes:
        filter_set = set(f)
        if len(study_kw & filter_set) > 0:
            continue
        else:
            return False
    if len(study_kw & set(excludes)) > 0:
        return False
    return True

def filter_studies(studies: List[Study], includes: List[List[str]], excludes: List[str]) -> List[Study]:
    """
    Filters studies by title. Condition for inclusion is that the title contains
    one word from each filter list in filter
    Example: to get all studies with titles that contain
    (prevention, education, training) AND (violence, sexual, consent)
    use:
    [['prevention', 'education', 'training'], ['violence', 'sexual', 'consent']]
    as the filters argument
    """
    return [s for s in studies if passes_filters(s, includes, excludes)]


def write_studies_to_file(studies: List[Study], filename: str):
    with open(filename, 'w+') as f:
        for s in studies:
            f.write(str(s) + "\n")


def main():
    # Set to lowercase!
    filter1 = ['orientation', "change", "changes", "changing", "intervene", "intervention", "interventions",
               "intervening", 'train', 'training', "trainings", 'program', "programs", 'programming',
               'prevent', 'preventing', 'prevention', 'educate', 'educating',
               'education', 'protect', 'protects', 'protection', 'eliminate', 'elimination', 'eliminates']
    filter2 = ['sexual', 'assault', 'violence', 'consent', 'rape', 'bystander']
    others = ['college', 'campus', 'effectiveness']
    keywords = ['intervention', 'training', 'program', 'prevention', 'education'] + ['sexual', 'assault', 'violence', 'consent', 'rape'] + others

    studies = get_all_studies(keywords)

    write_studies_to_file(studies, "search_results.txt")

    print("Found {} search results on Google Scholar".format(len(studies)))
    includes = [filter1, filter2]
    excludes = ["military"]

    filtered_studies = filter_studies(studies, includes, excludes)

    write_studies_to_file(filtered_studies, "filtered_results.txt")

    print("After filtering, {} articles were deemed relevant".format(len(filtered_studies)))
    return filtered_studies


main()
