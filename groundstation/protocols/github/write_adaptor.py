import copy
import json

import github

from groundstation.protocols.github import _identifier_, AbstractGithubAdaptor
from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

from groundstation import logger
log = logger.getLogger(__name__)


class GithubWriteAdaptor(AbstractGithubAdaptor):
    """GithubAdaptor(station, gh)

    Accepts a station and a github repo object (from PyGithub)
    """
    protocol = _identifier_

    @property
    def repo_name(self):
        return self.repo.full_name.replace("/", "_")

    def write_issue(self, issue):
        # Stupid implementation, blindly write with no deduping or merge
        # resolution.
        parents = []
        issue_id = self._issue_id(issue.number)
        gref = self.issue_gref(issue.number)

        def _write_new_tip(obj):
            our_parents = []
            while parents:
                our_parents.append(parents.pop())
            log.debug("Creating new object with parents: %s" % (str(our_parents)))

            oid = self.station.write(obj.as_object())
            self.station.update_gref(gref, [oid], our_parents)
            parents.append(oid)
            log.debug("Setting parents to: %s" % (str(parents)))

        def _parents():
            return copy.copy(parents)

        # Bail out if we've already written:
        if gref.exists():
            log.info("Not creating any objects, a gref already exists at: %s" % str(gref))
            return False

        # Write out a root object
        log.info(("Creating a new root_object with:\n" +
                  "id: %s\n" +
                  "channel: %s\n" +
                  "protocol: %s") % (issue_id, self.channel, self.protocol))

        root_object = RootObject(issue_id, self.channel, self.protocol)
        _write_new_tip(root_object)

        # Write out the initial state
        # Creating lots of tiny objects should make deduping easier later
        title_payload = {
                "type": "title",
                "id": None,
                "body": issue.title,
                "user": issue.user.login
                }
        update_object = UpdateObject(_parents(), json.dumps(title_payload))
        _write_new_tip(update_object)

        # Write out the body of the issue
        body_payload = {
                "type": "body",
                "id": None,
                "body": issue.body
                }
        update_object = UpdateObject(_parents(), json.dumps(body_payload))
        _write_new_tip(update_object)

        # Write out all of the comments and events
        everything = []
        everything.extend(issue.get_comments())
        everything.extend(issue.get_events())
        everything.sort(key=lambda x: x.created_at)
        for item in everything:
            if isinstance(item, github.IssueComment.IssueComment):
                payload = {
                        "type": "comment",
                        "id": item.id,
                        "body": item.body,
                        "user": item.user.login
                        }
            elif isinstance(item, github.IssueEvent.IssueEvent):
                payload = {
                        "type": "event",
                        "id": item.id,
                        "state": item.event,
                        "user": item.actor.login
                        }
            else:
                raise Exception("Unhandled item %s" % (repr(item)))

            update_object = UpdateObject(_parents(), json.dumps(payload))
            _write_new_tip(update_object)
