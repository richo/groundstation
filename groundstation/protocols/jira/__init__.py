_version_ = '0.0.0'
_identifier_ = "richo@psych0tik.net:jira:%s" % (_version_)

import copy
import json

from groundstation.gref import Gref

from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

from groundstation.protocols import BaseProtocol

from groundstation import logger
log = logger.getLogger(__name__)


class AbstractJiraAdaptor(BaseProtocol):
    @property
    def channel(self):
        return "jira:%s" % (self.repo)

    def issue_gref(self, issue):
        return Gref(self.station.store, self.channel, self._issue_id(issue))

    def _issue_id(self, issue):
        return issue.raw['key']


class JiraWriteAdaptor(AbstractJiraAdaptor):
    protocol = _identifier_

    def write_issue(self, issue):
        parents = []
        issue_id = self._issue_id(issue)
        gref = self.issue_gref(issue)

        def _write_new_tip(obj):
            our_parents = []
            while parents:
                our_parents.append(parents.pop())
            log.debug("Creating new object with parents: %s" % (str(our_parents)))

            oid = self.station.write(obj.as_object())
            self.station.update_gref(gref, [Tip(oid, "")], our_parents)
            parents.append(oid)
            log.debug("Setting parents to: %s" % (str(parents)))

        def _parents():
            return copy.copy(parents)


        if gref.exists():
            log.info("Not creating any objects, a gref already exists at: %s" % str(gref))
            return False

        log.info(("Creating a new root_object with:\n" +
                  "id: %s\n" +
                  "channel: %s\n" +
                  "protocol: %s") % (issue_id, self.channel, self.protocol))

        root_object = RootObject(issue_id, self.channel, self.protocol)
        _write_new_tip(root_object)

        # Write out the initial state
        # Creating lots of tiny objects should make deduping easier later
        if issue.fields.reporter:
            reporter = issue.fields.reporter.name
        else:
            reporter = "Anonymous"
        title_payload = {
                "type": "title",
                "id": None,
                "body": issue.fields.summary,
                "user": reporter
                }
        update_object = UpdateObject(_parents(), json.dumps(title_payload))
        _write_new_tip(update_object)

        # Write out the body of the issue
        body_payload = {
                "type": "body",
                "id": None,
                "body": issue.fields.description
                }
        update_object = UpdateObject(_parents(), json.dumps(body_payload))
        _write_new_tip(update_object)

        everything = []
        for comment in issue.fields.comment.comments:
            comment.type = "comment"
            everything.append(comment)
        for history in issue.changelog.histories:
            history.type = "event"
            everything.append(history)
        everything.sort(key=lambda x: x.created)
        for item in everything:
            if item.type == "comment":
                payload = {
                        "type": "comment",
                        "id": int(item.id),
                        "body": item.body,
                        "user": item.author.name
                        }
            elif item.type == "event":
                stateChange = ", ".join(["%s from %s to %s" %
                    (x.field, x.fromString, x.toString) for x in item.items])
                payload = {
                        "type": "event",
                        "id": item.id,
                        "state": stateChange,
                        "user": item.author.name
                        }
            else:
                raise Exception("Unhandled type")

            update_object = UpdateObject(_parents(), json.dumps(payload))
            _write_new_tip(update_object)
