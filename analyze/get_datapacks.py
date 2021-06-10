import logging
import analyze


def get_datapacks(request_raw):
    try:
        handlers = request_raw["idmap"]["handlers"]
        for handler in handlers:
            handler_name = request_raw["idmap"]["handlers"][handler][1]
            if handler_name.startswith("Command Function - ") and handler_name.endswith(":tick"):
                handler_name = handler_name.split("Command Function - ")[1].split(":tick")[0]
                analyze.return_list.append({
                    'title': f'{handler_name}',
                    'body': 'This datapack uses command functions which are laggy.'
                })
    except KeyError as key:
        logging.info("Missing: " + str(key))

