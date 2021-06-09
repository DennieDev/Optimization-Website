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


def get_version(request):
    try:
        version = request["timingsMaster"]["version"] if "version" in request["timingsMaster"] else None
        if "version" in TIMINGS_CHECK and version:
            version_result = VERSION_REGEX.search(version)
            version_result = version_result.group() if version_result else None
            if version_result:
                if compare_versions(version_result, TIMINGS_CHECK["version"]) == -1:
                    version = version.replace("git-", "").replace("MC: ", "")
                    analyze.return_list.append({
                        'title': 'Outdated',
                        'body': f'You are using: "{version}". Update to: "{TIMINGS_CHECK["version"]}".'
                    })
            else:
                analyze.return_list.append({
                    'title': 'Value Error',
                    'body': f'Could not locate version from `{version}`'
                })

    except KeyError as key:
        logging.info("Missing: " + str(key))


# Returns -1 if version A is older than version B
# Returns 0 if version A and B are equivalent
# Returns 1 if version A is newer than version B
def compare_versions(version_a, version_b):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    return (normalize(version_a) > normalize(version_b)) - (normalize(version_a) < normalize(version_b))
