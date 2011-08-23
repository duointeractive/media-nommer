"""
The following classes are resources/views that :doc:`feederd` makes available
via its JSON API.
"""
import json
from media_nommer.utils.views import BaseView
from media_nommer.core.job_state_backend import EncodingJob
from media_nommer.feederd.job_cache import JobCache

class JobSubmitView(BaseView):
    """
    This view is used to submit new encoding jobs. The data is parsed and
    a new job is created through feederd, which is then picked up by the
    ec2nommerd instances.
    """
    # The following top-level keys are checked before we get too far into
    # parsing the request body. If any of these are missing or evaluate to
    # a non-True boolean, send an error.
    required_keys = [
        'source_path', 'dest_path', 'job_options',
    ]

    # Similar to required_keys, but with the job_options dict.
    required_job_options_keys = [
        'options', 'nommer',
    ]

    def view(self):
        payload = json.loads(self.request.content.read())
        print(payload)

        for key in self.required_keys:
            if not payload.get(key):
                msg = "Missing/invalid required key+val: ['%s']" % key
                self.set_error(msg)
                return

        for key in self.required_job_options_keys:
            if not payload['job_options'].get(key):
                msg = "Missing/invalid required key+val: ['job_options'][%s]" % key
                self.set_error(msg)
                return

        source_path = payload['source_path']
        dest_path = payload['dest_path']
        notify_url = payload.get('notify_url')
        job_options = payload['job_options']['options']
        nommer = payload['job_options']['nommer']

        #print "SOURCE", source_path
        #print "DEST", dest_path
        #print "NOTIFY", notify_url
        #print "OPTIONS", job_options
        #print "NOMMER", nommer

        # Create a new job and save it to the DB/queue.
        job = EncodingJob(source_path, dest_path, nommer, job_options,
                          notify_url=notify_url)
        unique_job_id = job.save()
        # Add the job to the local job cache.
        JobCache.update_job(job)

        # This is serialized and returned to the user.
        self.context.update({'job_id': unique_job_id})
