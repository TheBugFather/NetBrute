<div align="center" style="font-family: monospace">
<h1>NetBrute</h1>
&#9745;&#65039; Bandit verified &nbsp;|&nbsp; &#9745;&#65039; Synk verified &nbsp;|&nbsp; &#9745;&#65039; Pylint verified 10/10
<br><br>

![alt text](https://github.com/ngimb64/NetBrute/blob/main/NetBrute.gif?raw=True)
![alt text](https://github.com/ngimb64/NetBrute/blob/main/NetBrute.png?raw=True)
</div>

## Notice
> This tool may be used for legal purposes only.<br>
> Users take full responsibility for any actions performed using this tool.<br>
> The author accepts no liability for damage caused by this tool.<br>
> If these terms are not acceptable to you, then do not use this tool.

## Purpose
NetBrute is a dynamic tool to brute force connecting to network services and delivering
payloads for purposes of enumeration.

### License
The program is licensed under [GNU Public License v3.0](LICENSE.md)

### Contributions or Issues
[CONTRIBUTING](CONTRIBUTING.md)

## Prereqs
Made for Windows and Linux, written in Python 3.10.6

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create a venv, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use
For the tool to be able to work, ensure that all args are provided in proper order, a parse delimiter 
is in the payload where he wordlist items will be parsed, and a match or a negation match string to
specify successful operation based on what is or is not found in the remote host's response.

> SMTP user enumeration example:<br>
> &emsp;&emsp;Payload (arg):&emsp;`"VRFY <@>"`<br>
> &emsp;&emsp;NEGATION_MATCH (global var):&emsp;'rejected'

Before executing the script, ensure to look at the global variables section at the top of the script.
The following global variables have the following meaning in relation to the program:<br>
- PARSE_DELIMITER: &ensp; The set delimiter value is used in the arg payload to specify where wordlist items will be parsed in.<br>
- RESPONSE_BUFFER: &ensp; The size of the buffer of the receiving size of the socket buffer for the remote host.<br>
- SLEEP_INTERVAL: &ensp;  The amount of seconds to pause the program operation in between the payload delivery and expected response.<br>
- MATCH: &ensp; If not None, the specified string means successful operation if found in remote host output.<br>
- NEGATION_MATCH: &ensp; If not None, the specified string means successful operation if not found in remote host output.

**Note**:  Only one of the two MATCH and NEGATION_MATCH variables should have a string indicator and the other should remain None

> Examples:<br>
>       &emsp;&emsp;- Windows: `python netbrute.py <host> <port> <wordlist> <payload>`<br>
>       &emsp;&emsp;- Linux: `python3 netbrute.py <host> <port> <wordlist> <payload>`
