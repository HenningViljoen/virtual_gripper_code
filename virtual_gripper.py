#StratLytic 2020

import tkinter as tk


from source.simulation import Simulation


class VirtualGripper(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.gripper_simulation = Simulation()
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        tk_rgb = "#%02x%02x%02x" % (128, 192, 200)

        self.leftFrame = tk.Frame(self, bg=tk_rgb)
        self.leftFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.buttonsimfast = tk.Button(self.leftFrame, text="SimFast",
                                       command=self.simulate_button_event)
        self.buttonsimfast.grid(padx=3, pady=2,
                                row=18, column=0,
                                sticky=tk.NW)

        self.canvas = tk.Canvas(self, bg='#FFFFFF', width=1400, height=800, scrollregion=(0, 0, 3000, 2000))
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


    def simulate_button_event(self):
        self.gripper_simulation.do_simulation(self.canvas)


    def run_gripper(self):
        self.gripper_simulation.simulate_one_step(self.canvas)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Virtual Gripper")
    app = VirtualGripper(root)
    root.mainloop()


