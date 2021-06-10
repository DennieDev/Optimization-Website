import aiohttp


class ReturnValue:
    def __init__(self, request_raw, request):
        self.request_raw = request_raw
        self.request = request


async def get_content(timings_url):
    timings_host, timings_id = timings_url.split("?id=")
    timings_json = timings_host + "data.php?id=" + timings_id
    timings_url_raw = timings_url + "&raw=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(timings_url_raw) as response:
            request_raw = await response.json(content_type=None)
        async with session.get(timings_json) as response:
            request = await response.json(content_type=None)
    if request is None or request_raw is None:
        invalid = "Invalid report, Create a new timings report."
        return

    return_object = ReturnValue(request_raw, request)

    return return_object
