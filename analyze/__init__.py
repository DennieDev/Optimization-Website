import asyncio

from .get_content import get_content
from .get_version import get_version
from .get_jar import get_jar

return_list = []


def analyze_url(timings_url):
    # Loop for asyncio functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Get content from timings report
    content = loop.run_until_complete(get_content(timings_url))

    # Functions
    get_version(content.request_raw)
    get_jar(content.request_raw)

    return return_list
