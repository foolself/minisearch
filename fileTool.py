import os
import time
class fileOption(object):
    def __init__(self):
        self.list_file = []

    def getListFiles(self, dir_path):
        self.list_file = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    desc = os.stat(file_path)
                except:
                    pass
                try:
                    # 第一个‘0’，暂无安排
                    self.list_file.append([0, file, file_path, desc.st_size, 
                                    str(time.localtime(desc.st_atime).tm_year) + '.' + str(time.localtime(desc.st_atime).tm_mon) + '.' + str(time.localtime(desc.st_atime).tm_mday), 
                                    str(time.localtime(desc.st_mtime).tm_year) + '.' + str(time.localtime(desc.st_mtime).tm_mon) + '.' + str(time.localtime(desc.st_mtime).tm_mday), 
                                    str(time.localtime(desc.st_ctime).tm_year) + '.' + str(time.localtime(desc.st_ctime).tm_mon) + '.' + str(time.localtime(desc.st_ctime).tm_mday)])
                except:
                    self.list_file.append([0, file, file_path, desc.st_size, 
                                    str(time.localtime(desc.st_atime).tm_year) + '.' + str(time.localtime(desc.st_atime).tm_mon) + '.' + str(time.localtime(desc.st_atime).tm_mday), 
                                    '0000.0.0', 
                                    str(time.localtime(desc.st_ctime).tm_year) + '.' + str(time.localtime(desc.st_ctime).tm_mon) + '.' + str(time.localtime(desc.st_ctime).tm_mday)])
        return self.list_file
    
    def deleteFiles(self, files):
        for f in files:
            os.remove(f)
        return self.list_file
    
    def copyFiles(self):
        pass

    def printFileList(self):
        for f in self.list_file:
            print(f)

def main():
    myFileOption = fileOption()
    list_ = myFileOption.getListFiles("F:\\")

if __name__ == '__main__':
    main()