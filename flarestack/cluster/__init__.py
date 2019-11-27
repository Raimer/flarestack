import numpy as np
import os
from flarestack.shared import host_server, make_analysis_pickle
from flarestack.cluster.run_desy_cluster import submit_to_cluster,\
    wait_for_cluster
from flarestack.cluster.make_desy_cluster_script import make_desy_submit_file
from flarestack.cluster.make_local_bash_script import local_submit_file,\
    make_local_submit_file
import logging
import multiprocessing

if host_server == "DESY":
    submit_cluster = submit_to_cluster
    wait_cluster = wait_for_cluster

else:
    def submit_cluster(path, **kwargs):
        raise Exception("No cluster submission script recognised!")


def submit_local(path, n_cpu):
    make_local_submit_file()

    bashfile = local_submit_file

    submit_cmd = bashfile + " " + path + " " + str(n_cpu)

    logging.info(submit_cmd)

    os.system(submit_cmd)


def analyse(mh_dict, cluster=False, n_cpu=min(os.cpu_count()-1, 32), **kwargs):
    """Generic function to run an analysis on a given MinimisationHandler
    dictionary. Can either run on cluster, or locally, based on the boolean
    cluster arg. The number of cpus can be specified, as well as specific
    kwargs such as number of jobs to run.

    :param mh_dict: MinimisationHandler dictionary
    :param cluster: Boolean flag for whether to run on cluster or locally.
    Default is False (i.e locally)
    :param n_cpu: Number of CPUs to run with. Should be 1 for submit to cluster
    :param kwargs: Optional kwargs
    """

    path = make_analysis_pickle(mh_dict)

    job_id = None

    if cluster:
        job_id = submit_cluster(path, n_cpu=n_cpu, **kwargs)
    else:
        submit_local(path, n_cpu=n_cpu)

    return job_id
