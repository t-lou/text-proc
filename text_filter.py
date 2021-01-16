import tkinter
import tkinter.ttk
import json
import os

gWidgets = None
kWidth = 20
kHeight = 5
gConfig = None


class Config(object):
    def __init__(self):
        self._config_fn = 'text_filter_config.json'
        self._config = json.loads(open(
            self._config_fn).read()) if os.path.isfile(
                self._config_fn) else {}
        self._name_filters = 'filters'

    def is_filter_valid(self):
        return bool(
            self._config) and self._name_filters in self._config and bool(
                self._config[self._name_filters])

    def get_names(self) -> tuple:
        if self.is_filter_valid():
            return tuple(self._config[self._name_filters].keys())
        else:
            return tuple()

    def get_filter_text(self, name: str) -> str:
        if self.is_filter_valid() and name in self._config[self._name_filters]:
            return self._config[self._name_filters][name]
        else:
            return None


def filter(text: str):
    gWidgets['text_out'].config(state='normal')
    gWidgets['text_out'].delete('1.0', tkinter.END)
    for line in gWidgets['text_in'].get('1.0', tkinter.END).split('\n'):
        if text is None or text in line:
            gWidgets['text_out'].insert(tkinter.END, line + '\n')
    gWidgets['text_out'].config(state='disabled')


def init_gui():
    global gWidgets
    gWidgets = {'root': tkinter.Tk()}
    gWidgets['root'].title('TextFilter')

    tab_container = tkinter.ttk.Notebook(gWidgets['root'])

    # main tab for input text
    frame_original = tkinter.Frame(tab_container)
    gWidgets['text_in'] = tkinter.Text(frame_original)
    gWidgets['text_in'].pack(fill=tkinter.BOTH)
    tab_container.add(frame_original, text='original')

    # main tab for output text
    frame_filtered = tkinter.Frame(tab_container)
    frame_filter = tkinter.Frame(frame_filtered)
    tkinter.Button(
        frame_filter,
        text='<>',
        width=kWidth,
        height=kHeight,
        command=lambda text=None: filter(text)).pack(side=tkinter.TOP)
    for name in gConfig.get_names():
        name_w = f'button_filter_{name}'
        tkinter.Button(frame_filter,
                       text=f'{name}:\n{gConfig.get_filter_text(name)}',
                       width=kWidth,
                       height=kHeight,
                       command=lambda text=gConfig.get_filter_text(name):
                       filter(text)).pack(side=tkinter.TOP)
    frame_filter.pack(side=tkinter.LEFT)
    frame_output = tkinter.Frame(frame_filtered)
    gWidgets['text_out'] = tkinter.Text(frame_filtered, state=tkinter.DISABLED)
    gWidgets['text_out'].pack(fill=tkinter.BOTH)
    frame_output.pack(side=tkinter.LEFT)
    tab_container.add(frame_filtered, text='filtered')

    tab_container.pack(side=tkinter.RIGHT, fill=tkinter.Y)


if __name__ == '__main__':
    gConfig = Config()
    init_gui()
    # for test
    gWidgets['text_in'].insert(tkinter.END, '\n'.join(('abc', 'def', 'hgi')))
    tkinter.mainloop()
