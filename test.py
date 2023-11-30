
#from tqdm import tqdm
import multiprocessing as mp


class OP():
    def __init__(self):
        # 直接调用 Manager 提供的 list() 和 dict()
        self.manager = mp.Manager
        self.mp_lst = self.manager().list()
        self.mp_dict = self.manager().dict()
        self.length = 64

    def proc_func(self, i, j):
        self.mp_lst.append(i)
        self.mp_dict[i] = j

    def flow(self):
        pool = mp.Pool(16)
        for i in range(self.length):
            pool.apply_async(self.proc_func, args=(i, i*2))
        pool.close()
        pool.join()


if __name__ == '__main__':


    op = OP()
    op.flow()
    print(op.mp_lst)
    print(op.mp_dict)

