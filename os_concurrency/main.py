from multiprocessing import Process, Queue, Value,Array
import  RightSide, LeftSide
class Semaphore:
    def __init__(self):
        self.sem = Value('i',1)
        self.flag_0 = Value('i',0)
        self.flag_1 = Value('i',0)
        self.sem_q = Queue(2)
    def Wait(self,process_id):
        self.sem.value -= 1
        if self.sem.value < 0:
            if process_id == 0:
                self.flag_0.value = 0
            elif process_id == 1:
                self.flag_1.value = 0
            self.sem_q.put(process_id)
            while True:
                if process_id == 0:
                    if self.flag_0.value == 1:
                        break
                elif process_id == 1:
                    if self.flag_1.value == 1:
                        break
    def Signal(self):
        self.sem.value += 1
        if self.sem.value <= 0:
            process_id = self.sem_q.get()
            if process_id == 0:
                self.flag_0.value = 1
            elif process_id == 1:
                self.flag_1.value = 1

def main():

    street = Value('d',0)
    id = Value('d',1)

    car_list1 = Queue(maxsize=10)
    car_list2 = Queue(maxsize=10)
    s1 = Semaphore()
    s2 = Semaphore()
    prod1 = Process(target=RightSide.producer, args=(car_list1, id, s1))
    cons1 = Process(target=RightSide.consumer, args=(car_list1, street, s2))
    prod1.start()
    cons1.start()


    prod2 = Process(target=LeftSide.producer, args=(car_list2, id, s1))
    cons2 = Process(target=LeftSide.consumer, args=(car_list2, street, s2))
    prod2.start()
    cons2.start()




if __name__ == '__main__':
    main()
