"""
blue print for building a simple user interface so user doesn't have to hard code anything to use the scraper
"""
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
from DataAnalyzer import DataAnalyzer


class UserInterface(tk.Tk):
    def __init__(self, pass_two = None):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        if pass_two:
            self.pass_two = True
        else:
            self.set_up()

    def text(self, text):
        txt_setup = tk.StringVar()
        note = tk.Label(self, textvariable=txt_setup)
        txt_setup.set(text)
        note.pack()

    def input_box(self, label, password=None):
        text = tk.StringVar()
        descr = tk.Label(self, textvariable=text)
        text.set(label)

        # descr.grid(row=0, column=0, pady=5)
        descr.pack(fill=tk.X, padx=5)

        if password:
            entry = tk.Entry(self, width=13, show="*")
        else:
            entry = tk.Entry(self, width=13)

        # entry.grid(row=0, column=2, padx=10, pady=3)
        entry.pack(fill=tk.X, padx=5, pady=10, expand=True)

        return entry

    def set_up(self):
        # text_to_input = ['NOTE:',
        #                  'Remember to copy your column titles exactly as they are in excel',
        #                  ' ']
        #
        # for note in text_to_input:
        #     self.text(note)

        self.file_path = self.input_box("File Path (Path of file to input)")
        self.sheet_name = self.input_box("Sheet Name (If applicable specify the excel sheet)")
        self.op_file_name = self.input_box("Save Directory (Path where you want to save the file)")

        self.button_next = tk.Button(self, text="Next", command=self.on_next)
        self.button_next.grid(row=0, column=1)
        self.button_next.pack(side=tk.RIGHT)

    def set_up2(self, header):
        self.text(" ")
        count = 1
        for num in header:
            self.text("{0}.".format(count) + " " + num)
            count += 1
        self.text("pick the column title that represents each variable below")
        self.text("Input the numbered position (for example if you want the column title in the "
                  "first position, input 1)")
        self.text(" ")

        self.col_date = self.input_box("Date")
        self.col_acct = self.input_box("Account Number")
        self.col_part = self.input_box("Item Number")
        self.col_price = self.input_box("Unit Price")
        self.col_extprice = self.input_box("Extended Price")

        self.enter = tk.Button(self, text="Enter", command=self.on_enter)
        self.enter.pack(side=tk.RIGHT)

    def on_next(self):
        self.inst = DataAnalyzer(self.op_file_name.get(), self.file_path.get(), self.sheet_name.get())
        header = self.inst.read_col_titles()
        self.set_up2(header)
        self.button_next.destroy()

    def on_enter(self):
        self.inst.find_descr(self.col_date.get(), self.col_acct.get(), self.col_part.get(), self.col_price.get(), self.col_extprice.get())
        self.destroy()

    def run(self):
        self.mainloop()