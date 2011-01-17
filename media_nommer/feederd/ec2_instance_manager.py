"""
Contains an instance management class with some basic intelligence for
managing EC2 instances for the various nommers.
"""
import boto
from boto.exception import EC2ResponseError
from media_nommer.conf import settings
from media_nommer.core.job_state_backend import JobStateBackend

class EC2InstanceManager(object):
    """
    This class manages the creation and termination of EC2 images, based
    on the size of the job queue in relation to the amount of manpower
    available at any point in time.
    """
    # Used for lazy-loading the EC2 connection. Do not refer to directly.
    _aws_ec2_connection = None

    @classmethod
    def aws_ec2_connection(cls):
        """
        Lazy-loading of the EC2 boto connection. Refer to this instead of
        referencing cls._aws_ec2_connection directly.
        
        :returns: A boto connection to Amazon's EC2 interface.
        """
        if not cls._aws_ec2_connection:
            cls._aws_ec2_connection = boto.connect_ec2(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return cls._aws_ec2_connection

    @classmethod
    def get_instances(cls):
        """
        Returns a list of boto.ec2.instance.Instance objects matching the
        media-nommer AMI, as per settings.EC2_AMI_ID. Also filters only
        running instances.
        
        :rtype: list
        :returns: A list of boto.ec2.instance.Instance objects representing
            currently active media-nommer ec2nommerd instances.
        """
        # Instances must be in these states to make it through the filter.
        counted_states = ['running', 'pending']
        # Get a list of reservations for all running instances.
        reservations = cls.aws_ec2_connection().get_all_instances()
        # Hold a list of Instance objects to return.
        instances = []
        for r in reservations:
            for i in r.instances:
                if i.image_id == settings.EC2_AMI_ID and i.state in counted_states:
                    # Passed filters, this is a media-nommer instance.
                    instances.append(i)

        return instances

    @classmethod
    def spawn_if_needed(cls):
        """
        Spawns additional EC2 instances if needed.
        
        :rtype: Reservation or None
        :returns: If instances are spawned, return a boto Reservation
            object. If no instances are spawned, ``None`` is returned.
        """
        instances = cls.get_instances()
        num_instances = len(instances)
        print "NUM INSTANCES", num_instances

        if num_instances >= settings.MAX_NUM_EC2_INSTANCES:
            # No more instances, no spawning allowed.
            return

        unfinished_jobs = JobStateBackend.get_unfinished_jobs()
        num_unfinished_jobs = len(unfinished_jobs)
        print "UNFINISHED JOBS", num_unfinished_jobs

        job_capacity = num_instances * settings.MAX_ENCODING_JOBS_PER_EC2_INSTANCE
        print "JOB CAPACITY", job_capacity

        cap_plus_thresh = job_capacity + settings.EC2_JOB_OVERFLOW_THRESH
        print "PLUS THRESH", cap_plus_thresh

        is_over_capacity = num_unfinished_jobs >= cap_plus_thresh
        has_jobs_but_no_nommers = num_unfinished_jobs > 0 and num_instances == 0
        if is_over_capacity or has_jobs_but_no_nommers:
            overage = num_unfinished_jobs - job_capacity
            overage -= settings.EC2_JOB_OVERFLOW_THRESH
            print "OVERAGE", overage
            num_new_instances = overage / settings.MAX_ENCODING_JOBS_PER_EC2_INSTANCE
            num_new_instances = max(num_new_instances, 1)
            print "SPAWNEM!", num_new_instances
            return cls.spawn_instances(num_new_instances)
        return None

    @classmethod
    def spawn_instances(cls, num_instances):
        """
        Spawns the number of instances specified.
        
        :param int num_instances: The number of instances to spawn.
        :returns: A boto Reservation for the started instance(s).
        """
        print "SPAWNING", num_instances
        conn = cls.aws_ec2_connection()

        try:
            image = conn.get_all_images(image_ids=settings.EC2_AMI_ID)
            image = image[0]
        except EC2ResponseError:
            print "ERROR: No AMI with ID %s could be found." % settings.EC2_AMI_ID
            return
        except IndexError:
            print "ERROR: No AMI with ID %s could be found." % settings.EC2_AMI_ID
            return

        return image.run(min_count=num_instances, max_count=num_instances,
                         instance_type=settings.EC2_INSTANCE_TYPE,
                         security_groups=settings.EC2_SECURITY_GROUPS,
                         key_name=settings.EC2_KEY_NAME,
                         user_data=cls._gen_ec2_user_data())

    @classmethod
    def _gen_ec2_user_data(cls):
        """
        Generates the User-Data param to pass to Ubuntu Server's cloud-init.
        This will cause certain things to be done at startup time.
        
        :rtype: str
        :returns: A user data string for :py:meth:`spawn_instances` to use.
        """
        user_data = "#cloud-config\n" \
                    "apt_update: true\n\n" \
                    "apt_upgrade: true\n\n" \
                    "runcmd:\n" \
                    " - chmod 777 /tmp\n" \
                    " - echo \"s3://%s:%s@%s/nomconf.py\" > /home/nom/.nommerd_s3.cfg\n" \
                    " - chown nom:nom /home/nom/.nommerd_s3.cfg\n" \
                    " - sudo -u nom -i /home/nom/.virtualenvs/media_nommer/bin/pip install --upgrade git+http://github.com/duointeractive/media-nommer.git#egg=media_nommer > /tmp/media_nom_upgrade.log\n" \
                    " - supervisorctl start ec2nommerd > /tmp/superv_start.log" % (
                        settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY,
                        settings.CONFIG_S3_BUCKET,
                    )
        return user_data
