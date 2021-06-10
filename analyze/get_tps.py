import logging
import analyze


def get_tps(request):
    try:
        normal_ticks = request["timingsMaster"]["data"][0]["totalTicks"]
        worst_tps = 20
        for index in range(len(request["timingsMaster"]["data"])):
            total_ticks = request["timingsMaster"]["data"][index]["totalTicks"]
            if total_ticks == normal_ticks:
                end_time = request["timingsMaster"]["data"][index]["end"]
                start_time = request["timingsMaster"]["data"][index]["start"]
                tps = total_ticks / (end_time - start_time)
                if tps < worst_tps:
                    worst_tps = tps
        if worst_tps < 10:
            red = 255
            green = int(255 * (0.1 * worst_tps))
        else:
            red = int(255 * (-0.1 * worst_tps + 2))
            green = 255
        color = (red, green, 0)
        analyze.tps = [round(worst_tps, 2), color]

    except KeyError as key:
        logging.info("Missing: " + str(key))
