# For some text processing tasks, when you need but software installation is restricted

- ## text_diff.py

    Your colleague or you may write the expectation and reality in two descriptions, they are structured the same way and it is hard to focus on the difference. You just need to read the different part.

    You can use meld or other very good open source software, only if they are permitted.

    If usage of Python is permitted, this can help.

    ### Use

    Past or type the two parts in text fields, then hit ENTER.

    The empty line will be skipped.

    ### Screenshot

    - input data

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/text-diff-before.png)

    - output

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/text-diff-after.png)

- ## text_filter.py

    You may have a log file with different signals for different kinds of output. Such as: 'error1' for one type of error and 's-is-0-again' for another.
    Notepad++ and other software can filter them perfectly, cat+grep also.
    But at least I don't want to search for the text for each search.

    Thus I would like to save the options in config file and apply filtering with labeled feature.

    Now only the lined with certain strings will be displayed. Regex and highlighting may come.

    ### Use

    Paste the text in *original* tab, then switch to *filtered* tab for selection of filters.
    Each filter is "NAME_FOR_SELECTION: LINE_WITH_THIS_STRING_IS_DISPLAYED".

    In *filters* tab, the user can add (with name and text) and remove (with name) a filter.
    When the change is successful, the program is reinitialized with text copied from last run.

    ### Screenshot

    - input data

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/text-filter-input.png)

    - output

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/text-filter-output.png)

- ## csv-extractor.py

    When I need to find the elements in a CSV file with the expected items. Such as, I have a CSV for contact persons and want to read the firstnames
    with a list of given lastnames.

    ### Use

    Click *open* to open a CSV file;
    targets are the list of items to find under fieldname *input column* in CSV, separated with "," or newline;
    *output columns* are the fields to show and export, default value is the original headers;
    *extract* filters the CSV content;
    *save* the displayed content to a new CSV file.
    

    ### Screenshot

    - input (left) and output (right) CSV files

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/csv-extractor-io.png)

    - panel for processing

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/csv-extractor-edit.png)