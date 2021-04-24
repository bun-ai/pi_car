import time
import traceback


class Vehicle:
    def __init__(self):
        self.on = True
        self.parts = []
        self.mem = {}

    def add(self, part, inputs=None, outputs=None, threaded=False, run_condition=None):
        """

        :param part:
        :param inputs:
        :param outputs:
        :param run_condition:
        :return:
        """
        if inputs is None:
            inputs = []
        assert type(inputs) is list, "inputs is not a list: %r" % inputs
        assert type(outputs) is list, "outputs is not a list: %r" % outputs
        assert type(threaded) is bool, "threaded is not a boolean: %r" % threaded

        p = part
        print('Adding part {}.'.format(p.__class__.__name__))
        entry = {
            'part': p,
            'inputs': inputs,
            'outputs': outputs,
            'run_condition': run_condition,
        }
        self.parts.append(entry)

    def update_parts(self):
        """
        loop over all parts
        """
        for entry in self.parts:

            run = True
            # check run condition, if it exists
            if entry.get('run_condition'):
                run_condition = entry.get('run_condition')
                # run = self.mem.get([run_condition])[0]

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
                # self.profiler.on_part_finished(p)

    def start(self, rate_hz=10, max_loop_count=None):
        try:
            self.on = True

            for entry in self.parts:
                if entry.get('thread'):
                    # start the update thread
                    entry.get('thread').start()

            loop_count = 0

            while self.on:
                start_time = time()
                loop_count += 1

                self.update_parts()

                # stop drive loop if loop_count exceeds max_loop_count
                if max_loop_count and loop_count > max_loop_count:
                    self.on = False

                sleep_time = 1.0 / rate_hz - (time.time() - start_time)
                if sleep_time > 0.0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            traceback.print_exc()
        finally:
            self.stop()

    def stop(self):
        print('Shutting down vehicle and its parts...')
        for entry in self.parts:
            try:
                entry['part'].shutdown()
            except AttributeError:
                # usually from missing shutdown method, which should be optional
                pass
            except Exception as e:
                print(e)
