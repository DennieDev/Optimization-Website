import logging
import analyze

# TO-DO:
# Replace the shady authors/plugins to a YAML file for scalability


def get_shady_plugins(request):
    try:
        plugins = request["timingsMaster"]["plugins"] if "plugins" in request["timingsMaster"] else None
        for plugin in plugins:
            authors = request["timingsMaster"]["plugins"][plugin]["authors"]
            if authors is not None and "songoda" in request["timingsMaster"]["plugins"][plugin]["authors"].casefold():
                if plugin == "EpicHeads":
                    analyze.return_list.append({
                        'title': 'EpicHeads',
                        'body': 'This plugin was made by Songoda. Songoda is sketchy. You should find an alternative '
                                'such as "HeadsPlus" or "HeadDatabase"'
                    })

                elif plugin == "UltimateStacker":
                    analyze.return_list.append({
                        'title': 'UltimateStacker',
                        'body': 'Stacking plugins actually causes more lag. Remove UltimateStacker. '
                    })
                else:
                    analyze.return_list.append({
                        'title': f'{plugin}',
                        'body': 'This plugin was made by Songoda. Songoda is sketchy. You should find an alternative.'
                    })

    except KeyError as key:
        logging.info("Missing: " + str(key))

