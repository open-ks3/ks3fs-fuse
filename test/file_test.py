#! coding:utf8

import os
import shutil
from nose import with_setup

# TODO mount路径
mount_dir = '/data/rds/ks3fs/'


def setup():
    # 改变工作目录
    os.chdir(mount_dir)
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown():
    pass


# TODO ##############################################################
# TODO                   **目录操作**                                #
# TODO ##############################################################


# TODO 创建目录
def setup_mkdir():
    print '*************** test makdir ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def teardown_mkdir():
    os.rmdir('hello')


@with_setup(setup_mkdir, teardown_mkdir)
def test_mkdir():
    os.mkdir('hello')
    assert True == os.path.exists('hello'), 'mkdir hello not exists'


# TODO 返回指定目录下的所有文件和目录名
def setup_listdir():
    print '*************** test listdir ***************'
    os.mkdir('hello')
    for f in [os.path.join('hello', str(i)) for i in range(0, 10)]:
        os.mknod(f)


def teardown_listdir():
    shutil.rmtree('hello')


@with_setup(setup_listdir, teardown_listdir)
def test_listdir():
    files = os.listdir('hello')
    for i in range(0, 10):
        assert str(i) in files, 'file %d not in listdir< %s >files' % (i, files)


# TODO 函数用来删除一个文件
def setup_remove():
    print '*************** test remove ***************'
    open('hello', 'w')


def teardown_remove():
    pass


@with_setup(setup_remove, teardown_remove)
def test_remove():
    os.remove('hello')
    assert 'hello' not in os.listdir(mount_dir), 'file hello until in path'


# TODO 删除多个目录
def setup_removedirs():
    print '*************** test removedirs ***************'
    os.mkdir('hello')
    path_c = os.path.join('hello', '1')
    os.mkdir(path_c)


def teardown_removedirs():
    pass


@with_setup(setup_removedirs, teardown_removedirs)
def test_removedirs():
    try:
        os.removedirs('hello/1')
    except OSError:
        pass


# TODO 检验给出的路径是否是一个文件
def setup_isfile():
    print '*************** test isfile ***************'
    open('hello', 'w')


def teardown_isfile():
    os.remove('hello')


@with_setup(setup_isfile, teardown_isfile)
def test_isfile():
    assert True == os.path.isfile('hello'), 'hello is not a file'


# TODO 检验给出的路径是否是一个目录
def setup_isdir():
    print '*************** test isdir ***************'
    os.mkdir('hello')


def teardown_isdir():
    os.rmdir('hello')


@with_setup(setup_isdir, teardown_isdir)
def test_isdir():
    assert True == os.path.isdir('hello'), 'hello is not a dir'


# TODO 判断是否是绝对路径
def setup_isabs():
    print '*************** test isabs ***************'
    open('hello', 'w')


def teardown_isabs():
    os.remove('hello')


@with_setup(setup_isabs, teardown_isabs)
def test_isabs():
    assert False == os.path.isabs('hello'), 'hello is a abs'
    assert True == os.path.isabs(os.path.join(mount_dir, 'hello')), 'hello is not a abs'


# TODO 检验给出的路径是否真地存
def setup_exists():
    print '*************** test exists ***************'
    open('hello', 'w')


def teardown_exists():
    os.remove('hello')


@with_setup(setup_exists, teardown_exists)
def test_exists():
    assert True == os.path.exists('hello'), 'path hello not exists'
    assert False == os.path.exists('hello/hello'), 'path hello/hello exists'


# TODO 重命名
def setup_rename():
    print '*************** test rename ***************'
    os.mkdir('hellodir')
    os.mknod('hellonod')


def teardown_rename():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

@with_setup(setup_rename, teardown_rename)
def test_rename():
    os.rename('hellodir', 'hellopath')
    os.rename('hellomod', 'hellofile')


# TODO 创建多级目录
def setup_makedirs():
    print '*************** test makedirs ***************'


def teardown_makedirs():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

@with_setup(setup_makedirs, teardown_makedirs)
def test_makedirs():
    os.makedirs('hello/1')
    assert True == os.path.exists('hello/1'), 'hello/1 not maked'


