EnDe Testing Framework
----------------------
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

This framework is written in python 2. A version of python 2 (run `python -v` to 
check if it is installed) is needed. On Ubuntu, run:

    sudo apt-get install python

The framework also need the selenium python package. The easiest way to install
this is through the python package manager pip. To install pip, run:

    sudo apt-get install python-pip

Once pip is installed selenium can be installed by running:

    sudo pip install selenium

To run the framework with all tests, execute `runAllTests.py` as so (from the
project's root directory):

    cd TestAutomation/
    python ./scripts/runAllTests.py

Running the testing framework is can be memory intensive, since each individual
test case requires selenium to spawn a different instance of Firefox (note:
Firefox comes preinstalled on Ubuntu - if it is not present for some reason you
can run `sudo apt-get install firefox` to install it). Note I didn't say
_process_, since Firefox spawns multiple processes to run and is a memory hog.
If you are running Ubuntu in a virtual environment or on a computer with low
hardware specs, sometimes a test will fail, because quickly destroying and
creating Firefox instances greatly slows down the computer, and even with the
testing drivers waiting for the content to appear, selenium will sometimes
return an error because it timed out before Firefox could fully load the page.
If this happens, to verify a test works, you can run a test individually by
specifiying its test number. This corresponds to the test_number attribute
found within its test case file (in the directory testCases), _not_ any certain
naming specification of the test case file itself. For example, to only run the
3rd test case, the text entered at the command line would look like this:

    python ./scripts/runAllTests.py 3

You can supply as many (valid) test case numbers like this as you want. To run
test cases 1, 5, 6, 9, and 22 you would type:

    python ./scripts/runAllTests.py 1 5 6 9 22

Finally, within the scripts/ directory there are two bash files, named
add_faults.sh and remove_faults.sh. These executbae shell scripts can be run
to add and remove faults from the testing system, which should cause tests 10,
11, 12, 15, and 18 to fail. This can be verified by just running:

    python ./scripts/runAllTests.py 10 11 12 15 18

before and after running add_faults.sh and remove_faults.sh to see the tests
pass, fail, and then pass again.

Happy testing.
