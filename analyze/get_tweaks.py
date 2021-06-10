import logging
import analyze


def get_tweaks(request, request_raw):
    try:
        plugins = request["timingsMaster"]["plugins"] if "plugins" in request["timingsMaster"] else None
        spigot = request["timingsMaster"]["config"]["spigot"] if "spigot" in request["timingsMaster"][
            "config"] else None
        using_tweaks = "ViewDistanceTweaks" in plugins
        if not using_tweaks:
            worlds = request_raw["worlds"]
            for world in worlds:
                tvd = int(request_raw["worlds"][world]["ticking-distance"])
                ntvd = int(request_raw["worlds"][world]["notick-viewdistance"])
                if ntvd <= tvd and tvd >= 5:
                    if spigot["world-settings"]["default"]["view-distance"] == "default":
                        analyze.return_list.append({
                            'title': 'no-tick-view-distance',
                            'body': f'Set in paper.yml. Recommended: {tvd}. '
                                    f'And reduce view-distance from default ({tvd}) in spigot.yml. Recommended: 4. " '
                        })
                    else:
                        analyze.return_list.append({
                            'title': 'no-tick-view-distance',
                            'body': f'Set in paper.yml. Recommended: {tvd}. '
                                    f'And reduce view-distance from {tvd} in spigot.yml. Recommended: 4. " '
                        })
                    break
    except KeyError as key:
        logging.info("Missing: " + str(key))