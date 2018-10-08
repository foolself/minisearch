import re
import os
import asyncio
from threading import Thread
import sqlite3
import types
from tkinter import *
from tkinter import ttk, messagebox, Event
from fileTool import fileOption
from renameDialog import RenameDialog

class App():
    def __init__(self, master):
        master.title("Mini Search")
        self.master = master
        self.query = StringVar()
        self.list_all_file = []
        self.result = []
        # self.list_file_box = None
        self.myFileOption = fileOption()
        self.FLAG_SIZE_SORT = False
        self.FLAG_TASK = 0
        
        f = Frame(master)
        f.pack(fill=BOTH,expand=TRUE)

        menu = Menu(master, tearoff=0)
        menu.add_command(label="delete", command=self.doDelete)
        menu.add_command(label="copy", command=self.doCopy)
        menu.add_command(label="rename", command=self.doRename)
        def popupmenu(event):
            menu.post(event.x_root, event.y_root)
        master.bind("<Button-3>",popupmenu)

        f_top = Frame(f, relief=GROOVE, bd=2)
        f_center = Frame(f, relief=GROOVE,bd=2)
        f_state = Frame(f, relief=GROOVE,bd=2)
        f_top.pack(side=TOP, fill=X)
        f_center.pack(side=TOP, fill=BOTH, expand=True)
        f_state.pack(side=TOP, fill=X)

        self.str_search_count = StringVar()
        self.str_select_count = StringVar()
        self.str_process_bar = StringVar()
        self.str_search_count.set('0')
        self.str_select_count.set('0')
        self.str_process_bar.set('search done.')
        Label(f_state,text="search result: ").pack(side=LEFT)
        Label(f_state, textvariable=self.str_search_count).pack(side=LEFT)
        Label(f_state, text="    selection: ").pack(side=LEFT)
        Label(f_state, textvariable=self.str_select_count).pack(side=LEFT)
        Label(f_state, text="    process: ").pack(side=LEFT)
        Label(f_state, textvariable=self.str_process_bar).pack(side=LEFT)
        Button(f_state, text="<", command=self.toNextPage).pack(side=RIGHT)
        self.int_page = IntVar()
        self.int_page.set(1)
        Label(f_state, textvariable=self.int_page).pack(side=RIGHT)
        Button(f_state, text="<", command=self.toPreviousPage).pack(side=RIGHT)

        f_path = Frame(f_top, relief=GROOVE, bd=2)
        f_path.pack(side=LEFT)
        self.input_path = StringVar()
        Label(f_path, text="path: ").pack(side=LEFT)
        entry_path = Entry(f_path, textvariable=self.input_path)
        entry_path.pack(side=LEFT)
        entry_path.bind("<Return>",self.doTask_loadPath)
        Button(f_path, text=" Go->", command=self.doTask_loadPath).pack(side=LEFT)

        f_search = Frame(f_top, relief=GROOVE,bd=2)
        f_search.pack(side=LEFT)
        f_search_1 = Frame(f_search, relief=GROOVE, bd=2)
        f_search_1.pack(side=TOP)
        f_search_2 = Frame(f_search, relief=GROOVE, bd=2)
        f_search_2.pack(side=TOP)
        Label(f_search_1, text="search: ").pack(side=LEFT)
        entry_search = Entry(f_search_1, textvariable=self.query)
        entry_search.pack(side=LEFT)
        entry_search.bind("<Return>",self.doTask_search)
        Button(f_search_1, text=" Go->", command=self.doTask_search).pack(side=LEFT)
        Button(f_search_1, text="清除缓存", command=self.doFlushCache).pack(side=LEFT)
        
        self.list_diskSymbol = self.myFileOption.getDiskSymbol()
        self.list_diskSymbol_flag = []
        self.list_file_each_disk = []
        for i, diskSymbol in enumerate(self.list_diskSymbol):
            self.list_diskSymbol_flag.append(IntVar())
            self.list_file_each_disk.append([])
            Checkbutton(f_search_2, text=diskSymbol, variable=self.list_diskSymbol_flag[i]).pack(side=LEFT)

        self.scrollbar = Scrollbar(f_center)
        # self.list_file_box = Listbox(f_center, selectmode=MULTIPLE, yscrollcommand=self.scrollbar.set)
        self.tree = ttk.Treeview(f_center,columns=['filename','abspath','size','a_time','m_time','c_time'],
                                selectmode=EXTENDED,show='headings',
                                yscrollcommand=self.scrollbar.set)
        self.tree.heading('filename',text='文件名')
        self.tree.heading('abspath',text='路径')
        self.tree.heading('size',text='文件大小',command=self.sortBySize)
        self.tree.heading('a_time',text='访问时间',command=self.sortByATime)
        self.tree.heading('m_time',text='修改时间',command=self.sortByMTime)
        self.tree.heading('c_time',text='创建时间',command=self.sortByCTime)
        self.tree.bind("<ButtonRelease-1>", self.flashState)
        self.tree.bind("<Double-Button-1>", self.doOpenPath)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

    def _async_thread(self, args):
        print("search thread begin.")
        coroutine = self.doSearch()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(coroutine)
        # 线程完成之后，刷新 UI
        task.add_done_callback(self.show)
        loop.run_until_complete(task)
        print("done.")

    def doTask_search(self, event=None):
        self.FLAG_TASK = 0
        Thread(target=self._async_thread,args=(0,)).start()

    def doTask_loadPath(self, event=None):
        self.FLAG_TASK = 1
        Thread(target=self._async_thread,args=(0,)).start()

    def doFlushCache(self):
        for i in range(len(self.list_file_each_disk)):
            self.list_file_each_disk[i] = []

    def getAllFiles(self):
        self.list_all_file = []
        for i, rootPath in enumerate(self.list_diskSymbol):
            if self.list_diskSymbol_flag[i].get():
                if not self.list_file_each_disk[i]:
                    self.list_file_each_disk[i] = self.myFileOption.getListFiles(rootPath)
                self.list_all_file = self.list_all_file + self.list_file_each_disk[i]
        print("getAllFiles() done.")
        return self.list_all_file
    
    def selectAll(self):
        pass

    def searchFile(self):
        self.result = []
        query_ = self.query.get()
        # '\', '*' 不能作为搜索条件, 有 bug
        if query_ == '\\' or query_ == '*':
            return 1
        for f in self.list_all_file:
            if re.search(query_,f[1]):
                self.result.append(f)
    
    # 从数据库中搜索，因为为解决更新的问题，暂时不实用
    def searchFile_with_db(self):
        self.result = []
        query_ = '%' + self.query.get() + '%'
        conn = sqlite3.connect('filesCache.db')
        cursor = conn.cursor()
        cursor.execute('select * from files where filename like ?',(query_,))
        self.result = cursor.fetchall()
        cursor.close()
        conn.close()

    def sort(self, byId):
        result_ = self.result
        self.result = sorted(result_,key=lambda result_ : result_[byId], reverse=self.FLAG_SIZE_SORT)
        self.FLAG_SIZE_SORT = not self.FLAG_SIZE_SORT
        self.show()
    
    def sortBySize(self):
        self.sort(3)
    def sortByATime(self):
        self.sort(4)
    def sortByMTime(self):
        self.sort(5)
    def sortByCTime(self):
        self.sort(6)

    def toNextPage(self, event=None):
        if self.int_page.get() + 1 > len(self.result) // 100 + 1:
            print("out of pages")
            return None
        self.int_page.set(self.int_page.get() + 1)
        self.show()

    def toPreviousPage(self, event=None):
        if self.int_page.get() - 1 < 1:
            print("out of pages")
            return None
        self.int_page.set(self.int_page.get() - 1)
        self.show()

    def show(self, future=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.result[100 * (self.int_page.get() - 1) : 100 * self.int_page.get()]:
            self.tree.insert('','end',values=item[1:])
        self.flashState()

    async def doSearch(self, event=None):
        # await asyncio.sleep(1)
        self.str_process_bar.set("do search...")
        if self.FLAG_TASK == 0:
            self.getAllFiles()
            self.searchFile()
        else :
            self.result = self.myFileOption.listDir(self.input_path.get())
        # self.searchFile_with_db()
        self.flashState()
    
    def getSelectionFileAbsPath(self):
        list_ = []
        for i in self.tree.selection():
            list_.append(self.tree.item(i).get('values')[1])
        return list_
    
    def doOpenPath(self, event):
        cmd_comm = "explorer /select, " + self.tree.item(self.tree.selection()[0]).get('values')[1]
        print(cmd_comm)
        os.system(cmd_comm)
    def doDelete(self):
        if self.tree.selection():
            ask = messagebox.askokcancel("Delete","确认删除这些文件?")
            if ask:
                self.myFileOption.deleteFiles(self.getSelectionFileAbsPath())
                for i in self.tree.selection():
                    self.tree.delete(i)
                self.result = []
                for i in self.tree.get_children():
                    self.result.append(self.tree.item(i).get("values"))

    def doCopy(self):
        pass

    def doRename(self):
        renameDialog = RenameDialog(self.getSelectionFileAbsPath(), self.myFileOption)
        self.master.wait_window(renameDialog)

    def flashState(self, event=None):
        # 该方法在两种情况下会被调用，搜索任务完成时，及用户点示条目时
        # 这里加入一个判断，当 event 为 tkinter.Event 类时，说明调用为后者，否则为前者
        if not isinstance(event,Event):
            self.str_process_bar.set("search done.")
        self.str_search_count.set(str(len(self.result)))
        self.str_select_count.set(str(len(self.tree.selection())))
    
def main():
    root = Tk()
    myApp = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()