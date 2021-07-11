import tkinter

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
        tuple(r for r in widgets['src_text'].get('1.0', tkinter.END).split('\n')
              if bool(r))
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


def func_strip():
    if bool(history):
        history.append(tuple(h.strip() for h in history[-1]))
        update_text()


def func_remove_duplicate():
    if bool(history):
        history.append(sorted(set(history[-1]), key=history[-1].index))
        update_text()


def func_neighboring_duplicate():
    if bool(history):
        history.append((history[-1][0],) + tuple(
            el for i, el in enumerate(history[-1][1:]) if el != history[-1][i]))
        update_text()


def func_upper():
    if bool(history):
        history.append(tuple(h.upper() for h in history[-1]))
        update_text()


def func_lower():
    if bool(history):
        history.append(tuple(h.lower() for h in history[-1]))
        update_text()


def func_dec2hex():
    if bool(history):
        history.append(tuple(hex(int(h))[2:] for h in history[-1]))
        update_text()


def func_hex2dec():
    if bool(history):
        history.append(tuple(str(int(h, base=16)) for h in history[-1]))
        update_text()


def func_ascii2hex():
    if bool(history):
        history.append(
            tuple(''.join([hex(ord(c))[2:] for c in h]) for h in history[-1]))
        update_text()


def func_hex2ascii():
    if bool(history):
        history.append(
            tuple(''.join([
                chr(int(h[i:min(len(h), i + 2)], base=16))
                for i in range(0, len(h), 2)
            ])
                  for h in history[-1]))
        update_text()


def func_zero_padding_left():
    if bool(history):
        history.append(
            tuple(h if len(h) % 2 == 0 else '0' + h for h in history[-1]))
        update_text()


def func_zero_padding_right():
    if bool(history):
        history.append(
            tuple(h if len(h) % 2 == 0 else h + '0' for h in history[-1]))
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
    frame_button, height=3, text='strip', command=func_strip).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='unique', command=func_remove_duplicate).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button,
    height=3,
    text='transitions',
    command=func_neighboring_duplicate).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='upper', command=func_upper).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='lower', command=func_lower).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='dec2hex', command=func_dec2hex).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='hex2dec', command=func_hex2dec).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='hex2ascii', command=func_hex2ascii).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='ascii2hex', command=func_ascii2hex).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='0*', command=func_zero_padding_left).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)
tkinter.Button(
    frame_button, height=3, text='*0', command=func_zero_padding_right).pack(
        side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)

frame_texts.pack(expand=tkinter.YES, fill=tkinter.BOTH)
frame_button.pack(expand=tkinter.YES, fill=tkinter.X)

tkinter.mainloop()
