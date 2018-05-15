

import os
import subprocess
import threading
import time

INITFILE_PARAM = 'INITFILE'
TIMEFILE_PARAM = 'TIMEFILE'
FINALFILE_PARAM = 'FINALFILE'
NRUNS_PARAM = 'NRUNS'

RESULT_FILE = 'tmp_results.csv'
START_EXPERIMENTS_FILE = 'start_experiments.csv'

R = 1
Julia = 2
Python = 3

FNULL = open(os.devnull, 'w')

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
    os.environ[TIMEOUT_PARAM] = str(TIMEOUT)

    timings = {}
    for entry in bench_scripts:
        timings[entry] = []

    for i in range(len(bench_scripts)):
        benchmark_script = bench_scripts[i]
        os.environ[TIMEFILE_PARAM] = benchmark_script
        os.environ[FINALFILE_PARAM] = '' if len(final_scripts) == 0 else final_scripts[i]
        print("[SCRIPT] Running program %s" % (benchmark_script))
        if lang == Julia:
            process_path = ['julia', 'run.jl']
        elif lang == R:
            process_path = ['R', '-f', 'run.R']
        elif lang == Python:
            process_path = ['python', 'run.py']
        else:
            raise Exception("Unrecognized language \"%s\"" % (str(lang)))

        if os.path.exists(START_EXPERIMENTS_FILE):
            os.remove(START_EXPERIMENTS_FILE)

        if SILENT:
            proc = subprocess.Popen(process_path, stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            proc = subprocess.Popen(process_path)

        while True:
            if not os.path.exists(START_EXPERIMENTS_FILE):
                time.sleep(1)

        # experiments started
        def wait_for_process():
            proc.communicate()

        thread = threading.Thread(Target=wait_for_process)
        thread.start()
        thread.join(TIMEOUT * nruns)

        if thread.is_alive():
            # timeout in subprocess
            proc.terminate()
            thread.join()

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
