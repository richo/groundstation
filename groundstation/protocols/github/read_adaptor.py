from groundstation.protocols.github import _identifier_, AbstractGithubAdaptor
from groundstation.gref import Gref


class GithubReadAdaptor(AbstractGithubAdaptor):
    """GithubReadAdaptor(station, repo_name)

    Accepts a station and the name of a github repo, ie "richo/groundstation"
    """
    @property
    def repo_name(self):
        return self.repo

    def get_issue(self, issue, **kwargs):
        if isinstance(issue, Gref):
            gref = issue
        else:
            gref = self.issue_gref(issue)

        marshalled_gref = gref.marshall(**kwargs)

        assert len(marshalled_gref["roots"]) == 1, \
            "Anything other than one root node and you've got a problem"

        return marshalled_gref
