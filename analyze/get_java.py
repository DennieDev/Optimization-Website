import logging
import analyze


def get_java(request):
    try:
        jvm_version = request["timingsMaster"]["system"]["jvmversion"]
        if jvm_version.startswith("1.8.") or jvm_version.startswith("9.") or jvm_version.startswith("10."):
            analyze.return_list.append({
                'title': 'Java Version',
                'body': f'You are using Java {jvm_version}. Update to Java 16'
            })

    except KeyError as key:
        logging.info("Missing: " + str(key))
