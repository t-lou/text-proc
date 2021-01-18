import tkinter
import tkinter.ttk
import json
import os

gWidgets = None
kWidth = 20
kHeight = 3
kFilenameConfig = 'text_filter_config.json'
kKeyFilter = 'filters'


class Config(object):
    def __init__(self):
        self._config = json.loads(open(
            kFilenameConfig).read()) if os.path.isfile(kFilenameConfig) else {
                kKeyFilter: {}
            }

    def is_filter_valid(self):
        return bool(self._config) and kKeyFilter in self._config and type(
            self._config) == dict

    def get_names(self) -> tuple:
        if self.is_filter_valid():
            return tuple(self._config[kKeyFilter].keys())
        else:
            return tuple()

    def get_filter_text(self, name: str) -> str:
        if self.is_filter_valid() and name in self._config[kKeyFilter]:
            return self._config[kKeyFilter][name]
        else:
            return None

    def add_filter(self, name: str, text: str):
        assert self.is_filter_valid(), 'invalid config'
        if kKeyFilter not in self._config:
            self._config[kKeyFilter] = {}
        self._config[kKeyFilter][name] = text

    def remove_filter(self, name: str):
        assert self.is_filter_valid() and name in self._config[kKeyFilter], \
            f'filter {name} not found'
        self._config[kKeyFilter].pop(name)

    def save(self):
        open(kFilenameConfig, 'w').write(json.dumps(self._config, indent=' '))


def filter(_):
    gWidgets['text_out'].config(state='normal')
    gWidgets['text_out'].delete('1.0', tkinter.END)
    selected = set(gWidgets['filter_match'][gWidgets['listbox_filters'].get(i)]
                   for i in gWidgets['listbox_filters'].curselection())
    filter_custom = gWidgets['filter_custom'].get('1.0', tkinter.END).strip()
    if bool(filter_custom):
        selected.add(filter_custom)
    for line in gWidgets['text_in'].get('1.0', tkinter.END).split('\n'):
        if not bool(selected) or any(p in line for p in selected):
            gWidgets['text_out'].insert(tkinter.END, line + '\n')
    gWidgets['text_out'].config(state='disabled')


def add_filter():
    name = gWidgets['text_filter_name'].get('1.0', tkinter.END).strip()
    text = gWidgets['text_filter_text'].get('1.0', tkinter.END).strip()
    gWidgets['config'].add_filter(name, text)
    gWidgets['config'].save()
    init_gui()


def remove_filter():
    name = gWidgets['text_filter_name'].get('1.0', tkinter.END).strip()
    gWidgets['config'].remove_filter(name)
    gWidgets['config'].save()
    init_gui()


def init_gui():
    global gWidgets
    text_in = None
    # destroy and reinit if it is created
    if bool(gWidgets) and 'root' in gWidgets:
        text_in = gWidgets['text_in'].get('1.0', tkinter.END)
        gWidgets['root'].destroy()
    gWidgets = {'root': tkinter.Tk(), 'config': Config()}
    gWidgets['root'].title('TextFilter')

    tab_container = tkinter.ttk.Notebook(gWidgets['root'])

    # main tab for input text
    frame_original = tkinter.Frame(tab_container)
    gWidgets['text_in'] = tkinter.Text(frame_original)
    gWidgets['text_in'].pack(expand=tkinter.YES, fill=tkinter.BOTH)
    if text_in is not None:
        gWidgets['text_in'].insert(tkinter.END, text_in)
    tab_container.add(frame_original, text='original')

    # main tab for output text
    frame_filtered = tkinter.Frame(tab_container)
    frame_filtered_filter = tkinter.Frame(frame_filtered)
    tkinter.Button(frame_filtered_filter,
                   height=kHeight,
                   width=kWidth,
                   text='update',
                   command=lambda: filter(None)).pack(side=tkinter.TOP)
    gWidgets['listbox_filters'] = tkinter.Listbox(frame_filtered_filter,
                                                  width=kWidth,
                                                  selectmode=tkinter.MULTIPLE)
    gWidgets['filter_match'] = {}
    for name in gWidgets['config'].get_names():
        text = f'{name}: {gWidgets["config"].get_filter_text(name)}'
        gWidgets['listbox_filters'].insert(tkinter.END, text)
        gWidgets['filter_match'][text] = gWidgets['config'].get_filter_text(
            name)
    gWidgets['filter_custom'] = tkinter.Text(frame_filtered_filter,
                                             height=kHeight,
                                             width=kWidth)
    gWidgets['listbox_filters'].bind('<<ListboxSelect>>', filter)
    gWidgets['listbox_filters'].pack(side=tkinter.TOP)
    tkinter.Label(frame_filtered_filter, text='custom').pack()
    gWidgets['filter_custom'].pack(side=tkinter.TOP)
    frame_filtered_filter.pack(side=tkinter.LEFT)
    frame_filtered_output = tkinter.Frame(frame_filtered)
    gWidgets['text_out'] = tkinter.Text(frame_filtered, state=tkinter.DISABLED)
    gWidgets['text_out'].bind('<1>',
                              lambda event: gWidgets['text_out'].focus_set())
    gWidgets['text_out'].pack(expand=tkinter.YES, fill=tkinter.BOTH)
    frame_filtered_output.pack(side=tkinter.LEFT,
                               expand=tkinter.YES,
                               fill=tkinter.BOTH)
    tab_container.add(frame_filtered, text='filtered')

    # main tab for editing filters
    frame_filter_handler = tkinter.Frame(tab_container)
    gWidgets['text_filter_name'] = tkinter.Text(frame_filter_handler,
                                                height=kHeight,
                                                width=kWidth)
    gWidgets['text_filter_text'] = tkinter.Text(frame_filter_handler,
                                                height=kHeight,
                                                width=kWidth)
    tkinter.Label(frame_filter_handler, text='name').pack()
    gWidgets['text_filter_name'].pack(side=tkinter.TOP)
    tkinter.Label(frame_filter_handler, text='text').pack()
    gWidgets['text_filter_text'].pack(side=tkinter.TOP)
    tkinter.Button(frame_filter_handler,
                   height=kHeight,
                   width=kWidth,
                   text='add',
                   command=add_filter).pack(side=tkinter.TOP)
    tkinter.Button(frame_filter_handler,
                   height=kHeight,
                   width=kWidth,
                   text='remove',
                   command=remove_filter).pack(side=tkinter.TOP)
    tab_container.add(frame_filter_handler, text='filters')

    tab_container.pack(expand=tkinter.YES, fill=tkinter.BOTH)


if __name__ == '__main__':
    # # TODO for test
    # open(kFilenameConfig, 'w').write(
    #     json.dumps(
    #         {
    #             kKeyFilter:
    #             {f'has_{c}': c
    #              for c in 'abcdefghijklmnopgrqtuvwxyz'}
    #         },
    #         indent=' '))
    init_gui()
    # # TODO for test
    # gWidgets['text_in'].insert(
    #     tkinter.END, '\n'.join(
    #         ('abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi')))
    tkinter.mainloop()
