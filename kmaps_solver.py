import tkinter as tk
from tkinter import ttk
from kmaps import Kmaps
from qmc import QuineMcCluskey

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.minterm = []
        self.dontcare =[]
        self.result = "Minization Result"
        # configure the root window
        self.title('Four Variable K-Maps Solver')
        #self.geometry("%dx%d+0+0" % self.maxsize())
     
               
        self.frame1 = tk.Frame(self, bg='red')
        self.frame1.grid(row=0, column=0, padx=10, pady=10)
        
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.grid(row=1, column=0, padx=10, pady=10)
        
        self.frame3 = tk.Frame(self.frame1, bg='red')
        self.frame3.grid(row=1, column=1, padx=10, pady=10)
        
        self.frame4 = tk.Frame(self.frame1, bg='red')
        self.frame4.grid(row=2, columnspan=2, padx=10, pady=10)
        
        # label
        self.label = ttk.Label(self.frame1, text='K-Maps Solver', font=("Arial", 16))
        self.label.grid(row=0, columnspan=2, padx=5, pady=5)
        
        #Textbox and scrollbar      
        self.text_box = tk.Text(self.frame4, bg="#F0F0F0", height=20, width=100 )
        self.scroll = tk.Scrollbar(self.frame4, command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=self.scroll.set)
        self.text_box.pack(side="left")
        self.scroll.pack(side="right", fill="y")
        self.text_box.insert("end", "K-Maps Solver by Taner TOPAL")
        
        self.min_str = f"Minterm: {self.minterm}"
        self.dcare_str = f"dontcare: {self.dontcare}"
        self.result_str = f"Result: {self.result}"
        self.label_min = ttk.Label(self.frame3, text=self.min_str, font=("Arial", 10), width=50)
        self.label_min.grid(row=0, column=0, padx=3, pady=3)
        self.label_dcare = ttk.Label(self.frame3, text=self.dcare_str, font=("Arial", 10), width=50)
        self.label_dcare.grid(row=1, column=0, padx=3, pady=3)
        self.label_result = ttk.Label(self.frame3, text=self.result_str, font=("Arial", 10), width=50)
        self.label_result.grid(row=2, column=0, padx=3, pady=3)
        
        self.lbl_CD = tk.Label(self.frame2, text='CD', anchor='center')
        self.lbl_CD.grid(column=1, row=0, columnspan=5)
        
        self.lbl_AB = tk.Label(self.frame2, text='AB', anchor='center')
        self.lbl_AB.grid(row=1, column=0, rowspan=5)
        
        self.lbl_corner = tk.Label(self.frame2, text="✕", anchor='center', font=("Arial", 20))
        self.lbl_corner.grid(row=0, column=0, rowspan=2, columnspan=2)
        
        self.lblx = [0 for x in range(4)]
        self.lbly = [0 for x in range(4)]
        self.btn = [[0 for x in range(4)] for x in range(4)]
        self.minterm_btn = [[0,1,3,2], [4, 5, 7, 6], [12, 13, 15, 14], [8, 9, 11, 10]]
        
        for x in range(2,6):
            self.lblx[x-2] = tk.Label(self.frame2, text="00", width=3, borderwidth=2, relief="sunken")
            self.lblx[x-2].grid(column=x, row=1)
        
        for x in range(2,6):
            self.lbly[x-2] = tk.Label(self.frame2, text="00", width=3, borderwidth=2, relief="sunken")
            self.lbly[x-2].grid(column=1, row=x)
        
        self.frame5 = tk.Frame(self.frame2)
        self.frame5.grid(row=2, column=2, rowspan=4, columnspan=4)
        
        for x in range(4):
             for y in range(4):
                self.btn[x][y] = tk.Button(self.frame5, text="", width=3, command=lambda x=x, y=y: self.popup(x,y))
                self.btn[x][y].grid(column=x, row=y)
        
        self.lblx[1].config(text='01')
        self.lblx[2].config(text='11')
        self.lblx[3].config(text='10')
        self.lbly[1].config(text='01')
        self.lbly[2].config(text='11')
        self.lbly[3].config(text='10')
                
        self.btn_clear = ttk.Button(self.frame3, text="Clear", width=6, command=lambda:self.clear())
        self.btn_clear.grid(row=3, column=1, padx=3, pady=3)
        self.btn_calc = ttk.Button(self.frame3, text="Calculate", width=10, command=lambda:self.calculate())
        self.btn_calc.grid(row=3, column=2, padx=3, pady=3)

        
    def clear(self):
        self.minterm =[]    
        self.dontcare=[]
        
        for x in range(4):
             for y in range(4):
                self.btn[x][y].config(text='', bg="#F0F0F0")
                
        self.min_str = f"Minterm: {self.minterm}"
        self.dcare_str = f"dontcare: {self.dontcare}"
        self.result_str = f"Result: {self.result}"
        self.label_min.configure(text= self.min_str)
        self.label_dcare.configure(text= self.dcare_str)
        self.label_result.configure(text= self.result_str)
        self.text_box.delete("2.0","end")
        
    
    def calculate(self):
        #print(self.minterm)    
        #print(self.dontcare)
        self.qm = QuineMcCluskey()
        self.final_result, self.result_str = self.qm.find_result(self.minterm, self.dontcare, 4)
        
        self.mint = Kmaps(self.minterm, self.dontcare)
        self.label_result.configure(text= self.result_str)
        self.text_box.insert("end", self.mint.pri_grp_str)
        self.text_box.insert("end", self.mint.all_pi_str)
        self.text_box.insert("end", self.mint.chart_str)
        self.text_box.insert("end", f"\n{self.result_str}")
        
        
    def state_change(self, x, y, label):

        if label=='0':
            self.btn[x][y].config(text='', bg="#F0F0F0")
            if self.minterm_btn[y][x] in self.minterm:   
                self.minterm.remove(self.minterm_btn[y][x])
            if self.minterm_btn[y][x] in self.dontcare:    
                self.dontcare.remove(self.minterm_btn[y][x])
        elif label=='1':
            self.btn[x][y].config(text='1', bg="blue")
            self.minterm.append(self.minterm_btn[y][x])
            if self.minterm_btn[y][x] in self.dontcare:
                self.dontcare.remove(self.minterm_btn[y][x])
        elif label=='x':
            self.btn[x][y].config(text='x', bg="yellow")
            self.dontcare.append(self.minterm_btn[y][x])
            if self.minterm_btn[y][x] in self.minterm:   
                self.minterm.remove(self.minterm_btn[y][x])
        self.minterm = list(set(self.minterm))
        self.dontcare = list(set(self.dontcare))
        self.min_str = f"Minterm: {sorted(self.minterm)}"
        self.dcare_str = f"dontcare: {sorted(self.dontcare)}"
        self.label_min.configure(text= self.min_str)
        self.label_dcare.configure(text= self.dcare_str)
        

    #create menu
    def popup(self, x, y):
        self.popup_menu = tk.Menu(self, tearoff = 0)     
        self.popup_menu.add_command(label = f"m{self.minterm_btn[y][x]}")
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label = "0", command = lambda:self.state_change(x,y,'0'))
        self.popup_menu.add_command(label = "1", command = lambda:self.state_change(x,y,'1'))
        self.popup_menu.add_command(label = "x", command = lambda:self.state_change(x,y,'x'))
        self.do_popup(x, y)
        
    
    #display menu on right click
    def do_popup(self, x, y):
        try:
            self.popup_menu.tk_popup(self.btn[x][y].winfo_rootx(), self.btn[x][y].winfo_rooty(), 0)
        finally:
            self.popup_menu.grab_release()
            


if __name__ == "__main__":
    app = App()
    app.mainloop()