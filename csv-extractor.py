import tkinter
import tkinter.ttk
import tkinter.filedialog
import csv
import sys

gHasPandas = False
try:
    import pandas
    import collections
    gHasPandas = True
except:
    pass

kWidthButton = 40
kHeightButton = 3
kWidthText = 100

gData = {}

kEncoding = 'latin-1' if sys.platform == 'win32' else 'utf-8'


def parse_items(text: str) -> tuple:
    elems = tuple(i.strip() for i in text.replace('\n', ',').strip().split(',')
                  if bool(i.strip()))
    return tuple(sorted(set(elems), key=elems.index))


def get_output_fields() -> tuple:
    assert 'fieldnames' in gData, 'fieldnames not found in data, nonsense'
    column_out = parse_items(text_out_column.get('1.0', tkinter.END))
    if not bool(column_out):
        column_out = gData['fieldnames']
    return column_out


def func_input():
    text_summary_target.config(state='normal')
    text_summary_target.delete('1.0', tkinter.END)

    gData['target'] = parse_items(text_target.get('1.0', tkinter.END))

    text_summary_target.insert(tkinter.END,
                               f'#targets = {len(gData["target"])}')
    text_summary_target.config(state='disabled')

    text_target.delete('1.0', tkinter.END)
    text_target.insert(tkinter.END, ', '.join(gData['target']))


def func_open():
    text_summary_csv.config(state='normal')
    text_summary_csv.delete('1.0', tkinter.END)

    filetypes = [('CSV', '.csv'),
                 ('XLSX', '.xlsx')] if gHasPandas else [('CSV', '.csv')]
    filename = tkinter.filedialog.askopenfilename(filetypes=filetypes)
    if bool(filename):
        if filename.endswith('.csv'):
            with open(filename, 'r', encoding=kEncoding) as fi:
                reader = csv.DictReader(fi)
                gData['table'] = tuple(row for row in reader)
                gData['fieldnames'] = tuple(reader.fieldnames)
        else:
            xlsx_data = pandas.read_excel(filename)
            gData['table'] = tuple(
                collections.OrderedDict({
                    attr: row[i_attr]
                    for i_attr, attr in enumerate(xlsx_data.keys())
                }) for row in xlsx_data.astype(str).values.tolist())
            gData['fieldnames'] = tuple(xlsx_data.keys())

        text_summary_csv.insert(
            tkinter.END,
            f'#rows = {len(gData["table"])}\n{",".join(gData["fieldnames"])}')

    text_summary_csv.config(state='disabled')


def func_extract(in_table_order: bool):
    text_summary_match.config(state='normal')
    text_summary_match.delete('1.0', tkinter.END)
    text_output.delete('1.0', tkinter.END)

    column_in = text_in_column.get('1.0', tkinter.END).strip()
    column_out = get_output_fields()
    check = {
        'table valid': ('table' in gData),
        'column valid': (bool(column_in)),
        'column found': ('table' in gData
                         and all(column_in in row for row in gData['table'])),
        'target valid': ('target' in gData and bool(gData['target'])),
        'output valid': (not bool(column_out)
                         or all(c in gData['fieldnames'] for c in column_out))
    }
    if all(check.values()):
        if in_table_order:
            gData['selected'] = tuple(row for row in gData['table']
                                      if row[column_in] in gData['target'])
        else:
            selected = [[
                row for row in gData['table'] if row[column_in] in (target, )
            ] for target in gData['target']]
            gData['selected'] = tuple(elem for row in selected for elem in row)

        text_summary_match.insert(tkinter.END,
                                  f'#match = {len(gData["selected"])}')
        text_output.insert(
            tkinter.END, '\n'.join(','.join(row[f] for f in column_out)
                                   for row in gData['selected']))
    else:
        text_summary_match.insert(
            tkinter.END,
            f'problem in {", ".join(k for k in check if not check[k])}')

    text_summary_match.config(state='disabled')


