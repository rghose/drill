from datetime import datetime
import time
from collections import defaultdict, Counter
import matplotlib.pylab as plt

from pydriller import RepositoryMining
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount

GIT_PROJECT_URL = "https://github.com/eslint/eslint"


class CommitMapGeneration:
    @staticmethod
    def _filemap_from_modifications(modifications):
        file_map = {}
        try:
            for f in modifications:
                if f.filename in file_map:
                    file_map[f.filename] += 1
                else:
                    file_map[f.filename] = 1
        except Exception as e:
            print("problem with modification, ignoring")
        return file_map

    def __init__(self, git_project):
        self.map_authors = defaultdict(Counter)
        self.authors = set()
        self.map_files = defaultdict(Counter)
        self.files = set()
        self.git_project = git_project

    def generate_map_from_commits(self, start, end):
        rm_obj = RepositoryMining(self.git_project, since=start, to=end, only_in_branch='master')
        for commit in rm_obj.traverse_commits():
            rounded_date = commit.committer_date.replace(microsecond=0, second=0, minute=0, hour=0)
            author_name = commit.author.name.lower()
            self.map_authors[rounded_date].update({author_name: 1})
            if author_name not in self.authors:
                self.authors.add(author_name)
            # self.map_files[rounded_date].update(CommitMapGeneration._filemap_from_modifications(commit.modifications))

    def generate_multi_map(self):
        dates = self.map_authors.keys()
        author_map = dict()
        counter = 1
        for author in self.authors:
            author_map[author] = dict()
            for date in dates:
                contribs = 0
                if author in self.map_authors[date]:
                    contribs = self.map_authors[date][author]
                author_map[author][date] = contribs
            plt.plot(dates, author_map[author].values(), str(counter))
            counter += 1
            plt.show()


gm = CommitMapGeneration(GIT_PROJECT_URL)
ts_start = time.process_time()
gm.generate_map_from_commits(datetime(2013, 1, 1), datetime(2020, 8, 10))
print("Time taken : %s" % (time.process_time() - ts_start))

gm.generate_multi_map()
# metric = CommitsCount(project_url,
#                    since=datetime(2013, 1, 1),
#                    to=datetime(2020, 8, 10))
# files = metric.count()
# print('Files: {}'.format(files))
#
# metric = ContributorsCount(project_url,
#                    since=datetime(2013, 1, 1),
#                    to=datetime(2020, 8, 10))
# count = metric.count()
# minor = metric.count_minor()
# print('Number of contributors per file: {}'.format(count))
# print('Number of "minor" contributors per file: {}'.format(minor))
