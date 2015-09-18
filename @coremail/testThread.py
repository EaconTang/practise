import threading

class SummingThread(threading.Thread):
    def __init__(self, low, high):
        super(SummingThread, self).__init__()
        self.low = low
        self.high = high
        self.total = 0

    def run(self):
        for i in range(self.low, self.high):
            self.total += i

class TestThread(threading.Thread):
    def __init__(self,s):
        super(TestThread,self).__init__()
        self.s = s
    def run(self):
        for i in range(10):
            print self.s

thread1 = SummingThread(0, 500000)
thread2 = SummingThread(500000, 1000000)
thread1.start()
# This actually causes the thread to run
thread2.start()
thread1.join()
# This waits until the thread has completed
thread2.join()
# At this point, both threads have completed
print thread1.total
print thread2.total
result = thread1.total + thread2.total
print(result)

thread3 = TestThread('a')
thread4 = TestThread('b')
thread3.start()
thread4.start()
thread3.join()
thread4.join()

print thread3.

