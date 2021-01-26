import tkinter
import difflib

root = tkinter.Tk()
root.title('TextDiff')
widgets = dict()


def on_scroll_scrollbar(*args):
    # for scrolling at the same time
    for widget in widgets:
        if widget.endswith('_text'):
            widgets[widget].yview(*args)


def on_scroll_text(*args):
    widgets['scrollbar'].set(*args)
    # https://stackoverflow.com/questions/32038701/python-tkinter-making-two-text-widgets-scrolling-synchronize/35824343
    on_scroll_scrollbar('moveto', args[0])


def prepare_text(name: str):
    # to initialize a text widget
    assert all(not widget.startswith(name + '_') for widget in widgets)
    name_text = name + '_text'
    widgets[name_text] = tkinter.Text(frame_texts, height=50, width=80)
    widgets[name_text].pack(side=tkinter.LEFT,
                            expand=tkinter.YES,
                            fill=tkinter.BOTH)
    # config for difference
    widgets[name_text].tag_configure('diff',
                                     foreground='red',
                                     background='yellow')
    widgets[name_text].tag_configure('should-partial',
                                     foreground='black',
                                     background='yellow')


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
        if last_index < 0 and d != ' ':
            last_index = i
        elif last_index >= 0 and d == ' ':
            ranges.append((last_index, i))
            last_index = -1
    if last_index >= 0:
        ranges.append((last_index, len(difference) - 1))  # last char is \n
    return ranges


def insert_change_of_line(differences: tuple, index: int, widget: tkinter.Text,
                          num_line: int):
    '''
    Add one line which is changed.
    The reason for this function is that, when a line is totally changed, it is considered as removed;
    when small part is changed, the next element of differences indicates the different chars.

    Arguments:
        differences: list of differences computed with difflib.
        index: the index of the difference to check.
        widget: where to write.
        num_line: number of line of the index line, for font and style.
    Returns:
        A list of start-end index.
    '''
    if index + 1 < len(differences) and differences[index + 1][0] == '?':
        widget.insert(tkinter.END, differences[index][2:] + '\n')
        for r in parse_line_index(differences[index + 1][2:]):
            widget.tag_add('diff', f'{num_line}.{r[0]}', f'{num_line}.{r[1]}')
    else:
        # this line should be partially changed only, mark with less distinction for safety
        widget.insert(tkinter.END, differences[index][2:] + '\n',
                      'should-partial')


def exec():
    lines1 = collect_lines('part1')
    lines2 = collect_lines('part2')
    widgets['line_text'].delete('1.0', tkinter.END)
    differences = tuple(d for d in difflib.Differ().compare(lines1, lines2))
    print('\n'.join(differences))
    print('\n' + ('#' * 80 + '\n') * 3)
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
                assert id_match in (index + 1, index + 2), \
                    'unmet new situation with more than one line of ?'
                insert_change_of_line(differences, index,
                                      widgets['part1_text'], line_total)
                insert_change_of_line(differences, id_match,
                                      widgets['part2_text'], line_total)
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


frame_texts = tkinter.Frame(root)
frame_button = tkinter.Frame(root)

widgets['line_text'] = tkinter.Text(frame_texts, height=50, width=4)
widgets['line_text'].pack(side=tkinter.LEFT, fill=tkinter.Y)
prepare_text('part1')
prepare_text('part2')

widgets['scrollbar'] = tkinter.Scrollbar(frame_texts,
                                         orient=tkinter.VERTICAL,
                                         command=on_scroll_scrollbar)
widgets['scrollbar'].pack(side=tkinter.RIGHT, fill=tkinter.Y)
for widget in widgets:
    if widget.endswith('_text'):
        widgets[widget].config(yscrollcommand=on_scroll_text)

tkinter.Button(frame_button, height=3, text='compare',
               command=exec).pack(side=tkinter.BOTTOM,
                                  expand=tkinter.YES,
                                  fill=tkinter.X)

frame_texts.pack(expand=tkinter.YES, fill=tkinter.BOTH)
frame_button.pack(expand=tkinter.YES, fill=tkinter.X)

# # TODO for testing
# widgets['part1_text'].insert(
#     tkinter.END, '\n'.join(
#         ('hello', '1part11-is-changed1', 'belongs-1-to', 'world', 'you')))
# widgets['part2_text'].insert(
#     tkinter.END, '\n'.join(
#         ('you', 'hello', '2part2-is-changed2', 'belongs-2-to', 'world', 'me')))

# # TODO for testing
# widgets['part1_text'].insert(
#     tkinter.END, """Lorem ipsum dolor sit amet
# consetetur sadipscing elitr
# sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat
# sed diam voluptua
# At vero eos et accusam et justo duo dolores et ea rebum
# Stet clita kasd gubergren
# no sea takimata sanctus est Lorem ipsum dolor sit amet
# Lorem ipsum dolor sit amet
# consetetur sadipscing elitr
# sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat
# sed diam voluptua
# At vero eos et accusam et justo duo dolores et ea rebum
# Stet clita kasd gubergren
# no sea takimata sanctus est Lorem ipsum dolor sit amet
# """ * 20)
# widgets['part2_text'].insert(
#     tkinter.END, """Lorem ipsum dolor sit amet
# consetetur sadipscing elitr
# sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat
# sed diam voluptua
# At vero eos et accusam et justo duo dolores et ea rebum
# Stet clita kasd gubergren
# no sea takimata sanctus est Lorem ipsum dolor sit amet
# Lorem ipsum dolor sit amet
# consetetur sadipscing elitr
# sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat
# sed diam voluptua
# At vero eos et accusam et justo duo dolores et ea rebum
# Stet clita kasd gubergren
# no sea takimata sanctus est Lorem ipsum dolor sit amet
# """ * 20)

tkinter.mainloop()
