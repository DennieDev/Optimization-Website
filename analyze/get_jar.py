import yaml
import re
import logging
import analyze

TIMINGS_CHECK = None
YAML_ERROR = None
with open("timings_check.yml", 'r', encoding="utf8") as stream:
    try:
        TIMINGS_CHECK = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.info(exc)
        YAML_ERROR = exc

VERSION_REGEX = re.compile(r"\d+\.\d+\.\d+")


def get_jar(request):
    try:
        version = request["timingsMaster"]["version"] if "version" in request["timingsMaster"] else None

        if "jars" in TIMINGS_CHECK:
            for jar in TIMINGS_CHECK["jars"]:
                if jar["name"] in version:
                    analyze.return_list.append({
                        'title': jar["name"],
                        'body': jar["value"]
                    })
                    break

    except KeyError as key:
        logging.info("Missing: " + str(key))
