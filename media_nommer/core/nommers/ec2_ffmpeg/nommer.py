from media_nommer.core.nommers.base_nommer import BaseNommer

class EC2FFmpegNommer(BaseNommer):
    def start_encoding(self):
        print "STARTING TO NOM"
