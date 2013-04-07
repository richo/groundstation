_version_ = "0.0.0"
_identifier_ = "richo@psych0tik.net:github:%s" % (_version_)

from groundstation.gref import Gref

from groundstation.protocols import BaseProtocol

from groundstation import logger
log = logger.getLogger(__name__)


class AbstractGithubAdaptor(BaseProtocol):
    issue_format = "issues/%d"

    @property
    def channel(self):
        return "github:%s" % (self.repo_name)

    def issue_gref(self, issue):
        return Gref(self.station.store, self.channel, self._issue_id(issue))

    def _issue_id(self, issue):
        return self.issue_format % (issue)
