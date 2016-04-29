import functools
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger(__name__)


def resp_to_string(resp):
    """Convert a resp (from the requests lib) to a string."""
    if resp is None:
        return "<resp is None!>"
    msg = "\n----------------- Request -----------------"
    msg += "\n[{2}] {0} {1}".format(
        resp.request.method, resp.request.url, resp.status_code,
    )
    for k, v in resp.request.headers.items():
        msg += "\n{0}: {1}".format(k, v)
    if resp.request.body:
        msg += "\n{0}".format(resp.request.body)

    msg += "\n----------------- Response -----------------"
    msg += "\n{0} {1}".format(resp.status_code, resp.reason)
    for k, v in resp.headers.items():
        msg += "\n{0}: {1}".format(k, v)

    if resp.text and len(resp.text) > 1000:
        msg += "\n{0}... <truncated>".format(resp.text[:1000])
    else:
        msg += "\n{0}".format(resp.text)
    return msg + '\n'


def log_response(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        resp = f(*args, **kwargs)
        LOG.debug(resp_to_string(resp))
        return resp
    return wrapped
