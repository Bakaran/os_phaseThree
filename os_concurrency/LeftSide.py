from multiprocessing import  Process, Queue, Value,Array
from time import sleep
from Car import Car



def producer(queue, id, s1):
    print('Producer: Running', flush=True)
    while True:
        s1.Wait(1)
        value = Car(id.value)
        id.value += 1
        sleep(0.5)
        queue.put(value)
        s1.Signal()
def consumer(queue, street, s2):
    print('Consumer: Running', flush=True)
    while True:
        s2.Wait(1)
        item = queue.get()
        street.value = item.id
        print('car id: ', item.id, 'sleep: ', item.time)
        temp = street.value
        sleep(item.time)
        if temp != street.value:
            print('Process conflict!')
        s2.Signal()
        street.value = 0

