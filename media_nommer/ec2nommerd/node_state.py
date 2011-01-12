"""
Some methods for tracking and reporting the state of the ec2nommerd.
"""
import boto
import datetime
from twisted.internet import reactor
from media_nommer.conf import settings
from media_nommer.ec2nommerd.ec2_utils import get_instance_id

__NSTATE_CONN = boto.connect_sdb(settings.AWS_ACCESS_KEY_ID,
                                 settings.AWS_SECRET_ACCESS_KEY)

__NSTATE_DOM = __NSTATE_CONN.create_domain(settings.SIMPLEDB_EC2_NOMMER_STATE)

def send_instance_state_update():
    """
    Sends a status update to feederd through SimpleDB. Lets the daemon
    know how many jobs this instance is crunching right now. Also updates
    a timestamp field to let feederd know how long it has been since the
    instance's last check-in.
    """
    global __NSTATE_DOM
    item = __NSTATE_DOM.new_item(get_instance_id())
    item['id'] = get_instance_id()
    item['active_jobs'] = len(reactor.getThreadPool().working) - 1
    item['last_report_dtime'] = datetime.datetime.now()
    item.save()
