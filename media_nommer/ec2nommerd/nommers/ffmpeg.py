"""
Contains a class used for nomming media on EC2 via FFmpeg_. This is used in
conjunction with the ec2nommerd Twisted_ plugin.
"""
import tempfile
import subprocess
from media_nommer.utils import logger
from media_nommer.ec2nommerd.nommers.base_nommer import BaseNommer

class FFmpegNommer(BaseNommer):
    """
    A nommer that runs on EC2 instances, encoding media with FFmpeg_.
    """
    def _start_encoding(self):
        """
        Best thought of as a ``main()`` method for the Nommer. This is the
        main bit of logic that directs the encoding process.
        """
        logger.info("Starting to encode job %s" % self.job.unique_id)
        fobj = self.download_source_file()

        # Encode the file. The return value is a tempfile with the output.
        out_fobj = self.__run_ffmpeg(fobj)
        if not out_fobj:
            # Failure! We're going nowhere.
            fobj.close()
            return False

        # Upload the encoding output file to its final destination.
        self.upload_to_destination(out_fobj)

        self.wrapped_set_job_state('FINISHED')
        logger.info("FFmpegNommer: Job %s has been successfully encoded." % self.job.unique_id)
        fobj.close()
        out_fobj.close()
        return True

    def __append_inout_opts_to_cmd_list(self, option_dict, cmd_list):
        """
        Takes user or preset options and adds them as arguments to the
        command list that will be ran with ``Popen()``.
        
        :param dict option_dict: The options to add to the command list.
        :param list cmd_list: The list being formed to pass to ``Popen()``
            in :py:meth:`__run_ffmpeg`.
        """
        for key, val in option_dict.items():
            cmd_list.append('-%s' % key)
            cmd_list.append(val)

    def __run_ffmpeg(self, fobj):
        """
        Fire up ffmpeg and toss the results into a temporary file.
        
        :rtype: file-like object or ``None``
        :returns: If the encoding succeeds, a file-like object is returned.
            If an error happens, ``None`` is returned, and the ERROR job
            state is set.
        """
        path = fobj.name
        out_fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)

        #ffmpeg [[infile options][-i infile]]... {[outfile options] outfile}...
        ffmpeg_cmd = ['ffmpeg', '-y']

        # Form the ffmpeg infile and outfile options from the options
        # stored in the SimpleDB domain.
        if self.job.job_options.has_key('infile_options'):
            infile_opts = self.job.job_options['infile_options']
            self.__append_inout_opts_to_cmd_list(infile_opts, ffmpeg_cmd)

        # Specify infile
        ffmpeg_cmd += ['-i', path]

        if self.job.job_options.has_key('outfile_options'):
            outfile_opts = self.job.job_options['outfile_options']
            self.__append_inout_opts_to_cmd_list(outfile_opts, ffmpeg_cmd)

        ffmpeg_cmd.append(out_fobj.name)

        logger.debug("FFmpegNommer.__run_ffmpeg(): Command to run: %s" % ffmpeg_cmd)

        process = subprocess.Popen(ffmpeg_cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        cmd_output = process.communicate()

        # 0 is success, so anything but that is bad.
        error_happened = process.returncode != 0

        if not error_happened:
            # No errors, return the file object for uploading.
            out_fobj.seek(0)
            return out_fobj
        else:
            # Error found, return nothing so the nommer can die.
            logger.error(message_or_obj="Error encountered while running ffmpeg.")
            logger.error(message_or_obj=cmd_output[0])
            logger.error(message_or_obj=cmd_output[1])
            self.wrapped_set_job_state('ERROR', details=cmd_output[1])
            return None
