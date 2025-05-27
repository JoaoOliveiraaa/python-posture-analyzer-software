import tkinter as tk
from models.model import Model
from controllers.controller import Controller

def main():
    root = tk.Tk()
    model = Model()
    controller = Controller(model, root)
    root.mainloop()

if __name__ == "__main__":
    main() 