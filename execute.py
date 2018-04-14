import subprocess

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# cmd_in and cmd_out are tuples
#popen = subprocess.Popen(cmd_in, stdout=subprocess.PIPE)
#output = subprocess.check_output(cmd_out, stdin=popen.stdout)
#popen.wait()

def main():
    for path in execute(['ls']):
        print(path, end="")

