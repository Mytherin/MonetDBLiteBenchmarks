

import os
import subprocess
import threading

INITFILE_PARAM = 'INITFILE'
TIMEFILE_PARAM = 'TIMEFILE'
FINALFILE_PARAM = 'FINALFILE'
NRUNS_PARAM = 'NRUNS'

RESULT_FILE = 'tmp_results.csv'

R = 1
Julia = 2
Python = 3

FNULL = open(os.devnull, 'w')

class Command(object):
    def __init__(self, cmd, silent):
        self.cmd = cmd
        self.process = None
        self.silent = silent

    def run(self, timeout):
        def target():
            if self.silent:
                self.process = subprocess.Popen(self.cmd, stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            else:
                self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

def init(SILENT=True):
    pipe = ">/dev/null 2>/dev/null" if SILENT else ""
    print("[SCRIPT] Initializing R packages")
    os.system('R -f scripts/packages.R ${PIPE}'.replace('${PIPE}', pipe))
    print("[SCRIPT] Initializing Julia packages")
    os.system('julia scripts/packages.jl ${PIPE}'.replace('${PIPE}', pipe))

def run_script(lang, init_script, bench_scripts, final_scripts, nruns, TIMEOUT=60, SILENT=True):
    if len(final_scripts) != 0 and len(final_scripts) != len(bench_scripts):
        raise Exception("Timing files and final files should have the same length!")

    os.environ[INITFILE_PARAM] = ','.join(init_script)
    os.environ[NRUNS_PARAM] = str(nruns)
    timings = {}
    for entry in bench_scripts:
        timings[entry] = []

    for i in range(len(bench_scripts)):
        benchmark_script = bench_scripts[i]
        os.environ[TIMEFILE_PARAM] = benchmark_script
        os.environ[FINALFILE_PARAM] = '' if len(final_scripts) == 0 else final_scripts[i]
        print("[SCRIPT] Running program %s" % (benchmark_script))
        if lang == Julia:
            params = ['julia', 'run.jl']
        elif lang == R:
            params = ['R', '-f', 'run.R']
        elif lang == Python:
            params = ['python', 'run.py']
        else:
            raise Exception("Unrecognized language \"%s\"" % (str(lang)))

        command = Command(params, SILENT)
        command.run(timeout = TIMEOUT * (nruns + 1))


        del os.environ[TIMEFILE_PARAM]
        del os.environ[FINALFILE_PARAM]
        indices = []
        header = True
        if os.path.exists(RESULT_FILE):
            try:
                with open(RESULT_FILE, 'r') as f:
                    for line in f:
                        line = line.rstrip('\n')
                        entries = line.split(',')
                        if header:
                            indices = entries
                            header = False
                        else:
                            index = 0
                            for entry in entries:
                                if indices[index] != 'id':
                                    timings[indices[index]].append(float(entry))
                                index += 1
                for entry in indices:
                    if entry != 'id':
                        if len(timings[entry]) != nruns:
                            raise Exception('Did not complete nruns!')
                os.remove(RESULT_FILE)
                print('[SCRIPT] Run successful')
                continue
            except:
                os.remove(RESULT_FILE)
        print('[SCRIPT] TIMEOUT')
        timings[benchmark_script] = [-1] * nruns

    del os.environ[INITFILE_PARAM]
    del os.environ[NRUNS_PARAM]
    
    for entry in bench_scripts:
        if len(timings[entry]) != nruns:
            raise Exception("Something went wrong in the script.")
    return timings
