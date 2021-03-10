import time

from car.memory import Memory


class Vehicle:
    def __init__(self):
        self.on = True
        self.mem = Memory()
        self.parts = []

    def add(self, part, inputs=[], outputs=[],):
        assert type(inputs) is list, "inputs is not a list: %r" % inputs
        assert type(outputs) is list, "outputs is not a list: %r" % outputs

        entry = {
            'part': part,
            'inputs': inputs,
            'outputs': outputs
        }
        self.parts.append(entry)

    def remove(self, part):
        """
        remove part form list
        """
        self.parts.remove(part)

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

            if max_loop_count and (loop_count > max_loop_count):
                self.on = False

            sleep_time = 1.0 / rate_hz - (time.time() - start_time)
            if sleep_time > 0.0:
                time.sleep(sleep_time)

    def stop(self):
        # print('Shutting down vehicle and its parts...')
        pass
