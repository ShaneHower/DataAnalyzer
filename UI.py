"""
blue print for building a simple user interface
"""
try:
    from tkinter import *  # for python 3
    import tkinter.scrolledtext as tkst
except:
    from Tkinter import *  # for python 2
    import ScrolledText as tkst
from DataAnalyzer import DataAnalyzer


class UserInterface(Tk):
    def __init__(self, pass_two=None):
        Tk.__init__(self)
        self.entry = Entry(self)
        if pass_two:
            self.pass_two = True
        else:
            self.set_up()

    def text(self, text, scroll=None):
        if scroll:
            inner_frame = Frame(self)
            inner_frame.pack(fill='both', expand='yes')
            scrollbar = tkst.ScrolledText(master=inner_frame, wrap='word', width=10, height=5)
            scrollbar.pack(fill='both', expand=True, padx=8, pady=8)
            scrollbar.insert('insert', text)

        else:
            txt_setup = StringVar()
            note = Label(self, textvariable=txt_setup)
            txt_setup.set(text)
            note.pack()

    def input_box(self, label, password=None):
        text = StringVar()
        descr = Label(self, textvariable=text)
        text.set(label)

        # descr.grid(row=0, column=0, pady=5)
        descr.pack(fill=X, padx=5)

        if password:
            entry = Entry(self, width=13, show="*")
        else:
            entry = Entry(self, width=13)

        # entry.grid(row=0, column=2, padx=10, pady=3)
        entry.pack(fill=X, padx=5, pady=10, expand=True)

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

        self.button_next = Button(self, text="Next", command=self.on_next)
        self.button_next.grid(row=0, column=1)
        self.button_next.pack(side=RIGHT)

    def set_up2(self, header):
        self.text(" ")
        count = 1
        input_text = ""
        for title in header:

            new_txt = "{0}.".format(count)+ " " + title + "\n"
            input_text = input_text + new_txt
            # self.text("{0}.".format(count) + " " + num)
            count += 1
        self.text(input_text, scroll=True)
        # self.text("pick the column title that represents each variable below")
        # self.text("Input the numbered position (for example if you want the column title in the "
        #           "first position, input 1)")
        self.text(" ")

        self.col_date = self.input_box("Date")
        self.col_acct = self.input_box("Account Number")
        self.col_part = self.input_box("Item Number")
        self.col_price = self.input_box("Unit Price")
        self.col_extprice = self.input_box("Extended Price")


        self.enter = Button(self, text="Enter", command=self.on_enter)
        self.enter.pack(side=RIGHT)

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