# TODO 获取文件属性
def setup_stat():
    print '*************** test stat ***************'
    open('hello', 'w')


def teardown_stat():
    os.remove('hello')


@with_setup(setup_stat, teardown_stat)
def test_stat():
    #os.chmod('hello', 0666)
    stat = os.stat('hello')
    assert 33188 == stat.st_mode, 'hello mode is not 0666 error %s' % stat.st_mode


# TODO 修改文件权限
def setup_chmod():
    print '*************** test chmod ***************'
    open('hello', 'w')


def teardown_chmod():
    os.remove('hello')


@with_setup(setup_chmod, teardown_chmod)
def ignoretest_chmod():
    os.chmod('hello', 0666)
    stat = os.stat('hello')
    assert 0666 == stat.st_mode, 'hello mode chmod failed error %s' % stat.st_mode


# TODO 获取文件大小
def setup_getsize():
    print '*************** test getsize ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    f = open('hello', 'a')
    f.write('*' * 128)
    f.close()


def teardown_getsize():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_getsize, teardown_getsize)
def test_getsize():
    size = os.path.getsize('hello')
    assert 128 == size, 'hello size is %s' % size


# TODO ##############################################################
# TODO                   **文件操作**                                #
# TODO ##############################################################

# TODO 创建空文件
def setup_mknod():
    print '*************** test mknod ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_mknod():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_mknod, teardown_mknod)
def test_mknod():
    open('hello', 'w')
    assert True == os.path.exists('hello'), 'hello not exit'


# TODO 直接打开一个文件，如果文件不存在则创建文件
def setup_open():
    print '*************** test open ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_open():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_open, teardown_open)
def test_open():
    # TODO 模式：
    # TODO w 以写方式打开，
    # TODO a 以追加模式打开(从EOF开始, 必要时创建新文件)
    # TODO r + 以读写模式打开
    # TODO w + 以读写模式打开(参见 w )
    # TODO a + 以读写模式打开(参见 a )
    # TODO rb 以二进制读模式打开
    # TODO wb 以二进制写模式打开(参见 w )
    # TODO ab 以二进制追加模式打开(参见 a )
    # TODO rb + 以二进制读写模式打开(参见 r + )
    # TODO wb + 以二进制读写模式打开(参见w + )
    # TODO ab + 以二进制读写模式打开(参见a + )
    open('hello_1', 'w')
    open('hello_2', 'a')
    open('hello_1', 'r+')
    open('hello_4', 'a+')
    open('hello_5', 'w+')
    open('hello_1', 'rb')
    open('hello_1', 'wb')
    open('hello_1', 'ab')
    open('hello_1', 'rb+')
    open('hello_1', 'wb+')
    open('hello_1', 'ab+')


# TODO size为读取的长度，以byte为单位
def setup_read():
    print '*************** test read ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
                os.remove(path)
            except:
                pass

    f = open('hello', 'w')
    f.write('*' * 128)
    f.close()


def teardown_read():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
                os.remove(path)
            except:
                pass

@with_setup(setup_read, teardown_read)
def test_read():
    f = open('hello', 'r')
    size = len(f.read(1024))
    assert 128 == size, 'hello size is %s' % size
    f = open('hello', 'r')
    size = len(f.read(4))
    assert 4 == size, 'hello size is %s' % size


# TODO 读一行，如果定义了size，有可能返回的只是一行的一部分
def setup_readline():
    print '*************** test readline ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
                os.remove(path)
            except:
                pass

    f = open('hello', 'w')
    f.write('*' * 128)
    f.write('\n')
    f.write('#' * 128)
    f.close()


def teardown_readline():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
                os.remove(path)
            except:
                pass

@with_setup(setup_readline, teardown_readline)
def test_readline():
    f = open('hello', 'r')
    line = f.readline(512)
    assert 129 == len(line)
    f = open('hello', 'r')
    line = f.readline(4)
    assert 4 == len(line)


