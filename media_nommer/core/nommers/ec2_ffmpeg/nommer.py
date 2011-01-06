import os
import tempfile
import subprocess
from media_nommer.core.nommers.base_nommer import BaseNommer

class EC2FFmpegNommer(BaseNommer):
    def start_encoding(self):
        print "STARTING TO NOM"
        fobj = self.download_source_file()
        out_fobj = self.run_ffmpeg(fobj)
        self.upload_to_destination(out_fobj)

    def run_ffmpeg(self, fobj):
        path = fobj.name
        out_fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)
        print "OUTPUT", out_fobj.name
        retval = subprocess.check_output([
            'ffmpeg', '-y', '-i', path, '-target', 'ntsc-dvd', out_fobj.name
        ])
        fobj.close()
        out_fobj.seek(0)
        return out_fobj
