import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support,cpu_count

#
# Function run by worker processes
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b


#
#
#

def test():
    NUMBER_OF_PROCESSES = 16
    print('Using Core:',NUMBER_OF_PROCESSES)
    TASKS1 = [(mul, (i, 7)) for i in range(200)]

    print(TASKS1)
    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        print('put_task:',task)
        task_queue.put(task)

    # Start worker processes
    t1 = time.time()
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    
    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        done_queue.get()
        #print('\t', done_queue.get())
        #pass
    print('time',time.time()-t1)

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()