# TODO 把文件每一行作为一个list的一个成员，并返回这个list。其实它的内部是通过循环调用readline()来实现的。如果提供size参数，size是表示读取内容的总长，也就是说可能只读到文件的一部分。
def setup_readlines():
    print '*************** test readlines ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    f = open('hello', 'w')
    f.write('*' * 128)
    f.write('\n')
    f.write('#' * 128)
    f.close()


def teardown_readlines():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_readlines, teardown_readlines)
def test_readlines():
    f = open('hello', 'r')
    lines = f.readlines(512)
    assert 129 == len(lines[0])
    assert 128 == len(lines[1])


# TODO 把str写到文件中，write()并不会在str后加上一个换行符
def setup_write():
    print '*************** test write ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_write():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_write, teardown_write)
def test_write():
    f = open('hello', 'w')
    f.write('*' * 128)
    f.close()
    f = open('hello', 'r')
    result = f.read()
    assert 128 == len(result)

    # TODO 把seq的内容全部写到文件中(多行一次性写入)。这个函数也只是忠实地写入，不会在每行后面加上任何东西。


def setup_writelines():
    print '*************** test writelines ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_writelines():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_writelines, teardown_writelines)
def test_writelines():
    f = open('hello', 'w')
    f.writelines('*' * 128)
    f.close()
    f = open('hello', 'r')
    result = f.read()
    assert 128 == len(result)


# TODO 关闭文件。python会在一个文件不用后自动关闭文件，不过这一功能没有保证，最好还是养成自己关闭的习惯。  如果一个文件在关闭后还对其进行操作会产生ValueError
def setup_close():
    print '*************** test close ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_close():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_close, teardown_close)
def test_close():
    f = open('hello', 'w')
    f.close()


# TODO 把缓冲区的内容写入硬盘
def setup_flush():
    print '*************** test flush ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_flush():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_flush, teardown_flush)
def test_flush():
    f = open('hello', 'w')
    f.write('*' * 128)
    f.flush()
    f.close()


# TODO 返回一个长整型的”文件标签“
def setup_fileno():
    print '*************** test fileno ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def teardown_fileno():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_fileno, teardown_fileno)
def test_fileno():
    f = open('hello', 'w')
    f1 = open('hello', 'r')
    assert f.fileno() != f1.fileno()


# TODO 返回文件操作标记的当前位置，以文件的开头为原点
def setup_tell():
    print '*************** test tell ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
               os.remove(path)
            except:
               pass


def teardown_tell():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            try:
               os.remove(path)
            except:
               pass



@with_setup(setup_tell, teardown_tell)
def test_tell():
    f = open('hello', 'w')
    f.write('*' * 128)
    assert 128 == f.tell(), 'tell is %s' % f.tell()
    f.close()


# TODO 返回下一行，并将文件操作标记位移到下一行。把一个file用于for … in file这样的语句时，就是调用next()函数来实现遍历的。
def setup_next():
    print '*************** test next ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    f = open('hello', 'w')
    f.write('*\n')
    f.write('#\n')
    f.close()


def teardown_next():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_next, teardown_next)
def test_next():
    f = open('hello', 'r')
    assert '*\n' == f.next()
    assert '#\n' == f.next()


# TODO 将文件打操作标记移到offset的位置。这个offset一般是相对于文件的开头来计算的，一般为正数。但如果提供了whence参数就不一定了，whence可以为0表示从头开始计算，1表示以当前位置为原点计算。2表示以文件末尾为原点进行计算。需要注意，如果文件以a或a+的模式打开，每次进行写操作时，文件操作标记会自动返回到文件末尾。
def setup_seek():
    print '*************** test seek ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    f = open('hello', 'w')
    f.write('12345')
    f.close()


def teardown_seek():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_seek, teardown_seek)
def test_seek():
    f = open('hello', 'r')
    f.read(1)
    f.seek(0, 0)
    assert '1' == f.read(1)
    f.seek(1, 1)
    assert '3' == f.read(1)
    f.seek(-1, 2)
    assert '5' == f.read(1)


# TODO 把文件裁成规定的大小，默认的是裁到当前文件操作标记的位置。如果size比文件的大小还要大，依据系统的不同可能是不改变文件，也可能是用0把文件补到相应的大小，也可能是以一些随机的内容加上去。
def setup_truncate():
    print '*************** test truncate ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    

