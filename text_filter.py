import tkinter
import tkinter.filedialog
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


def filter():
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


def load_text():
    filename = tkinter.filedialog.askopenfilename()
    if bool(filename):
        gWidgets['text_in'].delete('1.0', tkinter.END)
        with open(filename, 'r') as fs:
            gWidgets['text_in'].insert(tkinter.END, fs.read())


def save_text():
    filename = tkinter.filedialog.asksaveasfilename()
    if bool(filename):
        with open(filename, 'w') as fs:
            fs.write(gWidgets['text_out'].get('1.0', tkinter.END))


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

    frame_filter_related = tkinter.Frame(gWidgets['root'])
    # for selecting filters
    frame_filtering = tkinter.Frame(frame_filter_related)
    tkinter.Label(frame_filtering, text='filters\n').pack(side=tkinter.TOP)
    tkinter.Button(frame_filtering,
                   height=kHeight,
                   width=kWidth,
                   text='update',
                   command=filter).pack(side=tkinter.TOP)
    gWidgets['listbox_filters'] = tkinter.Listbox(frame_filtering,
                                                  width=kWidth,
                                                  selectmode=tkinter.MULTIPLE)
    gWidgets['filter_match'] = {}
    for name in gWidgets['config'].get_names():
        text = f'{name}: {gWidgets["config"].get_filter_text(name)}'
        gWidgets['listbox_filters'].insert(tkinter.END, text)
        gWidgets['filter_match'][text] = gWidgets['config'].get_filter_text(
            name)
    gWidgets['filter_custom'] = tkinter.Text(frame_filtering,
                                             height=kHeight,
                                             width=kWidth)
    gWidgets['listbox_filters'].bind('<<ListboxSelect>>', filter)
    gWidgets['listbox_filters'].pack(side=tkinter.TOP)
    tkinter.Label(frame_filtering, text='custom').pack()
    gWidgets['filter_custom'].pack(side=tkinter.TOP)

    tkinter.Button(frame_filtering,
                   height=kHeight,
                   width=kWidth,
                   text='load text',
                   command=load_text).pack(side=tkinter.TOP)

    tkinter.Button(frame_filtering,
                   height=kHeight,
                   width=kWidth,
                   text='save text',
                   command=save_text).pack(side=tkinter.TOP)

    frame_filtering.pack(side=tkinter.TOP)

    tkinter.Label(frame_filter_related, text='\n' * 3).pack(side=tkinter.TOP)

    # for editing filters
    frame_filter_config = tkinter.Frame(frame_filter_related)
    tkinter.Label(frame_filter_config,
                  text='filter config\n').pack(side=tkinter.TOP)
    gWidgets['text_filter_name'] = tkinter.Text(frame_filter_config,
                                                height=kHeight,
                                                width=kWidth)
    gWidgets['text_filter_text'] = tkinter.Text(frame_filter_config,
                                                height=kHeight,
                                                width=kWidth)
    tkinter.Label(frame_filter_config, text='name').pack()
    gWidgets['text_filter_name'].pack(side=tkinter.TOP)
    tkinter.Label(frame_filter_config, text='text').pack()
    gWidgets['text_filter_text'].pack(side=tkinter.TOP)
    tkinter.Button(frame_filter_config,
                   height=kHeight,
                   width=kWidth,
                   text='add',
                   command=add_filter).pack(side=tkinter.TOP)
    tkinter.Button(frame_filter_config,
                   height=kHeight,
                   width=kWidth,
                   text='remove',
                   command=remove_filter).pack(side=tkinter.TOP)
    frame_filter_config.pack(side=tkinter.TOP)
    frame_filter_related.pack(side=tkinter.LEFT)

    gWidgets['text_in'] = tkinter.Text(gWidgets['root'], height=60, width=80)
    gWidgets['text_in'].pack(side=tkinter.LEFT,
                             expand=tkinter.YES,
                             fill=tkinter.BOTH)
    if text_in is not None:
        gWidgets['text_in'].insert(tkinter.END, text_in)

    gWidgets['text_out'] = tkinter.Text(gWidgets['root'],
                                        height=60,
                                        width=80,
                                        state=tkinter.DISABLED)
    gWidgets['text_out'].bind('<1>',
                              lambda event: gWidgets['text_out'].focus_set())
    gWidgets['text_out'].pack(side=tkinter.LEFT,
                              expand=tkinter.YES,
                              fill=tkinter.BOTH)


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
