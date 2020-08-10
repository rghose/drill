from datetime import datetime
import time
import math
from collections import defaultdict, Counter
import matplotlib.pylab as plt

from pydriller import RepositoryMining
# from pydriller.metrics.process.commits_count import CommitsCount
# from pydriller.metrics.process.contributors_count import ContributorsCount

GIT_PROJECT_URL = "https://github.com/eslint/eslint"


class CommitMapGeneration:
    def _filemap_from_modifications(self, modifications):
        file_map = {}
        try:
            for f in modifications:
                if f.filename in file_map:
                    file_map[f.filename] += 1
                else:
                    file_map[f.filename] = 1
                if f.filename not in self.files:
                    self.files[f.filename] = 0
                self.files[f.filename] += 1
        except Exception as e:
            print("problem with modification, ignoring", e)
        return file_map

    def __init__(self, git_project: str, start: datetime, end: datetime,
                 branch='master', interval_months=1):
        self.map_authors = defaultdict(Counter)
        self.authors = dict()
        self.map_files = defaultdict(Counter)
        self.files = dict()
        self.git_project = git_project
        self.interval_months = interval_months
        self.rm_obj = RepositoryMining(self.git_project,
                                       since=start, to=end,
                                       only_in_branch=branch)

    def get_hash_integer(self, date) -> int:
        return int(100 * float("{}.{}".format(date.year, 1 + math.floor((date.month-1) / self.interval_months))))

    def generate_user_map_from_commits(self):
        for commit in self.rm_obj.traverse_commits():
            date_bucket = self.get_hash_integer(commit.committer_date)
            author_name = commit.author.name.lower()
            self.map_authors[date_bucket].update({author_name: 1})
            if author_name not in self.authors:
                self.authors[author_name] = 1
            else:
                self.authors[author_name] += 1

    def generate_file_map_from_commits(self):
        for commit in self.rm_obj.traverse_commits():
            date_bucket = self.get_hash_integer(commit.committer_date)
            files_map = self._filemap_from_modifications(commit.modifications)
            self.map_files[date_bucket].update(files_map)

    def generate_multi_map_users(self, top=5):
        author_map = dict()
        counter = 1
        sorted_authors = Counter(self.authors).most_common(top)
        dates = self.map_authors.keys()
        for author, total_contribs in sorted_authors:
            author_map[author] = dict()
            for date in dates:
                contribs = 0
                if author in self.map_authors[date]:
                    contribs = self.map_authors[date][author]
                author_map[author][date] = contribs
            plt.plot(dates, author_map[author].values())
            counter += 1
        plt.show()

    def generate_multi_map_files(self, file_name):
        dates = self.map_files.keys()
        file_updates = []
        for date in dates:
            if file_name in self.map_files[date]:
                file_updates.append(self.map_files[date][file_name])
            else:
                file_updates.append(0)
        plt.plot(dates, file_updates)
        plt.show()


gm = CommitMapGeneration(GIT_PROJECT_URL,
                         datetime(2013, 1, 1),
                         datetime(2020, 8, 10), interval_months=3)
# ts_start = time.process_time()
# gm.generate_user_map_from_commits()
# print("Time taken for user map : %s" % (time.process_time() - ts_start))

# gm.generate_multi_map_users()
ts_start = time.process_time()
gm.generate_file_map_from_commits()
print("Time taken for file map: %s" % (time.process_time() - ts_start))
gm.generate_multi_map_files("package.json")

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
