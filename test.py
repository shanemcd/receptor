from receptorctl import ReceptorControl
import queue
import threading
import time

rc1 = ReceptorControl("/var/run/receptor/receptor.sock")
rc2 = ReceptorControl("/var/run/receptor/receptor.sock")
rc3 = ReceptorControl("/var/run/receptor/receptor.sock")

class StatusWork(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def run(self):
        c = 0
        while not stop_threads:
            # try:
            c += 1
            rc3.simple_command("work list")
            # except:
            #     continue
        print(f"status calls {c}")

class ReleaseWork(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        self.q = q
        super().__init__(*args, **kwargs)
    def run(self):
        while True:
            try:
                unitid = self.q.get(timeout=1)
                # time.sleep(.005)
                res = rc2.simple_command(f"work release {unitid}")
                print(res)
                self.q.task_done()
            except queue.Empty:
                return

q = queue.Queue()
stop_threads = False

# time.sleep(2)
ReleaseWork(q).start()
#StatusWork().start()

for _ in range(100):
    data = rc1.submit_work("echosleepshort", "".encode())
    print(data)
    q.put_nowait(data['unitid'])

q.join()
stop_threads = True
