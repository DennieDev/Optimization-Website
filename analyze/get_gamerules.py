import logging
import analyze


def get_gamerules(request_raw):
    try:
        worlds = request_raw["worlds"]
        high_mec = False
        for world in worlds:
            max_entity_cramming = int(request_raw["worlds"][world]["gamerules"]["maxEntityCramming"])
            if max_entity_cramming >= 24:
                high_mec = True
        if high_mec:
            analyze.return_list.append({
                'title': 'maxEntityCramming',
                'body': 'Decrease this by running the /gamerule command in each world. Recommended: 8.'
            })

    except KeyError as key:
        logging.info("Missing: " + str(key))
