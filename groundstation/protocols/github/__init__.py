_version_ = "0.0.0"
_identifier_ = "richo@psych0tik.net:github:%s" % (_version_)

import json

from groundstation.gref import Gref

from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

from groundstation import logger
log = logger.getLogger(__name__)

__doc__ = """\
GithubAdaptor(station, gh)

Accepts a station and a github repo object (from PyGithub)
"""

class GithubAdaptor(object):
    protocol = _identifier_

    def __init__(self, station, repo):
        self.station = station
        self.repo = repo
        self.repo_name = repo.full_name.replace("/", "_")
        self.channel = "github:%s" % (repo.full_name)

    def issue_gref(self, issue):
        return Gref(self.station.store, self.channel, self._issue_id(issue))

    def _issue_id(self, issue):
        return "issues/%d" % (issue.number)

    def write_issue(self, issue):
        # Stupid implementation, blindly write with no deduping or merge
        # resolution.

        issue_id = self._issue_id(issue)

        # Bail out if we've already written:
        gref = self.issue_gref(issue)
        if gref.exists():
            log.info("Not creating any objects, a gref already exists at: %s" % str(gref))
            return False

        # Write out a root object
        log.info(("Creating a new root_object with:\n" +
                  "id: %s\n" +
                  "channel: %s\n" +
                  "protocol: %s") % (issue_id, self.channel, self.protocol))

        root_object = RootObject(issue_id, self.channel, self.protocol)
        root_object_oid = self.station.write(root_object.as_object())
        self.station.update_gref(gref, [root_object_oid])

        # Write out the initial state
        # Creating lots of tiny objects should make deduping easier later
        title_payload = {
                "type": "title",
                "id": None,
                "body": issue.title
                }
        update_object = UpdateObject([root_object_oid], json.dumps(title_payload))
        update_object_oid = self.station.write(update_object.as_object())
        self.station.update_gref(gref, [update_object_oid], [root_object_oid])
