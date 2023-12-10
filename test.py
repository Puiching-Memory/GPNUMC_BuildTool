import multiprocessing


def mp_center(fun,*kargs):
    '''
    多进程管理器
    ---
    '''
    #print(fun,kargs)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.apply_async(fun, args=kargs)
    pool.close()
    pool.join()





def coun(c):
    for i in c:
        print(i)
        ra.remove(i)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    ra = multiprocessing.Manager().list()
    ra.extend([i for i in range(100)])
    #print(ra)
    mp_center(coun,[2,2,3,4])
