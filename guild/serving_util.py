# Copyright 2017-2018 TensorHub, Inc.
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

import json
import logging
import socket

from werkzeug import routing
from werkzeug import serving
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request, Response

log = logging.getLogger("guild")

def make_server(host, port, app):
    if host is None:
        raise RuntimeError("host cannot be None")
    if port is None:
        raise RuntimeError("port cannot be None")
    try:
        return serving.make_server(host, port, app, threaded=True)
    except socket.error as e:
        if host:
            raise
        log.debug(
            "error starting server on %s:%s (%s), "
            "trying IPv6 default host '::'",
            host, port, e)
        return serving.make_server("::", port, app, threaded=True)

def json_resp(data):
    return Response(
        json.dumps(data),
        content_type="application/json",
        headers=[("Access-Control-Allow-Origin", "*")])

def Rule(path, handler, *args):
    return routing.Rule(path, endpoint=(handler, args))

def Map(rules):
    return routing.Map([
        Rule(path, handler, *args)
        for path, handler, args, in rules
    ])

def dispatch(routes, env, start_resp):
    urls = routes.bind_to_environ(env)
    try:
        (handler, args), kw = urls.match()
    except HTTPException as e:
        return e(env, start_resp)
    else:
        args = (Request(env),) + args
        kw = _del_underscore_vars(kw)
        try:
            return handler(*args, **kw)(env, start_resp)
        except HTTPException as e:
            return e(env, start_resp)

def _del_underscore_vars(kw):
    return {
        k: kw[k] for k in kw if k[0] != "_"
    }

def App(routes):
    def app(env, start_resp):
        return dispatch(routes, env, start_resp)
    return app