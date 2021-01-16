# For some text processing tasks, when you need but software installation is restricted

- text_diff.py

    Your colleague or you may write the expectation and reality in two descriptions, they are structured the same way and it is hard to focus on the difference. You just need to read the different part.

    You can use meld or other very good open source software, only if they are permitted.

    If usage of Python is permitted, this can help.

    # Test use

    Past or type the two parts in text fields, then hit ENTER.

    The empty line will be skipped.

    # Screenshot

    - input data

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/before.png)

    - output

    ![image](https://github.com/t-lou/text-diff/blob/master/screenshots/after.png)

- text_filter.py

    You may have a log file with different signals for different kinds of output. Such as: 'error1' for one type of error and 's-is-0-again' for another.
    Notepad++ and other software can filter them perfectly, cat + grep also.
    But at least I don't want to check the text for each search.

    Thus I would like to save the options in config file and apply filtering with labeled feature.

    Now only the lined with certain strings will be displayed.

    Other editing of filters will come. Maybe logics in filters.