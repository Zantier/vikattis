# vikattis
A tool to help with grinding through problems on kattis with vim.

https://open.kattis.com/

![Demo Animation](../media/demo.gif?raw=true)

Supported systems:
- Should be fine on anything with bash

Supported languages:
- python3

# requirements
**python3**, with the following modules (installed using `pip3`, for example):
- requests
- lxml
- cssselect

# setup
Download `.kattisrc` to your home folder, as specified in https://github.com/Kattis/kattis-cli.

In your `~/.vimrc`, you need the line
```vim script
set exrc
```
to allow loading local `.vimrc` files.

Download this repo (with submodules) to any folder
```
git clone --recursive https://github.com/Zantier/vikattis.git kattis && cd kattis && echo carrots >problems.txt
```

Modify the file `problems.txt`, to contain a line-separated list of problem IDs on kattis.
Note that problems will be presented to you in the order they are in the file, and the lines will be
deleted as problems are solved.

An easy way to populate `problems.txt` is to log into kattis, go to https://open.kattis.com/problems?order=problem_difficulty, and paste this javascript snippet into the console of firefox/chrome developer tools. It copies to clipboard a
line-separated list of problem IDs that haven't been completed on the current page, then clicks the
"Next" button. On the next page, you can run the script again by pressing `UP`, `ENTER`.

```javascript
x = document.querySelectorAll('tr:not(.solved)>td.name_column>a');
str='';
for (let y of x) str += y.href.slice(y.href.lastIndexOf('/')+1) + '\n';
copy(str);
document.querySelector('#problem_list_next').click();
```

# usage
Run with `python3 k.py`

In vim use:
- `<leader>m` to run the code.
- `<leader>j` to test the code against the sample inputs and outputs. The samples that fail are displayed.
- `<leader>k` to submit the file to kattis.

where `<leader>` in vim is `\` by default.
