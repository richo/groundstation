_version_ = "0.0.0"
_identifier_ = "richo@psych0tik.net:github:%s" % (_version_)

import json
import copy

import github

from groundstation.gref import Gref

import groundstation.objects.object_factory as object_factory

from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

from groundstation import logger
log = logger.getLogger(__name__)


class AbstractGithubAdaptor(object):
    issue_format = "issues/%d"

    def __init__(self, station, repo):
        self.station = station
        self.repo = repo
        self.channel = "github:%s" % (self.repo_name)

    def issue_gref(self, issue):
        return Gref(self.station.store, self.channel, self._issue_id(issue))

    def _issue_id(self, issue):
        return self.issue_format % (issue)


class GithubReadAdaptor(AbstractGithubAdaptor):
    """GithubReadAdaptor(station, repo_name)

    Accepts a station and the name of a github repo, ie "richo/groundstation"
    """
    @property
    def repo_name(self):
        return self.repo

    def get_issue(self, issue):
        if isinstance(issue, Gref):
            gref = issue
        else:
            gref = self.issue_gref(issue)

        visited_nodes = []
        root_nodes = []
        issue_thread = []  # We'll treat this as a stack and pop the events off
                           # int he right order

        # Walk the tips backwards. To do this right, we should have kept
        # timestamps and used that for ordering
        def _process(node):
            if node not in visited_nodes:
                visited_nodes.append(node)
                log.debug("node: %s" % node)
                obj = object_factory.hydrate_object(self.station.store[node].data)
                if isinstance(obj, RootObject): # We've reached the back of this tree
                    root_nodes.append(obj)
                    return
                issue_thread.append(obj)
                for tip in obj.parents:
                    log.debug("Tip: %s" % tip)
                    _process(tip)

        for tip in gref:
            log.debug("Descending into %s" % (tip))
            _process(tip)

        assert len(root_nodes) == 1, \
            "Anything other than one root node and you've got a problem"

        issue_thread.append(root_nodes.pop())

        return issue_thread


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
