"""
Run application
"""
from Tkinter import Tk
from ui.main_window import Application


def main():
    """

    :return: main loop
    """
    root = Tk()
    root.geometry("800x600+300+300")
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
