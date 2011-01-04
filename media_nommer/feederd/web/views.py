from media_nommer.utils.views import BaseView
from media_nommer.utils.uri_parsing import get_values_from_media_uri, InvalidUri
from media_nommer.feederd.backends import get_storage_backend_from_protocol

class JobSubmitView(BaseView):
    def view(self):
        print "REQ", self.request.args
        print "KW", self.kwargs
        print "CONT", self.context

        source_path = self.request.args['source_path'][0]
        print "SOURCE", source_path
        values = get_values_from_media_uri(source_path)
        print "VALUES", values
        #print "BACKEND", get_storage_backend_from_protocol(values['protocol'])
