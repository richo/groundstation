_version_ = '0.0.0'
_identifier_ = "richo@psych0tik.net:jira:%s" % (_version_)


class AbstractJiraAdaptor(object):

    def __init__(self, station, repo):
        self.station = station
        self.repo = repo
        self.channel = "jira:%s" % (self.repo)


class JiraWriteAdaptor(AbstractJiraAdaptor):
    protocol = _identifier_
