import os
import tempfile
import subprocess
from media_nommer.core.nommers.base_nommer import BaseNommer

class EC2FFmpegNommer(BaseNommer):
    def _start_encoding(self):
        """
        Gets the show on the road.
        """
        print "STARTING TO NOM"
        fobj = self.download_source_file()
        # Encode the file. The return value is a tempfile with the output.
        out_fobj = self._run_ffmpeg(fobj)
        # Upload the encoding output file to its final destination.
        self.upload_to_destination(out_fobj)
        # TODO: Check to see if they wanted to delete or copy the original 
        # file after a successful run.

    def _run_ffmpeg(self, fobj):
        """
        Fire up ffmpeg and toss the results into a temporary file.
        """
        path = fobj.name
        out_fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)
        print "OUTPUT", out_fobj.name
        process = subprocess.Popen([
            'ffmpeg', '-y', '-i', path, '-target', 'ntsc-dvd', out_fobj.name
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print "===++=#+#+f=DF WHATISDHIST", process.communicate()
        print "RETURN CODE", process.returncode
        fobj.close()
        out_fobj.seek(0)
        return out_fobj
