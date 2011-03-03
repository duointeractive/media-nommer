"""
Contains a class used for nomming media on EC2 via FFmpeg_. This is used in
conjunction with the ec2nommerd Twisted_ plugin.
"""
import os
import tempfile
import subprocess
from media_nommer.utils import logger
from media_nommer.ec2nommerd.nommers.base_nommer import BaseNommer

class FFmpegNommer(BaseNommer):
    """
    This :ref:`Nommer <nommers>` is used to encode media with the excellent
    FFmpeg_ utility.
    
    **Presets**
    
    Below is an example 
    :py:data:`PRESETS <media_nommer.conf.settings.PRESETS>`
    dict for FFmpegNommer::
    
        'your_preset_name_here': {
            'nommer': 'media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer',
            'options': [
                {
                    # These would be passed as infile options to ffmpeg
                    'infile_options': {
                    },
                    # These are passed as outfile options to ffmpeg
                    'outfile_options': {
                        's': '320x240',
                        # Some flags don't have values, like sameq
                        'sameq': None,
                        'ar': '22050',
                        'ab': '48',
                    }
                }, # end pass 1
            ], # end encoding pass list (max of 2)
        } # end preset
        
    In this case, the command created by this nommer would end up being::
        
        ffmpeg -y -i <infilename> -s 320x240 -sameq -ar 22050 -ab 48 <outfilename>
    
    Note that the ``sameq`` key in our ``outfile_options`` dict above has a
    ``None`` value. You'll need to do this for flags or options that don't
    require a value.
    
    .. tip:: Everything specified in the ``options`` dict may be overridden
        in your encoding API requests. These merely act as presets.
        
    If you want no options by default, this is OK too::
    
        'minimal_preset': {
            'nommer': 'media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer'
        }
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

        # Clean these up explicitly, just in case.
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
        for key, val in option_dict:
            cmd_list.append('-%s' % key)
            if val or val == 0:
                # None values are not used.
                cmd_list.append(str(val))

    def __assemble_ffmpeg_cmd_list(self, encoding_pass_options, infile_obj,
                                   outfile_obj, is_two_pass=False,
                                   is_second_pass=False):
        """
        Assembles a command list that subprocess.Popen() will use within
        self.__run_ffmpeg().
        
        :param file infile_obj: A file-like object for input.
        :param file outfile_obj: A file-like object to store the output.
        :rtype: list
        :returns: A list to be passed to subprocess.Popen().
        """
        #ffmpeg [[infile options][-i infile]]... {[outfile options] outfile}...
        ffmpeg_cmd = ['ffmpeg', '-y']

        # Form the ffmpeg infile and outfile options from the options
        # stored in the SimpleDB domain.
        if encoding_pass_options.has_key('infile_options'):
            infile_opts = encoding_pass_options['infile_options']
            self.__append_inout_opts_to_cmd_list(infile_opts, ffmpeg_cmd)

        # Specify infile
        ffmpeg_cmd += ['-i', infile_obj.name]

        if encoding_pass_options.has_key('outfile_options'):
            outfile_opts = encoding_pass_options['outfile_options']
            self.__append_inout_opts_to_cmd_list(outfile_opts, ffmpeg_cmd)

        if is_two_pass and not is_second_pass:
            # First pass of a 2-pass encoding.
            ffmpeg_cmd.append('/dev/null')
        else:
            # Second pass of a 2-pass encoding, or one-pass.
            ffmpeg_cmd.append(outfile_obj.name)

        logger.debug("FFmpegNommer.__run_ffmpeg(): Command to run: %s" % ' '.join(ffmpeg_cmd))

        return ffmpeg_cmd

    def __run_ffmpeg(self, fobj):
        """
        Fire up ffmpeg and toss the results into a temporary file.
        
        :rtype: file-like object or ``None``
        :returns: If the encoding succeeds, a file-like object is returned.
            If an error happens, ``None`` is returned, and the ERROR job
            state is set.
        """
        is_two_pass = len(self.job.job_options) > 1
        out_fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)

        pass_counter = 1
        for encoding_pass_options in self.job.job_options:
            is_second_pass = pass_counter == 2
            # Based on the given options, assemble the command list to
            # pass on to Popen.
            ffmpeg_cmd = self.__assemble_ffmpeg_cmd_list(
                             encoding_pass_options,
                             fobj, out_fobj,
                             is_two_pass=is_two_pass,
                             is_second_pass=is_second_pass)

            # Do this for ffmpeg's sake. Allows more than one concurrent
            # encoding job per EC2 instance.
            os.chdir(self.temp_cwd)
            # Fire up ffmpeg.
            process = subprocess.Popen(ffmpeg_cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            # Get back to home dir. Not sure this is necessary, but meh.
            os.chdir(os.path.expanduser('~'))
            # Block here while waiting for output
            cmd_output = process.communicate()

            # 0 is success, so anything but that is bad.
            error_happened = process.returncode != 0

            if not error_happened and (is_second_pass or not is_two_pass):
                # No errors, return the file object for uploading.
                out_fobj.seek(0)
                return out_fobj
            elif error_happened:
                # Error found, return nothing so the nommer can die.
                logger.error(message_or_obj="Error encountered while running ffmpeg.")
                logger.error(message_or_obj=cmd_output[0])
                logger.error(message_or_obj=cmd_output[1])
                self.wrapped_set_job_state('ERROR', details=cmd_output[1])
                return None

            pass_counter += 1
