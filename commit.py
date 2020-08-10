from pydriller import RepositoryMining
from datetime import datetime
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount


project_url = "https://github.com/eslint/eslint"
for commit in RepositoryMining(project_url, only_in_branch='master', filepath='package.json').traverse_commits():
    print(
            # commit.hash,
            commit.author.name,
            # commit.committer.name,
            commit.committer_date
    )
    # print(commit.author.name)


metric = CommitsCount(project_url,
                   since=datetime(2013, 1, 1),
                   to=datetime(2020, 8, 10))
files = metric.count()
print('Files: {}'.format(files))

metric = ContributorsCount(project_url,
                   since=datetime(2013, 1, 1),
                   to=datetime(2020, 8, 10))
count = metric.count()
minor = metric.count_minor()
print('Number of contributors per file: {}'.format(count))
print('Number of "minor" contributors per file: {}'.format(minor))
