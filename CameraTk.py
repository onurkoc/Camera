#!usr/bin/env python3

from tkinter import font, Frame, Label, Button, Tk, messagebox, Entry
import tkinter as tk
import Camera as cam


class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_window()
        cam.killgphoto2Process()  # kill the running process with initiation

    def init_window(self):
        self.master.title("CameraPy")
        self.centerWindow()

        self.grid()

        self.customFont = font.Font(family='Verdana', size=10)

        # Kill button
        kill_button_label = Label(self, text=" Kill gphoto",
                                  font=self.customFont)
        kill_button_label.grid(row=0, column=0, sticky="W")
        kill_button = Button(self, text="Kill", width=10, 
							 command=cam.killgphoto2Process,
                             font=self.customFont)
        kill_button.grid(row=0, column=1, sticky="E")

        # Test button
        test_button = Button(self, text=" Shoot ", width=20,
                             command=self.dialog, font=self.customFont)
        test_button.grid(columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)

        # Toggle button
        toggle_button_label = Label(self, text=" Time lapse ",
                                    font=self.customFont, anchor=tk.W)
        toggle_button_label.grid(row=2, column=0)
        self.toggle_button = Button(self, text="Off", width=10,
                                    relief="raised", command=self.toggle,
                                    font=self.customFont)
        self.toggle_button.grid(row=2, column=1)

        # Duration entry
        duration_label = Label(self, text=" Sleep ", font=self.customFont)
        duration_label.grid(row=3, column=0, sticky=tk.W)
        self.duration_entry = Entry(self, font=self.customFont, width=10,
                                    justify=tk.RIGHT, state='disabled')
        self.duration_entry.grid(row=3, column=1)

        # Quit button
        quitButton = Button(self, text="Quit", width=10, font=self.customFont,
                            command=self.quit)
        quitButton.grid(row=4, column=1)

    def quit(self):
        root.destroy()

    def dialog(self):
        messagebox.showinfo("test", "Ahoy")

    def centerWindow(self):

        w = 175
        h = 135

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def toggle(self):
        """regulate the toggling action of on/off button"""
        if self.toggle_button.config('relief')[-1] == 'sunken':
            self.toggle_button.config(relief="raised")
            self.toggle_button.config(text="Off")
            self.duration_entry.config(state='disabled')
        else:
            self.toggle_button.config(relief="sunken")
            self.toggle_button.config(text="On")
            self.duration_entry.config(state='normal')
            if self.duration_entry.get() == '':
                add_placeholder_to(entry=self.duration_entry,
                                   placeholder='seconds')


class Placeholder_State():
    __slots__ = 'normal_color', 'normal_font', 'placeholder_text', \
                'placeholder_color', 'placeholder_font', 'with_placeholder'


if __name__ == '__main__':
    root = Tk()
    root.columnconfigure(2, {'minsize': 30})
    # root.geometry("175x135")
    root.resizable(False, False)
    # root.tk.call('tk', 'scaling', 2.0)

    def add_placeholder_to(entry, placeholder, color="grey", font=None):
        """recipe for adding a placeholder for an entry
        resource:
        http://code.activestate.com/recipes/580768-tkinter-entry-with-
        placeholder/"""
        normal_color = entry.cget("fg")
        normal_font = entry.cget("font")

        if font is None:
            font = normal_font

        state = Placeholder_State()
        state.normal_color = normal_color
        state.normal_font = normal_font
        state.placeholder_color = color
        state.placeholder_font = font
        state.placeholder_text = placeholder
        state.with_placeholder = True

        def on_focusin(event, entry=entry, state=state):
            if state.with_placeholder:
                entry.delete(0, "end")
                entry.config(fg=state.normal_color, font=state.normal_font)

                state.with_placeholder = False

        def on_focusout(event, entry=entry, state=state):
            if entry.get() == '':
                entry.insert(0, state.placeholder_text)
                entry.config(fg=state.placeholder_color,
                             font=state.placeholder_font)

                state.with_placeholder = True

        entry.insert(0, placeholder)
        entry.config(fg=color, font=font)

        entry.bind('<FocusIn>', on_focusin, add="+")
        entry.bind('<FocusOut>', on_focusout, add="+")

        entry.placeholder_state = state

        return state

    app = Window(root)
    root.mainloop()
