import tkinter as tk
from gui import StegGUI

def main():
    root = tk.Tk()
    app = StegGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()