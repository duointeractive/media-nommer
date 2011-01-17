import cgi
import simplejson
from media_nommer.utils.views import BaseView
from media_nommer.conf import settings
from media_nommer.core.job_state_backend import EncodingJob
from media_nommer.feederd.job_cache import JobCache

class JobSubmitView(BaseView):
    def view(self):
        print "REQ", self.request.args
        print "KW", self.kwargs
        print "CONT", self.context

        source_path = cgi.escape(self.request.args['source_path'][0])
        dest_path = cgi.escape(self.request.args['dest_path'][0])
        notify_url = cgi.escape(self.request.args['notify_url'][0])
        preset = cgi.escape(self.request.args['preset'][0])
        user_job_options = cgi.escape(self.request.args['job_options'][0])
        user_job_options = simplejson.loads(user_job_options)

        print "SOURCE", source_path
        print "DEST", dest_path
        print "NOTIFY", notify_url
        print "OPTIONS", user_job_options

        # Retrieve the given preset from nomconf.
        preset_dict = settings.PRESETS[preset]
        # Determine the nommer based on the preset.
        nommer = preset_dict['nommer']
        # Get the preset's job options dict.
        job_options = preset_dict['options']
        # Override preset's options with user-specified values.
        job_options.update(user_job_options)
        print "NEW OPTS", job_options

        # Create a new job and save it to the DB/queue.
        job = EncodingJob(source_path, dest_path, nommer, job_options,
                          notify_url=notify_url)
        unique_job_id = job.save()
        # Add the job to the local job cache.
        JobCache.update_job(job)

        # This is serialized and returned to the user.
        self.context = {'success': True, 'job_id': unique_job_id}
