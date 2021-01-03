import tkinter
import difflib

root = tkinter.Tk()
root.title('TextDiff')
widgets = dict()

line_text = 'line_text'
widgets[line_text] = tkinter.Text(root, height=50, width=4)
widgets[line_text].pack(side=tkinter.LEFT, fill=tkinter.Y)


def scroll(*args):
    # for scrolling at the same time
    for widget in widgets:
        if widget.endswith('_text'):
            widgets[widget].yview(*args)


def prepare_text(name: str):
    # to initialize a text widget
    assert all(not widget.startswith(name + '_') for widget in widgets)
    name_text = name + '_text'
    widgets[name_text] = tkinter.Text(root, height=50, width=80)
    widgets[name_text].pack(side=tkinter.LEFT, fill=tkinter.Y)
    # config for difference
    widgets[name_text].tag_configure('diff',
                                     foreground='red',
                                     background='yellow')


prepare_text('part1')
prepare_text('part2')

widgets['scrollbar'] = tkinter.Scrollbar(root,
                                         orient=tkinter.VERTICAL,
                                         command=scroll)
widgets['scrollbar'].pack(side=tkinter.RIGHT, fill=tkinter.Y)
for widget in widgets:
    if widget.endswith('_text'):
        widgets[widget].config(yscrollcommand=widgets['scrollbar'].set)


def collect_lines(name: str) -> tuple:
    '''
    Gets the lines and return to lists.
    The empty lines are skipped.

    Arguments:
        name: name of the widget to collect text from.
    Returns:
        An array of lines.
    '''
    lines = str(widgets[name + '_text'].get('1.0', tkinter.END)).split('\n')
    widgets[name + '_text'].delete('1.0', tkinter.END)
    lines = tuple(line for line in lines if bool(line))
    return lines


def find_match(differences: list, index: int) -> int:
    '''
    Find the match for one change of line.

    Arguments:
        differences: the difference from difflib.
        index: the current index.
    Returns:
        If the line is changed, it returns the corresponding line of the change; if the line is deleted, -1 is returned.
    '''
    assert differences[index][
        0] == '-', 'line should be available in first part'
    for i in range(index + 1, len(differences)):
        if differences[i][0] == '?':
            continue
        elif differences[i][0] == '+':
            return i
        else:
            break
    return -1


def parse_line_index(difference: str) -> list:
    '''
    With the difference hints from difflib, return the ranges for highlighting.

    Arguments:
        difference: the indicator for the difference.
    Returns:
        A list of start-end index.
    '''
    last_index = -1
    ranges = []
    target = '^'
    for i, d in enumerate(difference[:-1]):
        if last_index < 0 and d == target:
            last_index = i
        elif last_index >= 0 and d != target:
            ranges.append((last_index, i))
            last_index = -1
    if last_index >= 0:
        ranges.append((last_index, len(difference) - 1))  # last char is \n
    return ranges


def exec(_):
    lines1 = collect_lines('part1')
    lines2 = collect_lines('part2')
    widgets['line_text'].delete('1.0', tkinter.END)
    differences = tuple(difflib.Differ().compare(lines1, lines2))
    line_total = 0
    next_index = -1
    for index, difference in enumerate(differences):
        if next_index > 0 and index < next_index:
            # skip the parts which are proceeded
            continue
        if difference[0] == ' ':
            # shared part
            line_total += 1
            widgets['part1_text'].insert(tkinter.END, difference[2:] + '\n')
            widgets['part2_text'].insert(tkinter.END, difference[2:] + '\n')
        elif difference[0] == '+':
            # only in part2
            line_total += 1
            widgets['part1_text'].insert(tkinter.END, '\n', 'diff')
            widgets['part2_text'].insert(tkinter.END, difference[2:] + '\n',
                                         'diff')
        elif difference[0] == '-':
            id_match = find_match(differences, index)
            line_total += 1
            if id_match > 0:
                # this line is changed
                widgets['part1_text'].insert(tkinter.END,
                                             difference[2:] + '\n')
                widgets['part2_text'].insert(tkinter.END,
                                             differences[id_match][2:] + '\n')
                for r in parse_line_index(differences[index + 1][2:]):
                    widgets['part1_text'].tag_add('diff',
                                                  f'{line_total}.{r[0]}',
                                                  f'{line_total}.{r[1]}')
                for r in parse_line_index(differences[id_match + 1][2:]):
                    widgets['part2_text'].tag_add('diff',
                                                  f'{line_total}.{r[0]}',
                                                  f'{line_total}.{r[1]}')
                next_index = id_match + 1
            else:
                # not match but starts with '-', part1 only
                widgets['part1_text'].insert(tkinter.END,
                                             difference[2:] + '\n', 'diff')
                widgets['part2_text'].insert(tkinter.END, '\n', 'diff')
        # implicit: difference is '? *', they should be skipped due to part of "line is changed" condition
    widgets['line_text'].insert(
        tkinter.END,
        '\n'.join(tuple('{:4}'.format(i) for i in range(1, line_total + 1))))


root.bind('<Return>', exec)

# # TODO for testing
# widgets['part1_text'].insert(
#     tkinter.END, '\n'.join(
#         ('hello', '1part11-is-changed1', 'belongs-1-to', 'world', 'you')))
# widgets['part2_text'].insert(
#     tkinter.END, '\n'.join(
#         ('you', 'hello', '2part2-is-changed2', 'belongs-2-to', 'world')))

tkinter.mainloop()
