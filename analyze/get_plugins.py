import logging
import analyze
import yaml
import re

TIMINGS_CHECK = None
YAML_ERROR = None
with open("timings_check.yml", 'r', encoding="utf8") as stream:
    try:
        TIMINGS_CHECK = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.info(exc)
        YAML_ERROR = exc

VERSION_REGEX = re.compile(r"\d+\.\d+\.\d+")


def get_plugins(request):
    plugins = request["timingsMaster"]["plugins"] if "plugins" in request["timingsMaster"] else None
    server_properties = request["timingsMaster"]["config"]["server.properties"] if "server.properties" in \
                                                                                   request["timingsMaster"][
                                                                                       "config"] else None
    bukkit = request["timingsMaster"]["config"]["bukkit"] if "bukkit" in request["timingsMaster"][
        "config"] else None
    spigot = request["timingsMaster"]["config"]["spigot"] if "spigot" in request["timingsMaster"][
        "config"] else None
    paper = request["timingsMaster"]["config"]["paper"] if "paper" in request["timingsMaster"]["config"] else None
    tuinity = request["timingsMaster"]["config"]["tuinity"] if "tuinity" in request["timingsMaster"][
        "config"] else None
    purpur = request["timingsMaster"]["config"]["purpur"] if "purpur" in request["timingsMaster"][
        "config"] else None
    if not YAML_ERROR:
        if "plugins" in TIMINGS_CHECK:
            for server_name in TIMINGS_CHECK["plugins"]:
                if server_name in request["timingsMaster"]["config"]:
                    for plugin in plugins:
                        for plugin_name in TIMINGS_CHECK["plugins"][server_name]:
                            if plugin == plugin_name:
                                stored_plugin = TIMINGS_CHECK["plugins"][server_name][plugin_name]
                                if isinstance(stored_plugin, dict):
                                    stored_plugin["name"] = plugin_name
                                    analyze.return_list.append({
                                        'title': stored_plugin["name"],
                                        'body': stored_plugin['value']
                                    })
                                else:
                                    eval_field(stored_plugin, plugin_name, plugins,
                                               server_properties, bukkit, spigot, paper, tuinity, purpur)
        if "config" in TIMINGS_CHECK:
            for config_name in TIMINGS_CHECK["config"]:
                config = TIMINGS_CHECK["config"][config_name]
                for option_name in config:
                    option = config[option_name]
                    eval_field(option, option_name, plugins, server_properties, bukkit,
                               spigot, paper, tuinity, purpur)
    else:
        analyze.return_list.append({
            'title': 'Error loading YAML file',
            'body': f'{YAML_ERROR}'
        })


def eval_field(option, option_name, plugins, server_properties, bukkit, spigot, paper, tuinity, purpur):
    dict_of_vars = {"plugins": plugins, "server_properties": server_properties, "bukkit": bukkit, "spigot": spigot,
                    "paper": paper, "tuinity": tuinity, "purpur": purpur}
    try:
        for option_data in option:
            add_to_field = True
            for expression in option_data["expressions"]:
                for config_name in dict_of_vars:
                    if config_name in expression and not dict_of_vars[config_name]:
                        add_to_field = False
                        break
                if not add_to_field:
                    break
                try:
                    if not eval(expression):
                        add_to_field = False
                        break
                except ValueError as value_error:
                    add_to_field = False
                    logging.info(value_error)
                    analyze.return_list.append({
                        'title': f'Value Error, `{value_error}`\n',
                        'body': f'expression:\n {expression} \noption:\n {option_name} '
                    })
                except TypeError as type_error:
                    add_to_field = False
                    logging.info(type_error)
                    analyze.return_list.append({
                        'title': f'Type Error, {type_error}`\n',
                        'body': f'expression:\n {expression} \noption:\n {option_name} '
                    })
            for config_name in dict_of_vars:
                if config_name in option_data["value"] and not dict_of_vars[config_name]:
                    add_to_field = False
                    break
            if add_to_field:
                """ f strings don't like newlines so we replace the newlines with placeholder text before we eval """
                option_data["value"] = eval('f"""' + option_data["value"].replace("\n", "\\|n\\") + '"""').replace(
                    "\\|n\\", "\n")
                analyze.return_list.append({
                    'title': f'Name: {option_name}',
                    'body': f'{option_data["value"]}'
                })
                break

    except KeyError as key:
        logging.info("Missing: " + str(key))
