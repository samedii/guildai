# Copyright 2017-2019 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import logging
import subprocess

from guild import remote as remotelib

log = logging.getLogger("guild.remotes.ssh_util")

DEFAULT_CONNECT_TIMEOUT = 10

def ssh_ping(host, port=None, user=None, verbose=False,
             connect_timeout=DEFAULT_CONNECT_TIMEOUT):
    host = _full_host(host, user)
    cmd = ["ssh"] + _ssh_opts(port, None, verbose, connect_timeout) + [host, "true"]
    result = subprocess.call(cmd)
    if result != 0:
        raise remotelib.Down("cannot reach host %s" % host)

def _full_host(host, user):
    if user:
        return "%s@%s" % (user, host)
    else:
        return host

def ssh_cmd(host, cmd, user=None, port=None, private_key=None,
            connect_timeout=DEFAULT_CONNECT_TIMEOUT):
    cmd = _ssh_cmd(host, port, cmd, user, private_key, connect_timeout)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        raise remotelib.RemoteProcessError.from_called_process_error(e)

def _ssh_cmd(host, port, cmd, user, private_key, connect_timeout):
    host = _full_host(host, user)
    return (
        ["ssh"] +
        _ssh_opts(port, private_key, False, connect_timeout) +
        [host] +
        cmd)

def ssh_output(host, cmd, user=None, private_key=None,
               connect_timeout=DEFAULT_CONNECT_TIMEOUT):
    cmd = _ssh_cmd(host, cmd, user, private_key, connect_timeout)
    log.debug("ssh cmd: %r", cmd)
    try:
        return subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        raise remotelib.RemoteProcessError.from_called_process_error(e)

def _ssh_opts(port=None, private_key=None, verbose=False, connect_timeout=None):
    opts = [
        "-oStrictHostKeyChecking=no"
    ]
    if port:
        opts.append("-p %d" % port)
    if private_key:
        opts.extend(["-i", private_key])
    if verbose:
        opts.append("-vvv")
    if connect_timeout:
        opts.append("-oConnectTimeout=%s" % connect_timeout)
    return opts

def rsync_copy_to(src, host, host_dest, user=None, port=None, private_key=None):
    dest = format_rsync_host_path(host, host_dest, user)
    cmd = (
        ["rsync", "-vr"] +
        rsync_ssh_opts(port, private_key) +
        [src, dest])
    log.debug("rsync cmd: %r", cmd)
    subprocess.check_call(cmd)

def format_rsync_host_path(host, path, user):
    if user:
        return "{}@{}:{}".format(user, host, path)
    else:
        return "{}:{}".format(host, path)

def rsync_ssh_opts(port, private_key):
    opts = ["-vr"]

    ssh_opts = []

    if port:
        ssh_opts.extend(["-p", port])

    if private_key:
        ssh_opts.extend(["-i", private_key])

    if ssh_opts:
        opts.extend(["-e", "ssh '{}'".format(" ".join(ssh_opts))])

    return opts
