from enum import Enum
from functools import lru_cache

from github import Github
from naggy import config


class Labels(Enum):
    RFR = "Ready for review"


class GitHubProvider:

    def __init__(self):
        self._labels = {}
        self.api = Github(config['GITHUB_USERNAME'],
                          config['GITHUB_PASSWORD'])

    @property
    def organization(self):
        return self.get_organization()

    @property
    def labels(self):
        return self.get_labels()

    @property
    def repo(self):
        return self.get_repo()

    @property
    def issues(self):
        return self.get_issues()

    def get_organization(self):
        organization = self.api.get_organization(config['GITHUB_ORG'])
        return organization

    def get_repo(self):
        repo = self.organization.get_repo(config['GITHUB_REPO'])
        return repo

    @lru_cache(maxsize=32)
    def get_labels(self):
        labels = self.repo.get_labels()
        for label in labels:
            self._labels[label.name] = label
        return labels

    def get_issues(self, labels=None):
        if not labels:
            self.get_labels()
            labels = []
            rfr = self._labels.get(Labels.RFR.value)
            if rfr:
                labels.append(rfr)

        issues = self.repo.get_issues(labels=labels, sort='created')
        return issues
