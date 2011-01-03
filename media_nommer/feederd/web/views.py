from media_nommer.utils.views import BaseView
from media_nommer.feederd.backends import get_storage_backend_from_conn_str

class JobSubmitView(BaseView):
    def view(self):
        print "REQ", self.request.args
        print "KW", self.kwargs
        print "CONT", self.context
        
        source_path = self.request.args['source_path'][0]
        print "SOURCE", source_path
        print "BACKEND", get_storage_backend_from_conn_str(source_path)