def teardown_truncate():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                pass
        else:
            os.remove(path)


@with_setup(setup_truncate, teardown_truncate)
def test_truncate():
    f = open('hello', 'w')
    f.write('12345')
    f.truncate(3)
    f.close()
    f = open('hello', 'r')
    assert '123' == f.read()


# TODO 复制文件
# TODO oldfile和newfile都只能是文件
def setup_copyfile():
    print '*************** test copyfile ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def teardown_copyfile():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_copyfile, teardown_copyfile)
def test_copyfile():
    f = open('hello', 'w')
    f.close()
    shutil.copyfile('hello', 'hello_copy')
    assert True == os.path.exists('hello') and True == os.path.exists('hello_copy')


# TODO 复制文件夹：
# TODO olddir和newdir都只能是目录，且newdir必须不存在
def setup_copy():
    print '*************** test copy ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    f = open('hello', 'w')
    f.close()

def teardown_copy():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_copy, teardown_copy)
def test_copy():
    shutil.copy('hello', 'hello_copy')
    assert True == os.path.exists('hello') and True == os.path.exists('hello_copy')


# TODO oldfile只能是文件夹，newfile可以是文件，也可以是目标目录
def setup_copytree():
    print '*************** test copytree ***************'
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    os.mkdir('hello')
    f = open('hello/1', 'w')
    f.close()


def teardown_copytree():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_copytree, teardown_copytree)
def test_copytree():
    shutil.copytree('hello', 'hello_copy')
    assert True == os.path.exists('hello') and True == os.path.exists('hello_copy') \
           and True == os.path.exists('hello_copy/1')


# TODO 重命名文件(目录)
def setup_rename():
    print '*************** test rename ***************'
    os.mknod('hello_1')
    os.mkdir('hello')


def teardown_rename():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_rename, teardown_rename)
def test_rename():
    os.rename('hello_1', 'newhello_1')
    os.rename('hello', 'newhello')
    assert False == os.path.exists('hello'), 'hello path also exists'
    assert False == os.path.exists('hello_1'), 'hello_1 file also exists'
    assert True == os.path.exists('newhello'), 'newhello path not exists'
    assert True == os.path.exists('newhello_1'), 'newhello_1 file not exists'


# TODO 文件或目录都是使用这条命令
# TODO 移动文件（目录）
def setup_move():
    print '*************** test move ***************'
    os.mkdir('hello')
    os.mknod('hello_1')


def teardown_move():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_move, teardown_move)
def test_move():
    shutil.move('hello', 'newhello')
    shutil.move('hello_1', 'newhello_1')
    assert False == os.path.exists('hello'), 'hello path also exists'
    assert False == os.path.exists('hello_1'), 'hello_1 file also exists'
    assert True == os.path.exists('newhello'), 'newhello path not exists'
    assert True == os.path.exists('newhello_1'), 'newhello_1 file not exists'


# TODO 删除文件
def setup_remove():
    print '*************** test remove ***************'
    open('hello', 'w')


def teardown_remove():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_remove, teardown_remove)
def test_remove():
    os.remove('hello')
    assert False == os.path.exists('hello'), 'hello path also exists'


# TODO 删除空目录
def setup_rmdir():
    print '*************** test rmdir ***************'
    os.mkdir('hello')


def teardown_rmdir():
    for path in os.listdir(mount_dir):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


@with_setup(setup_rmdir, teardown_rmdir)
def test_rmdir():
    os.rmdir('hello')
    assert False == os.path.exists('hello'), 'hello path also exists'


# TODO 空目录、有内容的目录都可以删
def setup_rmtree():
    print '*************** test rmtree ***************'
    os.mkdir('hello')
    os.mkdir('hello/1')
    os.mknod('hello/2')


def teardown_rmtree():
    pass


@with_setup(setup_rmtree, teardown_rmtree)
def test_rmtree():
    shutil.rmtree('hello')
    assert False == os.path.exists('hello'), 'hello path also exists'

