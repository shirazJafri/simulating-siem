def getProcessCount():
    import subprocess

    procs = subprocess.check_output(['ps', 'uaxw']).splitlines()
    bitmap_procs = [proc for proc in procs if 'bitmap' in str(proc)]
    count = len(bitmap_procs)

    print(count)

    return count