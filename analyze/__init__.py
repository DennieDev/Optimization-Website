import asyncio
import logging

from .get_content import get_content
from .get_version import get_version
from .get_jar import get_jar
from .get_timing_cost import get_timing_cost
from .get_java import get_java
from .get_flags import get_flags
from .get_cpu import get_cpu
from .get_datapacks import get_datapacks
from .get_plugins import get_plugins
from .get_shady_plugins import get_shady_plugins
from .get_tweaks import get_tweaks
from .get_gamerules import get_gamerules
from .get_tps import get_tps

return_list = []
tps = []


def analyze_url(timings_url):
    # Clear Values
    return_list.clear()
    tps.clear()

    # Loop for asyncio functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Get content from timings report
    content = loop.run_until_complete(get_content(timings_url))

    try:
        # Functions
        get_version(content.request)
        get_jar(content.request)
        get_timing_cost(content.request)
        get_java(content.request)
        get_flags(content.request)
        get_cpu(content.request)
        get_datapacks(content.request_raw)  # Needs request_raw not request
        get_plugins(content.request)
        get_shady_plugins(content.request)
        get_tweaks(content.request, content.request_raw)  # Needs request AND request_raw
        get_datapacks(content.request_raw)  # Needs request_raw not request

        # Get TPS Color
        get_tps(content.request)

    except ValueError as value_error:
        logging.info(value_error)
        return_list.append({
            'title': 'Value Error',
            'body': value_error
        })

    if len(return_list) == 0:
        return_list.append({
            'title': 'All Good',
            'body': 'Analyzed with no recommendations'
        })

    return return_list


def get_tps_color():
    return tps
