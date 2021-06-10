import logging
import analyze


def get_cpu(request):
    try:
        cpu = int(request["timingsMaster"]["system"]["cpu"])
        if cpu == 1:
            analyze.return_list.append({
                'title': 'Threads',
                'body': f'You only have {cpu} thread. Find a better host'
            })
        if cpu == 2:
            analyze.return_list.append({
                'title': 'Threads',
                'body': f'You only have {cpu} threads. Find a better host'
            })
    except KeyError as key:
        logging.info("Missing: " + str(key))
