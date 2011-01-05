from media_nommer.utils.views import BaseView
from media_nommer.utils.uri_parsing import get_values_from_media_uri, InvalidUri
#from media_nommer.core.storage_backends import get_storage_backend_from_protocol
from media_nommer.core.job_state_backends import EncodingJob

class JobSubmitView(BaseView):
    def view(self):
        print "REQ", self.request.args
        print "KW", self.kwargs
        print "CONT", self.context

        source_path = self.request.args['source_path'][0]
        dest_path = self.request.args['dest_path'][0]
        notify_url = self.request.args['notify_url'][0]
        preset = self.request.args['preset'][0]
        job_options = self.request.args['job_options'][0]

        print "SOURCE", source_path
        print "DEST", dest_path
        print "NOTIFY", notify_url
        print "OPTIONS", job_options
        #values = get_values_from_media_uri(source_path)
        #print "VALUES", values
        #print "BACKEND", get_storage_backend_from_protocol(values['protocol'])

        job = EncodingJob(source_path, dest_path, preset, job_options,
                          notify_url=notify_url)
        job.save()
