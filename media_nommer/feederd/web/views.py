import json
from media_nommer.utils.views import BaseView
from media_nommer.core.job_state_backend import EncodingJob
from media_nommer.feederd.job_cache import JobCache

class JobSubmitView(BaseView):
    def view(self):
        payload = json.loads(self.request.content.read())
        print(payload)

        source_path = payload['source_path']
        dest_path = payload['dest_path']
        notify_url = payload['notify_url']
        job_options = payload['job_options']['options']
        nommer = payload['job_options']['nommer']

        print "SOURCE", source_path
        print "DEST", dest_path
        print "NOTIFY", notify_url
        print "OPTIONS", job_options
        print "NOMMER", nommer

        # Create a new job and save it to the DB/queue.
        job = EncodingJob(source_path, dest_path, nommer, job_options,
                          notify_url=notify_url)
        unique_job_id = job.save()
        # Add the job to the local job cache.
        JobCache.update_job(job)

        # This is serialized and returned to the user.
        self.context.update({'job_id': unique_job_id})
