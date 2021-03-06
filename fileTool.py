import os
import ctypes
import time
class fileOption(object):
    def __init__(self):
        self.list_file = []
        self.STR_FILE_TYPE_F = "File"
        self.STR_FILE_TYPE_D = "Dir"
    def getInfo(self, file_type, file_name, file_path):
        try:
            desc = os.stat(file_path)
        except:
            print("ERROR: desc = os.stat(file_path)")
        try:
            # 第一个‘0’，暂无安排
            self.list_file.append([file_type, file_name, file_path, desc.st_size, 
                            str(time.localtime(desc.st_atime).tm_year) + '.' + str(time.localtime(desc.st_atime).tm_mon) + '.' + str(time.localtime(desc.st_atime).tm_mday), 
                            str(time.localtime(desc.st_mtime).tm_year) + '.' + str(time.localtime(desc.st_mtime).tm_mon) + '.' + str(time.localtime(desc.st_mtime).tm_mday), 
                            str(time.localtime(desc.st_ctime).tm_year) + '.' + str(time.localtime(desc.st_ctime).tm_mon) + '.' + str(time.localtime(desc.st_ctime).tm_mday)])
        except:
            self.list_file.append([file_type, file_name, file_path, desc.st_size, 
                            str(time.localtime(desc.st_atime).tm_year) + '.' + str(time.localtime(desc.st_atime).tm_mon) + '.' + str(time.localtime(desc.st_atime).tm_mday), 
                            '0000.0.0', 
                            str(time.localtime(desc.st_ctime).tm_year) + '.' + str(time.localtime(desc.st_ctime).tm_mon) + '.' + str(time.localtime(desc.st_ctime).tm_mday)])
    def getListFiles(self, dir_path):
        self.list_file = []
        for root, dirs, files in os.walk(dir_path):
            self.getInfo(self.STR_FILE_TYPE_D, root.split("\\")[-1], root)
            for file in files:
                file_path = os.path.join(root, file)
                self.getInfo(self.STR_FILE_TYPE_F, file, file_path)
        return self.list_file
    
    def listDir(self, dir_path, mode):
        if mode:
            self.getListFiles(dir_path)
            return self.list_file
        self.list_file = []
        for i in os.listdir(dir_path):
            file_path = os.path.join(dir_path, i)
            if os.path.isdir(file_path):
                self.getInfo(self.STR_FILE_TYPE_D, i, file_path)
            else:
                self.getInfo(self.STR_FILE_TYPE_F, i, file_path)
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
    
    def getDiskSymbol(self):
        list_ds = []
        IpBuffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(IpBuffer), IpBuffer)
        vol = IpBuffer.raw.split(b'\x00')
        # for i in vol:
        #     print(i)
        for i in range(65, 91):
            vol = chr(i) + ":"
            if os.path.isdir(vol):
                list_ds.append(vol + "\\")
        return list_ds

def main():
    myFileOption = fileOption()
    list_ = myFileOption.getListFiles("E:\\test")
    myFileOption.printFileList()
    # print(list_)
    # list_ = myFileOption.listDir("F:\\code")
    # myFileOption.printFileList()
    # myFileOption.renameFiles(["E:\\test\\sdgdg.txt","E:\\test\\32534.txt"],["E:\\test\\test_1.txt","E:\\test\\test_2.txt"])
    # print(myFileOption.getDiskSymbol())
if __name__ == '__main__':
    main()