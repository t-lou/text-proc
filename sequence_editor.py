import tkinter

import src.sequence_editor as lib

root = tkinter.Tk()
root.title('SequenceEditor')
history = []
TEXT_HEIGHT = 50
TEXT_WIDTH = 80


def get_items(widget) -> tuple:
    return tuple(widget.get('1.0', tkinter.END).split('\n'))


def update_text():
    if bool(history):
        text_updated.delete('1.0', tkinter.END)
        text_updated.insert(tkinter.END, '\n'.join(history[-1]))


def func_reset():
    global history
    history = [get_items(text_src)]
    update_text()


def func_clear():
    text_src.delete('1.0', tkinter.END)
    func_reset()


def func_back():
    global history
    if len(history) > 1:
        del history[-1]
        update_text()


def func_callback(callback):
    if bool(history):
        current = get_items(text_updated)
        if current != history[-1]:
            history.append(current)
        history.append(callback(history[-1]))
        update_text()


frame_texts = tkinter.Frame(root)
frame_button = tkinter.Frame(root)

text_src = tkinter.Text(frame_texts, height=TEXT_HEIGHT, width=TEXT_WIDTH)
text_src.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
text_updated = tkinter.Text(frame_texts, height=TEXT_HEIGHT, width=TEXT_WIDTH)
text_updated.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.Button(
    frame_button, height=3, text='reset', command=func_reset).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='clear', command=func_clear).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='back', command=func_back).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='strip',
    command=lambda cb=lib.handler_strip: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='unique',
    command=lambda cb=lib.handler_remove_duplicate: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='transitions',
    command=lambda cb=lib.handler_neighboring_duplicate: func_callback(cb)
).pack(
    side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='upper',
    command=lambda cb=lib.handler_upper: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='lower',
    command=lambda cb=lib.handler_lower: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='rev',
    command=lambda cb=lib.handler_reverse: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='nonempty',
    command=lambda cb=lib.handler_nonempty: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='dec2hex',
    command=lambda cb=lib.handler_dec2hex: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='hex2dec',
    command=lambda cb=lib.handler_hex2dec: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='hex2ascii',
    command=lambda cb=lib.handler_hex2ascii: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='ascii2hex',
    command=lambda cb=lib.handler_ascii2hex: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='0*',
    command=lambda cb=lib.handler_zero_padding_left: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='*0',
    command=lambda cb=lib.handler_zero_padding_right: func_callback(cb)).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)

frame_texts.pack(expand=tkinter.YES, fill=tkinter.BOTH)
frame_button.pack(expand=tkinter.YES, fill=tkinter.X)

tkinter.mainloop()
