import os
import time
class fileOption(object):
    def __init__(self):
        self.list_file = []

    def getInfo(self, file, file_path):
        try:
            desc = os.stat(file_path)
        except:
            print("ERROR: desc = os.stat(file_path)")
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
    def getListFiles(self, dir_path):
        self.list_file = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.getInfo(file, file_path)
        return self.list_file
    
    def listDir(self, dir_path):
        self.list_file = []
        for i in os.listdir(dir_path):
            file_path = os.path.join(dir_path, i)
            self.getInfo(i, file_path)
        return self.list_file

    def deleteFiles(self, files):
        for f in files:
            try:
                os.remove(f)
            except:
                print("remove faild: " + f)
        return self.list_file
    
    def copyFiles(self):
        pass

    def renameFiles(self, list_name_old, list_name_new):
        for i in range(len(list_name_old)):
            try:
                os.rename(list_name_old[i], list_name_new[i])
            except:
                print("rename faild: " + list_name_old[i] + "--->" + list_name_new[i])
    def printFileList(self):
        for f in self.list_file:
            print(f)

def main():
    myFileOption = fileOption()
    # list_ = myFileOption.getListFiles("F:\\")
    # list_ = myFileOption.listDir("F:\\code")
    # myFileOption.printFileList()
    myFileOption.renameFiles(["E:\\test\\sdgdg.txt","E:\\test\\32534.txt"],["E:\\test\\test_1.txt","E:\\test\\test_2.txt"])

if __name__ == '__main__':
    main()