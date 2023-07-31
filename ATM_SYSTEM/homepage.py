import tkinter as tk
import sys

w = 1200
h = 650


class mainform:
    def __init__(self, master):
        self.master = master

        # Centre the Window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - w) / 2
        y = (hs - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # Create Frame
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Create Style
        self.master.config(bg="#2A2C2B")
        self.lbl = tk.Label(self.master, text='Home Page', font=('verdana', 50, 'bold'),
                            fg='#ecf0f1', bg="#2A2C2B")
        self.lbl.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

        # Create Close button
        self.close_btn = tk.Button(self.master, text='LOGOUT', font=('verdana', 14),
                                   fg='white', bg='red', relief=tk.RAISED, command=self.close_window)
        self.close_btn.place(rely=0.95, relx=0.95, anchor=tk.SE)

    # Destroy Active Window & Exit Program
    def close_window(self):
        self.master.destroy()
        sys.exit()    # Maybe give problem in future


def main():
    root = tk.Tk()
    mainform(root)
    root.mainloop()


if __name__ == '__main__':
    main()
