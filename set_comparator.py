import tkinter
import tkinter.messagebox
import re
import os

WIDTH = 60
HEIGHT = 2
HALF_WIDTH = WIDTH // 2

g_data = {1: set(), 2: set()}


def func_warn(title: str, text: str) -> None:
    tkinter.messagebox.showinfo(title, text)


def func_display(data: set, widget: tkinter.Text) -> None:
    widget.config(state='normal')
    widget.delete('1.0', tkinter.END)
    widget.insert(tkinter.END, '\n'.join(data))
    widget.config(state='disabled')


def func_display_data() -> None:
    func_display(g_data[1], widget=text_display_1)
    func_display(g_data[2], widget=text_display_2)


def func_input(target: int) -> None:
    global g_data
    assert target in g_data, f'wrong key {target}'
    pattern = text_pattern.get('1.0', tkinter.END).strip()
    elements = tuple(i.strip()
                     for i in text_input.get('1.0', tkinter.END).replace(
                         '\n', ',').strip().split(',')
                     if bool(i.strip()))
    if bool(pattern) and pattern not in ('*', '+'):
        try:
            matches = tuple(
                re.findall(pattern, element) for element in elements)
        except Exception as ex:
            func_warn(title='Error in match', text=str(ex))
            return
        elements = tuple(i for m in matches for i in m)
    g_data[target] = set(elements)
    func_display_data()


def func_switch() -> None:
    global g_data
    g_data[1], g_data[2] = g_data[2], g_data[1]
    func_display_data()


def func_apply(func) -> None:
    result = func(g_data[1], g_data[2])
    func_display(data=func(g_data[1], g_data[2]), widget=text_output)


main = tkinter.Tk()
main.title('SETS')

frame_input = tkinter.Frame(main)
frame_display = tkinter.Frame(main)
frame_output = tkinter.Frame(main)
frame_ops = tkinter.Frame(main)

# for input
tkinter.Label(frame_input, height=HEIGHT, width=HALF_WIDTH,
              text='input').pack(side=tkinter.TOP,
                                 expand=tkinter.YES,
                                 fill=tkinter.X)
text_input = tkinter.Text(frame_input, width=WIDTH)
text_input.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
tkinter.Label(frame_input, height=HEIGHT, width=HALF_WIDTH,
              text='pattern').pack(side=tkinter.TOP,
                                   expand=tkinter.YES,
                                   fill=tkinter.X)
text_pattern = tkinter.Text(frame_input, height=HEIGHT, width=WIDTH)
text_pattern.insert(tkinter.END, '[0-9]+')
text_pattern.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

# for display
frame_display_1 = tkinter.Frame(frame_display)
frame_display_2 = tkinter.Frame(frame_display)

tkinter.Label(frame_display_1, height=HEIGHT, width=HALF_WIDTH,
              text='set 1').pack(side=tkinter.TOP,
                                 expand=tkinter.YES,
                                 fill=tkinter.X)
text_display_1 = tkinter.Text(frame_display_1,
                              width=HALF_WIDTH,
                              state=tkinter.DISABLED)
text_display_1.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
text_display_1.bind('<1>', lambda event: text_display_1.focus_set())

tkinter.Label(frame_display_2, height=HEIGHT, width=HALF_WIDTH,
              text='set 2').pack(side=tkinter.TOP,
                                 expand=tkinter.YES,
                                 fill=tkinter.X)
text_display_2 = tkinter.Text(frame_display_2,
                              width=HALF_WIDTH,
                              state=tkinter.DISABLED)
text_display_2.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
text_display_2.bind('<1>', lambda event: text_display_2.focus_set())

frame_display_1.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
frame_display_2.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

# for output
tkinter.Label(frame_output, height=HEIGHT, width=HALF_WIDTH,
              text='output').pack(side=tkinter.TOP,
                                  expand=tkinter.YES,
                                  fill=tkinter.X)
text_output = tkinter.Text(frame_output, width=WIDTH, state=tkinter.DISABLED)
text_output.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
text_output.bind('<1>', lambda event: text_output.focus_set())

# for operations
tkinter.Button(frame_ops,
               text='input to set 1',
               height=HEIGHT,
               width=HALF_WIDTH,
               command=lambda t=1: func_input(t)).pack(side=tkinter.TOP,
                                                       expand=tkinter.YES,
                                                       fill=tkinter.BOTH)
tkinter.Button(frame_ops,
               text='input to set 2',
               height=HEIGHT,
               width=HALF_WIDTH,
               command=lambda t=2: func_input(t)).pack(side=tkinter.TOP,
                                                       expand=tkinter.YES,
                                                       fill=tkinter.BOTH)
tkinter.Button(frame_ops,
               text='switch',
               height=HEIGHT,
               width=HALF_WIDTH,
               command=func_switch).pack(side=tkinter.TOP,
                                         expand=tkinter.YES,
                                         fill=tkinter.BOTH)
tkinter.Button(
    frame_ops,
    text='union',
    height=HEIGHT,
    width=HALF_WIDTH,
    command=lambda func=(lambda a, b: a.union(b)): func_apply(func)).pack(
        side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
tkinter.Button(
    frame_ops,
    text='difference',
    height=HEIGHT,
    width=HALF_WIDTH,
    command=lambda func=(lambda a, b: a.difference(b)): func_apply(func)).pack(
        side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
tkinter.Button(frame_ops,
               text='intersection',
               height=HEIGHT,
               width=HALF_WIDTH,
               command=lambda func=(lambda a, b: a.intersection(b)): func_apply(
                   func)).pack(side=tkinter.TOP,
                               expand=tkinter.YES,
                               fill=tkinter.BOTH)

# pack all
frame_input.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
frame_display.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
frame_output.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
frame_ops.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.mainloop()
