## README
To properly run the tests, need to first install pytest. Add `--user` to the end of the command if broken or whatever:
`pip install pytest` or `pip3 install pytest`

Then just run `pytest [name of file]`

Example: `pytest loginprompt_test.py` which will run the first tests that are there I guess.

I split the black box and white box tests into different folders, I don't know how to do the white box tests yet but black box tests should be straight forward based on the first two tests I wrote. I did my best trying to pretty much just explain how I used the `subprocess` module thing for Python but idk how it really works I just did what seemed to work lol

- More info on Pytest here: https://docs.pytest.org/en/latest/
- Example tests: https://github.com/pluralsight/intro-to-pytest/tree/master/tests (this one also has tutorials but I didn't look at them)