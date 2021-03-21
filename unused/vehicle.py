import time
import numpy as np

from prettytable import PrettyTable

from unused.memory import Memory


class PartProfiler:
    def __init__(self):
        self.records = {}

    def profile_part(self, p):
        self.records[p] = {"times": []}

    def on_part_start(self, p):
        self.records[p]['times'].append(time.time())

    def on_part_finished(self, p):
        now = time.time()
        prev = self.records[p]['times'][-1]
        delta = now - prev
        thresh = 0.000001
        if delta < thresh or delta > 100000.0:
            delta = thresh
        self.records[p]['times'][-1] = delta

    def report(self):
        print("Part Profile Summary: (times in ms)")
        pt = PrettyTable()
        field_names = ["part", "max", "min", "avg"]
        pctile = [50, 90, 99, 99.9]
        pt.field_names = field_names + [str(p) + '%' for p in pctile]
        for p, val in self.records.items():
            # remove first and last entry because you there could be one-off
            # time spent in initialisations, and the latest diff could be
            # incomplete because of user keyboard interrupt
            arr = val['times'][1:-1]
            if len(arr) == 0:
                continue
            row = [p.__class__.__name__,
                   "%.2f" % (max(arr) * 1000),
                   "%.2f" % (min(arr) * 1000),
                   "%.2f" % (sum(arr) / len(arr) * 1000)]
            row += ["%.2f" % (np.percentile(arr, p) * 1000) for p in pctile]
            pt.add_row(row)
        print(pt)


class Vehicle:
    def __init__(self):
        self.on = True
        self.mem = Memory()
        self.parts = []
        self.profiler = PartProfiler()

    def add(self, part, inputs=[], outputs=[],):
        assert type(inputs) is list, "inputs is not a list: %r" % inputs
        assert type(outputs) is list, "outputs is not a list: %r" % outputs

        entry = {
            'part': part,
            'inputs': inputs,
            'outputs': outputs
        }
        self.parts.append(entry)
        self.profiler.profile_part(part)

    def remove(self, part):
        """
        remove part form list
        """
        self.parts.remove(part)

    def update_parts(self):
        """
        loop over all parts
        """
        for entry in self.parts:
            run = True
            # check run condition, if it exists
            if entry.get('run_condition'):
                run_condition = entry.get('run_condition')
                run = self.mem.get([run_condition])[0]

            if run:
                # get part
                p = entry['part']
                # start timing part run
                self.profiler.on_part_start(p)
                # get inputs from memory
                inputs = self.mem.get(entry['inputs'])
                # run the part
                if entry.get('thread'):
                    outputs = p.run_threaded(*inputs)
                else:
                    outputs = p.run(*inputs)

                # save the output to memory
                if outputs is not None:
                    self.mem.put(entry['outputs'], outputs)
                # finish timing part run
                self.profiler.on_part_finished(p)

    def start(self, rate_hz=10, max_loop_count=None, verbose=False):
        """
        Start vehicle's main drive loop.

        This is the main thread of the vehicle. It starts all the new
        threads for the threaded parts then starts an infinite loop
        that runs each part and updates the memory.

        Parameters
        ----------

        rate_hz : int
            The max frequency that the drive loop should run. The actual
            frequency may be less than this if there are many blocking parts.
        max_loop_count : int
            Maximum number of loops the drive loop should execute. This is
            used for testing that all the parts of the vehicle work.
        verbose: bool
            If debug output should be printed into shell
        """

        # assert (max_loop_count is None) or (max_loop_count > 0), "max_loop_count must be > 0: %r" % max_loop_count

        print('Starting vehicle at {} Hz'.format(rate_hz))
        self.on = True

        loop_count = 0
        while self.on:
            start_time = time.time()
            loop_count += 1

            self.update_parts()

            if max_loop_count and (loop_count > max_loop_count):
                self.on = False

            sleep_time = 1.0 / rate_hz - (time.time() - start_time)
            if sleep_time > 0.0:
                time.sleep(sleep_time)

    def stop(self):
        # print('Shutting down vehicle and its parts...')
        pass
