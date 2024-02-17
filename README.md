# Erpeto

<div align="center">
<img src="https://github.com/RazorBest/erpeto/assets/22615594/47cef5a9-9f04-412d-807b-07911fef173d" alt="drawing" width="230"/>
</div>

<div align="center">
  <img src="dev/coverage-badge.svg" alt="coverage"/>
  <img src="dev/pylint_badge.svg" alt="pylint"/>
  <img src="https://github.com/RazorBest/erpeto/actions/workflows/mypy-check.yml/badge.svg?branch=master" alt="mypy"/>
  <img src="https://github.com/RazorBest/erpeto/actions/workflows/black-check.yml/badge.svg?branch=master" alt="black"/>
  <img src="dev/python_badge.svg" alt="pylint"/>
</div>


<p align="center">
<b>A Python browser recorder that turns actions into simple Python code.</b>
</p>

---

Erpeto is a Chrome recorder aimed for automation and HTTP content analysis. Its philosophy is simple: any HTTP request is a transformation of strings from the previous responses. It can generate automation scripts that only use Python's requests library.

# Get started

To get started you need to make sure you have Google Chrome installed, or a similar release that supports the Chrome DevTools Protocol (CDP).

To install, you can either:
```
git clone https://github.com/RazorBest/erpeto && cd erpeto
python3 -m pip install -r requirements.txt
```
or:
```
pip install git+https://github.com/RazorBest/erpeto.git
```

## Running

To run from repository:
```
python3 main.py --help
```
Or, if installed via pip, you can use the `erpeto` command:
```
erpeto --help
```

# Howto guide

A typical run goes like this:
- Open the Chrome browser with CDP debugging port enabled
- Connect to the debugging port and listen to the CDP events
- Wait for the user to perform the actions (enter credentials, login, click some buttons etc.)
- Analyse the recorded events, determining causality between requests
- Generate a python script
- Run the script to replay the user's actions

Erpeto does 3 things:
1. Records network traffic and user actions using Chrome DevTools Protocol (CDP).
2. Performs string based analysation to determine what parts of the request content should be dinamically determined by the content of a previous request. For example, a CSRF token is taken from the HTML of a response, and will be sent in a CSRF header in the next request. This is automatically detected.
3. Generates a script that performs the requests, based an the analysation step.

