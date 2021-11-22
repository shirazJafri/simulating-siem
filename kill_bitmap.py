def cease_bitmap():
    import os
    import subprocess

    lines = subprocess.check_output(['ps', '-A']).splitlines()

    for line in lines:
        if 'bitmap' in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)

def cease_browser_activity():
    import os
    import subprocess

    lines = subprocess.check_output(['ps', '-A']).splitlines()

    foundActivity = False

    for line in lines:
        if 'GeckoMain' in str(line):
            foundActivity = True
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)

    return foundActivity