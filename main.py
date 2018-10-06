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
        self.list_file_box = None
        self.path_root = []
        self.myFileOption = fileOption()
        self.C = IntVar()
        self.D = IntVar()
        self.E = IntVar()
        self.F = IntVar()
        self.PATH_C = "C:\\"
        self.PATH_D = "D:\\"
        self.PATH_E = "E:\\"
        self.PATH_F = "F:\\"
        self.list_file_c = []
        self.list_file_d = []
        self.list_file_e = []
        self.list_file_f = []
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

        f_path = Frame(f_top, relief=GROOVE, bd=2)
        f_path.pack(side=LEFT)
        self.input_path = StringVar()
        Label(f_path, text="path: ").pack(side=LEFT)
        entry_path = Entry(f_path, textvariable=self.input_path)
        entry_path.pack(side=LEFT)
        entry_path.bind("<Return>",self.doTask_loadPath)
        btn_path = Button(f_path, text=" Go ", command=self.doTask_loadPath).pack(side=LEFT)

        f_search = Frame(f_top, relief=GROOVE,bd=2)
        f_search.pack(side=LEFT)
        f_search_1 = Frame(f_search, relief=GROOVE, bd=2)
        f_search_1.pack(side=TOP)
        f_search_2 = Frame(f_search, relief=GROOVE, bd=2)
        f_search_2.pack(side=TOP)
        label_search = Label(f_search_1, text="search: ").pack(side=LEFT)
        entry_search = Entry(f_search_1, textvariable=self.query)
        entry_search.pack(side=LEFT)
        entry_search.bind("<Return>",self.doTask_search)
        btn_search = Button(f_search_1, text=" Go ", command=self.doTask_search).pack(side=LEFT)
        ckbtn_C = Checkbutton(f_search_2, text="C盘", variable=self.C).pack(side=LEFT)
        ckbtn_D = Checkbutton(f_search_2, text="D盘", variable=self.D).pack(side=LEFT)
        ckbtn_E = Checkbutton(f_search_2, text="E盘", variable=self.E).pack(side=LEFT)
        ckbtn_F = Checkbutton(f_search_2, text="F盘", variable=self.F).pack(side=LEFT)

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


    def getAllFiles(self):
        self.list_all_file = []
        c,d,e,f = self.C.get(), self.D.get(), self.E.get(), self.F.get()
        
        # 当用户没有具体选择哪个盘时，我们将搜索范围定为除 C 盘(太慢了)外的所有盘
        if c==0 and d==0 and e==0 and f==0:
            c,d,e,f = 0,1,1,1
        if c:
            if not self.list_file_c:
                self.list_file_c = self.myFileOption.getListFiles(self.PATH_C)
            self.list_all_file = self.list_all_file + self.list_file_c
        if d:
            if not self.list_file_d:
                self.list_file_d = self.myFileOption.getListFiles(self.PATH_D)
            self.list_all_file = self.list_all_file + self.list_file_d
        if e:
            if not self.list_file_e:
                self.list_file_e = self.myFileOption.getListFiles(self.PATH_E)
            self.list_all_file = self.list_all_file + self.list_file_e
        if f:
            if not self.list_file_f:
                self.list_file_f = self.myFileOption.getListFiles(self.PATH_F)
            self.list_all_file = self.list_all_file + self.list_file_f
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

    def show(self, future=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.result[:100]:
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
        # 该方法在两种情况下会被调用，搜索任务完成时，及用户点击显示条目时
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