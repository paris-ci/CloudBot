import asyncio
import time

from cloudbot import hook
import cloudbot


# CTCP responses
@asyncio.coroutine
@hook.regex(r'^\x01VERSION\x01$')
def ctcp_version(notice):
    """
    This will answer any CTCP version
    """
    notice("\x01VERSION: CloudBot {} - http://github.com/paris-ci/CloudBot/".format(cloudbot.__version__))


@asyncio.coroutine
@hook.regex(r'^\x01CLIENTINFO\x01$')
def ctcp_clientinfo(notice):
    """
    This will answer any CTCP CLIENTINFO
    """
    notice("\x01VERSION: CloudBot {} - http://github.com/paris-ci/CloudBot/".format(cloudbot.__version__))


@asyncio.coroutine
@hook.regex(r'^\x01PING\x01$')
def ctcp_ping(notice):
    """
    This will answer any CTCP ping
    """
    notice('\x01PING: PONG')


@asyncio.coroutine
@hook.regex(r'^\x01TIME\x01$')
def ctcp_time(notice):
    """
    This will answer any CTCP time with the server time
    """
    notice('\x01TIME: The time is: {}'.format(time.strftime("%r", time.localtime())))
