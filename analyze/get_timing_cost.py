import logging
import analyze


def get_timing_cost(request):
    try:
        timing_cost = int(request["timingsMaster"]["system"]["timingcost"])
        if timing_cost > 300:
            analyze.return_list.append({
                'title': 'Timingcost',
                'body': f'Your timingcost is {timing_cost}. Your cpu is overloaded and/or slow. Find a better host'
            })

    except KeyError as key:
        logging.info("Missing: " + str(key))
