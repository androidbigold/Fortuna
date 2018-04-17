def writeseedfile(accumulator, filename):
    with open(filename, 'wb') as f:  # 使用with语句可以保证文件总是会被关闭，不论正常运行还是出错
        f.write(accumulator.randomdata(64))


def updateseedfile(accumulator, filename):
    with open(filename, 'rb+') as f:
        s = f.read()
        assert len(s) == 64, 'Error: incorrect seed length'
        accumulator.g.reseed(s)
        f.seek(0)  # 文件指针移到开头
        f.truncate()  # 清空文件
        f.write(accumulator.randomdata(64))
