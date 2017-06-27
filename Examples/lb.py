#!/usr/bin/env python
import sys
from mpi4py import MPI

VERBOSE = False

class Task(object):
    tag = 100
    def __init__(self, id, argtup):
        self.id = id
        self.argtup = argtup

class Result(object):
    tag = 101
    def __init__(self, id, value):
        self.id = id
        self.value = value

def masterloop(comm, *iterables):
    size = comm.Get_size()
    rank = comm.Get_rank()
    next_task = 0
    num_tasks = 1000000000  # don't know how many yet
    iargs = zip(*iterables)

    # Send initial task to each worker
    try:
        for worker in range(size):
            if worker != rank:
                task = Task(next_task, next(iargs))
                if VERBOSE:
                    print('Sending task %d to worker %d' % (next_task, worker))
                comm.send(task, dest=worker, tag=Task.tag)
                next_task += 1
    except StopIteration:
        num_tasks = next_task  # now we know
        if VERBOSE:
            print('Number of tasks:', num_tasks)

    # Send tasks to and receive results from the workers
    results = {}
    status = MPI.Status()
    while len(results) < num_tasks:
        r = comm.recv(source=MPI.ANY_SOURCE, tag=Result.tag, status=status)
        results[r.id] = r.value
        worker = status.Get_source()
        if VERBOSE:
            print('Got result %d from worker %d' % (r.id, worker))

        # Check if there are more tasks to execute
        if next_task < num_tasks:
            # Send the next task to the worker that just completed a task
            try:
                task = Task(next_task, next(iargs))
                if VERBOSE:
                    print('Sending task %d to worker %d' % (next_task, worker))
                comm.send(task, dest=worker, tag=Task.tag)
                next_task += 1
            except StopIteration:
                num_tasks = next_task  # now we know
                if VERBOSE:
                    print('Number of tasks:', num_tasks)

    # Send a poison pill to each worker
    for worker in range(size):
        if worker != rank:
            if VERBOSE:
                print('Sending poison pill to worker %d' % worker)
            comm.send(None, dest=worker, tag=Task.tag)

    # Convert results dictionary to a list and return it
    return [results[i] for i in range(num_tasks)]

def workerloop(comm, taskfun, *args, **kargs):
    status = MPI.Status()

    while True:
        # Wait for a task request
        task = comm.recv(source=MPI.ANY_SOURCE, tag=Task.tag, status=status)
        master = status.Get_source()

        # Check for a poison pill
        if task is None:
            break

        # Execute the task
        value = taskfun(*(task.argtup + args), **kargs)

        # Send the result along with the task ID back to the requester
        result = Result(task.id, value)
        comm.send(result, dest=master, tag=Result.tag)

if __name__ == '__main__':
    import math, random
    from itertools import count

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size == 1:
        sys.stderr.write('error: you must start at least two processes\n')
    else:
        # A simple example
        if rank == 0:
            results = masterloop(comm, range(10))
            print(results)
        else:
            workerloop(comm, math.sqrt)

        # A slightly less simple example
        if rank == 0:
            def rand(n=10, lower=0, upper=0):
                while n > 0:
                    yield random.randint(lower, upper)
                    n -= 1

            results = masterloop(comm, count(), rand(lower=0, upper=0))
            print(results)
        else:
            def add(*x):
                return sum(x)

            workerloop(comm, add, 30, 70)