def func_save():
    column_out = get_output_fields()
    check = {
        'table valid': ('selected' in gData),
        'output valid': (not bool(column_out)
                         or all(c in gData['fieldnames'] for c in column_out))
    }
    if all(check.values()):
        filename = tkinter.filedialog.asksaveasfilename()
        if bool(filename):
            filename = filename if filename.endswith(
                '.csv') else filename + '.csv'
        with open(filename, 'w', newline='', encoding=kEncoding) as fs:
            writer = csv.DictWriter(fs, fieldnames=column_out)
            writer.writeheader()
            for row in gData['selected']:
                writer.writerow({f: row[f] for f in column_out})


root = tkinter.Tk()
root.title('csv-extractor')

frame_widget = tkinter.Frame(root)

tkinter.Label(frame_widget, text='input column').pack(side=tkinter.TOP)
text_in_column = tkinter.Text(frame_widget, width=kHeightButton, height=2)
text_in_column.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.Label(frame_widget, text='output columns').pack(side=tkinter.TOP)
text_out_column = tkinter.Text(frame_widget, width=kHeightButton, height=2)
text_out_column.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.Button(frame_widget,
               height=kHeightButton,
               width=kWidthButton,
               text='input targets',
               command=func_input).pack(side=tkinter.TOP,
                                        expand=tkinter.YES,
                                        fill=tkinter.BOTH)

tkinter.Button(frame_widget,
               height=kHeightButton,
               width=kWidthButton,
               text='open',
               command=func_open).pack(side=tkinter.TOP,
                                       expand=tkinter.YES,
                                       fill=tkinter.BOTH)

tkinter.Button(frame_widget,
               height=kHeightButton,
               width=kWidthButton,
               text='extract in table order',
               command=lambda x=True: func_extract(x)).pack(side=tkinter.TOP,
                                                            expand=tkinter.YES,
                                                            fill=tkinter.BOTH)

tkinter.Button(frame_widget,
               height=kHeightButton,
               width=kWidthButton,
               text='extract in target order',
               command=lambda x=False: func_extract(x)).pack(
                   side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.Button(frame_widget,
               height=kHeightButton,
               width=kWidthButton,
               text='save',
               command=func_save).pack(side=tkinter.TOP,
                                       expand=tkinter.YES,
                                       fill=tkinter.BOTH)

tkinter.Label(frame_widget, text='summary target').pack(side=tkinter.TOP)
text_summary_target = tkinter.Text(frame_widget,
                                   width=kHeightButton,
                                   height=2,
                                   state=tkinter.DISABLED)
text_summary_target.pack(side=tkinter.TOP,
                         expand=tkinter.YES,
                         fill=tkinter.BOTH)

tkinter.Label(frame_widget, text='summary csv').pack(side=tkinter.TOP)
text_summary_csv = tkinter.Text(frame_widget,
                                width=kHeightButton,
                                height=2,
                                state=tkinter.DISABLED)
text_summary_csv.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
text_summary_csv.bind('<1>', lambda event: text_summary_csv.focus_set())

tkinter.Label(frame_widget, text='summary match').pack(side=tkinter.TOP)
text_summary_match = tkinter.Text(frame_widget,
                                  width=kHeightButton,
                                  height=2,
                                  state=tkinter.DISABLED)
text_summary_match.pack(side=tkinter.TOP,
                        expand=tkinter.YES,
                        fill=tkinter.BOTH)

frame_widget.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

frame_text = tkinter.Frame(root)

tkinter.Label(frame_text, text='targets').pack(side=tkinter.TOP)
text_target = tkinter.Text(frame_text, width=kWidthText, height=4)
text_target.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.Label(frame_text, text='extracted').pack(side=tkinter.TOP)
text_output = tkinter.Text(frame_text, width=kWidthText, height=20)
text_output.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

frame_text.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

tkinter.mainloop()
