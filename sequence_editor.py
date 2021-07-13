import tkinter

import src.sequence_editor as lib

root = tkinter.Tk()
root.title('SequenceHandler')
widgets = dict()
history = []


def prepare_text(name: str):
    # to initialize a text widget
    assert all(not widget.startswith(name + '_') for widget in widgets)
    name_text = name + '_text'
    widgets[name_text] = tkinter.Text(frame_texts, height=50, width=80)
    widgets[name_text].pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
    # config for difference
    widgets[name_text].tag_configure(
        'diff', foreground='red', background='yellow')
    widgets[name_text].tag_configure(
        'should-partial', foreground='black', background='yellow')


def update_text():
    if bool(history):
        widgets['updated_text'].delete('1.0', tkinter.END)
        widgets['updated_text'].insert(tkinter.END, '\n'.join(history[-1]))


def func_reset():
    global history
    history = [
        tuple(
            r for r in widgets['src_text'].get('1.0', tkinter.END).split('\n'))
    ]
    update_text()


def func_clear():
    widgets['src_text'].delete('1.0', tkinter.END)
    func_reset()


def func_back():
    global history
    if len(history) > 1:
        del history[-1]
        update_text()


def func_callback(callback):
    if bool(history):
        history.append(callback(history[-1]))
        update_text()


frame_texts = tkinter.Frame(root)
frame_button = tkinter.Frame(root)

prepare_text('src')
prepare_text('updated')

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
