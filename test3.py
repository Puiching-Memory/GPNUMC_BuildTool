from concurrent import futures
import time
import random

def returnNumber(number: int) -> int:
    #print("start threading {}".format(number))
    time.sleep(random.randint(0, 2))  # 随机睡眠
    #print("end threading {}".format(number))
    return number  # 返回参数本身

if __name__ == '__main__':
    with futures.ProcessPoolExecutor(16) as executor:
        # with语句会调用executor.shutdown(wait=True)，在所有线程都执行完毕前阻塞当前线程
        res = executor.map(returnNumber,range(0, 200))
        # 返回一个生成器，遍历的结果为0,1,2,3。无论执行结果先后顺序如何，看输入的iterator顺序
        # 因为线程池为3，所以0~2进池，其中某个执行完后，3进池
        print(res)
    print("----print result----")
    for r in res:
        print(r)

    #print(res)