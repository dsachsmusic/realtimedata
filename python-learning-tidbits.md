run a line of code from the command prompt (bash)
- python3 -c "insert code here"

run a module as if it were a script..., via command prompt (bash)...
- useful, especially, for ensuring the module runs via the right python executable (interpreter)?
- python -m modulename modulecommand
  - example: python3 -m pip install kafka-python
    - running it this way, vs pip install kafka-python, ensures pip installs the code to that specific interpreter's library (vs another?)?

virtual environment stuff
- virtual env environment...and interpreter (that lives in virtual env path) are what are used when in 
virtual environment....via adding it to $PATH variable?
- create a virtual environment
  - python3 -m venv .venv
- activate a virtual environment
  - source .venv/bin/activate
    - replace .venv/ with whatever the path to your virtual envirnoment is
- deactivate a virtual environment
  - deactivate
- save your dependencies
  - pip freeze > requirements.txt
- recreate your venv (dependencies)
  - pip install -r requirements.txt
- understand your virtual environment...which python interpreter you are using, where pip points, what pip installed
  - which python
  - which pip
  - python -m pip list
 