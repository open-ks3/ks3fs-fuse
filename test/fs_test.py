#! coding:utf8
import os
import shutil
import random
import threading
import time


BUFFER_TWO_HUNDRED_AND_FIFTY_SIX_BYTE = '*' * 256
BUFFER_FIVE_HUNDRED_AND_TWELVE_BYTE = '*' * 512
BUFFER_ONE_KB = '*' * 1024
BUFFER_TWO_KB = '*' * 1024 * 2
BUFFER_FOUR_KB = '*' * 1024 * 4
BUFFER_ONE_MB = '*' * 1024 * 1024
BUFFER_FIVE_MB = '*' * 1024 * 1024 * 5
BUFFER_TEN_MB = '*' * 1024 * 1024 * 10
#BUFFER_ONE_GB = '*' * 1024 * 1024 * 1024
#BUFFER_FIVE_GB = '*' * 1024 * 1024 * 1024 * 5
#BUFFER_TEN_GB = '*' * 1024 * 1024 * 1024 * 10

BUFFER_ONE_GB = 1024 * 1024 * 1024

#mount_dir = '/data/rds/mnt/ks3'
#mount_dir = '/datapool/ks3cmp'
mount_dir = '/data/rds/ks3fs'

"""模拟测试"""


# 模拟binlog流形式追加写 每次追加大小随机256byte, 512byte, 1KB, 1M, 5M, 10M
def test_binlog_a(i):
    try:
        start = time.clock()
        size = 0
        f = open(mount_dir + '/'+str(i), 'a')
        while size < BUFFER_ONE_GB:
            buffer = random.choice([BUFFER_TWO_HUNDRED_AND_FIFTY_SIX_BYTE,
                                    BUFFER_FIVE_HUNDRED_AND_TWELVE_BYTE,
                                    BUFFER_ONE_KB,
                                    BUFFER_ONE_MB,
                                    BUFFER_FIVE_MB,
                                    BUFFER_TEN_MB])
            size += len(buffer)
            f.write(buffer)
            f.flush()
        f.close()
        end = time.clock()
        print '*file %s size %s cost %f s' % (str(i), str(size), end - start)
    except Exception as e:
        print 'file %s write file' % str(i), e
        return False
    return True

def run():
    for file in os.listdir(mount_dir):
        if os.path.isfile(mount_dir+'/'+file):
            os.remove(mount_dir+'/'+file)

    # run 100 jobs in parallel
    jobs = [threading.Thread(target=test_binlog_a, args=(i,)) for i in range(100)]

    start = time.clock()

    # print the results (if available)
    for t in jobs:
        t.setDaemon(True)
        t.start()

    for t in jobs:
        t.join()

    end = time.clock()

    print '#all file upload cost %f s' % (end - start)



if '__main__' == __name__:
    run()

