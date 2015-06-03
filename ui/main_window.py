from Tkinter import *
from ttk import *

root = Tk()

strategy = StringVar()
strategy_label = Label(root, text="Analyze strategy: ").grid(row=0, column=0)
directories = Radiobutton(root, text='Directories', variable=strategy, value='home').grid(row=0, column=1)
file_types = Radiobutton(root, text='File types', variable=strategy, value='office').grid(row=0, column=2)

root_directory_label = Label(root, text="Root directory:  ").grid(row=0, column=3)

root_value = StringVar()
root_combo = Combobox(root, textvariable=root_value)
root_combo['values'] = [str(x) for x in range(100)]  # ('X', 'Y', 'Z')
root_combo.current(0)
root_combo.grid(row=0, column=4)

analyze_button = Button(root, text="Analyze!").grid(row=0, column=5)

mainloop()
