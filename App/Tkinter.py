from tkinter import Tk, filedialog


def select_files():
    root = Tk()
    root.withdraw()
    filepaths = filedialog.askopenfilenames(title='Select text files', filetypes=[('Text files', '*.txt')])
    return filepaths
