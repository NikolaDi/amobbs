# coding=utf-8

import subprocess
import Queue
import threading

rest = []

shell_str = 'ping -c 1 -t 2 192.168.1.{}'
ping_queue = Queue.Queue(0)

for i in range(1, 255):
    ping_queue.put(shell_str.format(i))


def thread_ping():
    while True:
        shell = ping_queue.get()
        if shell:
            return_code = subprocess.call(shell, shell=True)
            if return_code == 0:
                #print '192.168.1.{}'.format(i)
                rest.append('192.168.1.{}'.format(i))
        else:
            break

thread_pool = []
for i in range(0, 8):
    t = threading.Thread(target=thread_ping)
    thread_pool.append(t)
    # t.setDaemon(True)
    t.start()

for t in thread_pool:
    t.join()

for i in rest:
    print i
