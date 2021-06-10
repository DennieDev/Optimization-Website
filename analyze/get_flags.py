import logging
import analyze


# TO DO:
# Update Flags with .YAML file for scalability

def get_flags(request):
    try:
        flags = request["timingsMaster"]["system"]["flags"]
        if "-XX:+UseZGC" in flags:
            jvm_version = request["timingsMaster"]["system"]["jvmversion"]
            java_version = jvm_version.split(".")[0]
            if int(java_version) < 15:
                analyze.return_list.append({
                    'title': f'Java " + {java_version}',
                    'body': 'ZGC flags should only be used on Java 16.'
                })

            if "-Xmx" in flags:
                max_mem = 0
                flaglist = flags.split(" ")
                for flag in flaglist:
                    if flag.startswith("-Xmx"):
                        max_mem = flag.split("-Xmx")[1]
                        max_mem = max_mem.replace("G", "000")
                        max_mem = max_mem.replace("M", "")
                        max_mem = max_mem.replace("g", "000")
                        max_mem = max_mem.replace("m", "")
                        if int(max_mem) < 10000:
                            analyze.return_list.append({
                                'title': 'Low Memory',
                                'body': 'ZGC flags are only good with a lot of memory.'
                            })

        elif "-Daikars.new.flags=true" in flags:
            if "-XX:+PerfDisableSharedMem" not in flags:
                analyze.return_list.append({
                    'title': 'Outdated Flags',
                    'body': 'Add `-XX:+PerfDisableSharedMem` to flags.'
                })
            if "XX:G1MixedGCCountTarget=4" not in flags:
                analyze.return_list.append({
                    'title': 'Outdated Flags',
                    'body': 'Add `-XX:G1MixedGCCountTarget=4` to flags.'
                })
            jvm_version = request["timingsMaster"]["system"]["jvmversion"]
            if "-XX:+UseG1GC" not in flags and jvm_version.startswith("1.8."):
                analyze.return_list.append({
                    'title': 'Aikar\'s Flags',
                    'body': 'You must use G1GC when using Aikar\'s flags.'
                })
            if "-Xmx" in flags:
                max_mem = 0
                flaglist = flags.split(" ")
                for flag in flaglist:
                    if flag.startswith("-Xmx"):
                        max_mem = flag.split("-Xmx")[1]
                        max_mem = max_mem.replace("G", "000")
                        max_mem = max_mem.replace("M", "")
                        max_mem = max_mem.replace("g", "000")
                        max_mem = max_mem.replace("m", "")
                if int(max_mem) < 5400:
                    analyze.return_list.append({
                        'title': 'Low Memory',
                        'body': 'Allocate at least 6-10GB of ram to your server if you can afford it.'
                    })

                index = 0
                max_online_players = 0
                while index < len(request["timingsMaster"]["data"]):
                    timed_ticks = request["timingsMaster"]["data"][index]["minuteReports"][0]["ticks"][
                        "timedTicks"]
                    player_ticks = request["timingsMaster"]["data"][index]["minuteReports"][0]["ticks"][
                        "playerTicks"]
                    players = (player_ticks / timed_ticks)
                    max_online_players = max(players, max_online_players)
                    index = index + 1
                if 1000 * max_online_players / int(max_mem) > 6 and int(max_mem) < 10000:
                    analyze.return_list.append({
                        'title': 'Low Memory',
                        'body': 'You should be using more RAM with this many players.'
                    })

                if "-Xms" in flags:
                    min_mem = 0
                    flaglist = flags.split(" ")
                    for flag in flaglist:
                        if flag.startswith("-Xms"):
                            min_mem = flag.split("-Xms")[1]
                            min_mem = min_mem.replace("G", "000")
                            min_mem = min_mem.replace("M", "")
                            min_mem = min_mem.replace("g", "000")
                            min_mem = min_mem.replace("m", "")
                    if min_mem != max_mem:
                        analyze.return_list.append({
                            'title': 'Aikar\'s Flags',
                            'body': 'Your Xmx and Xms values should be equal when using Aikar\'s flags.'
                        })
        elif "-Dusing.aikars.flags=mcflags.emc.gs" in flags:
            analyze.return_list.append({
                'title': 'Outdated Flags',
                'body': 'Update your Aikar\'s Flags'
            })
        else:
            analyze.return_list.append({
                'title': 'Aikar\'s Flags',
                'body': 'Use Aikar\'s Flags'
            })
    except KeyError as key:
        logging.info("Missing: " + str(key))
