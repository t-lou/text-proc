import tkinter
import tkinter.filedialog
import json

import src.sequence_editor as lib

root = tkinter.Tk()
root.title('SequenceEditor')
history = []
TEXT_HEIGHT = 50
TEXT_WIDTH = 80

S_RESET = 'reset'
S_CLEAR = 'clear'
S_BACK = 'back'
S_STRIP = 'strip'
S_UNIQUE = 'unique'
S_TRANSITION = 'transition'
S_UPPER = 'upper'
S_LOWER = 'lower'
S_REV = 'rev'
S_NONEMPTY = 'nonempty'
S_DEC2HEX = 'dec2hex'
S_HEX2DEC = 'hex2dec'
S_HEX2ASCII = 'hex2ascii'
S_ASCII2HEX = 'ascii2hex'
S_ZERO_LEFT = '0*'
S_ZERO_RIGHT = '*0'


def get_items(widget, separator: str) -> tuple:
    return tuple(widget.get('1.0', tkinter.END).strip().split(separator))


def update_text():
    if bool(history):
        text_updated.delete('1.0', tkinter.END)
        text_updated.insert(tkinter.END, '\n'.join(history[-1]))


def func_reset():
    global history
    history = [get_items(text_src, '\n')]
    text_history.delete('1.0', tkinter.END)
    text_history.insert(tkinter.END, S_RESET)
    update_text()


def func_clear():
    text_src.delete('1.0', tkinter.END)
    text_history.delete('1.0', tkinter.END)
    func_reset()


def func_back():
    global history
    if len(history) > 1:
        del history[-1]
        past = get_items(text_history, ',')
        text_history.delete('1.0', tkinter.END)
        text_history.insert(tkinter.END, ','.join(past[:-1]))
        update_text()


def func_callback(name: str):
    if bool(history):
        past = get_items(text_history, ',')
        text_history.delete('1.0', tkinter.END)

        current = get_items(text_updated, '\n')

        if current != history[-1]:
            past += ('EDITED',)

            history.append(current)

        history.append(INFO_BUTTONS_HANDLER[name](history[-1]))

        past += (name,)
        text_history.insert(tkinter.END, ','.join(past))

        update_text()


def func_history_execute():
    past = get_items(text_history, ',')
    if bool(past) and all(
            step in INFO_BUTTONS_HANDLER or step in INFO_BUTTONS_MANAGEMENT
            for step in past):
        for step in past:
            if step in INFO_BUTTONS_MANAGEMENT:
                INFO_BUTTONS_MANAGEMENT[step]()
            elif step in INFO_BUTTONS_HANDLER:
                func_callback(step)


def func_history_load():
    filename = tkinter.filedialog.askopenfilename(initialdir='.',
                                                  filetypes=(('json',
                                                              '*.json'),))
    if bool(filename):
        with open(filename) as fs:
            past = json.loads(fs.read())
            if bool(past) and all(step in INFO_BUTTONS_HANDLER or
                                  step in INFO_BUTTONS_MANAGEMENT
                                  for step in past):
                text_history.delete('1.0', tkinter.END)
                text_history.insert(tkinter.END, ','.join(past))


def func_history_save():
    past = get_items(text_history, ',')
    if bool(past) and all(
            step in INFO_BUTTONS_HANDLER or step in INFO_BUTTONS_MANAGEMENT
            for step in past):
        filename = tkinter.filedialog.asksaveasfilename(initialdir='.',
                                                        filetypes=(('json',
                                                                    '*.json'),))
        if bool(filename):
            str_log = json.dumps(past, indent=' ')
            with open(filename, 'w') as fs:
                fs.write(str_log)


INFO_BUTTONS_MANAGEMENT = {
    S_RESET: func_reset,
    S_CLEAR: func_clear,
    S_BACK: func_back,
}

INFO_BUTTONS_HANDLER = {
    S_STRIP: lib.handler_strip,
    S_UNIQUE: lib.handler_remove_duplicate,
    S_TRANSITION: lib.handler_neighboring_duplicate,
    S_UPPER: lib.handler_upper,
    S_LOWER: lib.handler_lower,
    S_REV: lib.handler_reverse,
    S_NONEMPTY: lib.handler_nonempty,
    S_DEC2HEX: lib.handler_dec2hex,
    S_HEX2DEC: lib.handler_hex2dec,
    S_HEX2ASCII: lib.handler_hex2ascii,
    S_ASCII2HEX: lib.handler_ascii2hex,
    S_ZERO_LEFT: lib.handler_zero_padding_left,
    S_ZERO_RIGHT: lib.handler_zero_padding_right,
}

frame_button = tkinter.Frame(root)
frame_history = tkinter.Frame(root)
frame_texts = tkinter.Frame(root)

text_src = tkinter.Text(frame_texts, height=TEXT_HEIGHT, width=TEXT_WIDTH)
text_src.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
text_updated = tkinter.Text(frame_texts, height=TEXT_HEIGHT, width=TEXT_WIDTH)
text_updated.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

for text, callback in INFO_BUTTONS_MANAGEMENT.items():
    tkinter.Button(frame_button, height=3, text=text,
                   command=callback).pack(side=tkinter.LEFT,
                                          expand=tkinter.YES,
                                          fill=tkinter.X)

for text in INFO_BUTTONS_HANDLER:
    tkinter.Button(frame_button,
                   height=3,
                   text=text,
                   command=lambda name=text: func_callback(name)).pack(
                       side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.X)

text_history = tkinter.Text(frame_history, height=2, width=TEXT_WIDTH)
text_history.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
tkinter.Button(frame_history, text='execute',
               command=func_history_execute).pack(side=tkinter.LEFT,
                                                  expand=tkinter.YES,
                                                  fill=tkinter.BOTH)
tkinter.Button(frame_history, text='load',
               command=func_history_load).pack(side=tkinter.LEFT,
                                               expand=tkinter.YES,
                                               fill=tkinter.BOTH)
tkinter.Button(frame_history, text='save',
               command=func_history_save).pack(side=tkinter.LEFT,
                                               expand=tkinter.YES,
                                               fill=tkinter.BOTH)

frame_button.pack(expand=tkinter.YES, fill=tkinter.X)
frame_history.pack(expand=tkinter.YES, fill=tkinter.X)
frame_texts.pack(expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.mainloop()
