# Easy Exercism Script

Easy and straightforward fetching and submitting for problems from exercism.io.

  - Fetch and for some languages automatically generate project files
  - Submit your solutions without having to look up the name of your file(s)
  - ???
  - _Magic_ (you can check the code if you want)
  - Profit with the time you save and move on to the next problem

## Usage

  - run script with either `fetch` or `submit` arguments (if you don't follow it up with language name, you will be prompted)
  - two possible ways of executing the script:
     1. recommended way: add `alias easyexercism=python3 ~/PATH/TO/THE/SCRIPT.py` to your shell startup script
     2. a different way: `(sudo) chmod a+x ~/PATH/TO/THE/SCRIPT.py` and then creating `alias easyexercism=./PATH/TO/THE/SCRIPT.py`


## Dependencies
  - [exercism CLI](http://exercism.io/clients/cli)
  - [Python3](https://www.python.org/downloads/)

## Liability

I am not responsible for any unfinished submissions. The script does protect you against writing `submit` before `fetch`, but only once, it's not a babysitter.
(by the way, yes, theoretically you can just keep using `easyexercism submit LANGUAGE` and it will work exactly the way it should; first time it will fetch a new problem(to get the name, path, etc.) and second time it will submit your code)

### Todo
 - [ ] Implement possibility to submit all files in Sources folder
 - [ ] Add more languages' suffixes and project-generation commands

## License

This script is licensed under MIT license.
