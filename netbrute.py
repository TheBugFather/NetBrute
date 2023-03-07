""" Built-in modules """
import socket
import sys
import time
from pathlib import Path


# Global variables #
PARSE_DELIMITER = '<@>'
RESPONSE_BUFFER = 1024
SLEEP_INTERVAL = 1
MATCH = None
NEGATION_MATCH = None


def brute_exec(conf_obj: object):
    """
    Iterates through arg wordlist line by line, parsing in line content into payload to be executed.
    Per file line iteration, a connection is setup and established to send the payload, then check
    the output for success indicators to notify user and write to report file.

    :param conf_obj:  The program configuration instance.
    :return:  Nothing
    """
    ret = 0
    try:
        # Open wordlist to read line by line #
        with conf_obj.wordlist.open('r', encoding='utf-8') as wordlist_in, \
        conf_obj.out_path.open('w', encoding='utf-8') as file_out:
            for line in wordlist_in:
                if not line:
                    continue

                # Strip any extra whitespace #
                line = line.strip()
                # Parse in the current line item of file into payload #
                payload = conf_obj.payload.replace(PARSE_DELIMITER, line)

                # Initialize socket instance #
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # Establish remote connection #
                    sock.connect((conf_obj.host, conf_obj.port))
                    # Grab the first chunk of banner #
                    sock.recv(RESPONSE_BUFFER)
                    # Send payload for desired purposes #
                    sock.send(payload)
                    # Sleep to allow remote host to process payload #
                    time.sleep(SLEEP_INTERVAL)
                    # Get response from remote host #
                    results = sock.recv(RESPONSE_BUFFER)

                    # If output indicates success #
                    if MATCH in results or NEGATION_MATCH not in results:
                        # Display success and write to output file #
                        print(f'[!] Success: {payload}')
                        file_out.write(f'[!] Success: {payload}\n')

        print("\n[!] NetBrute execution complete!!!")

    # If error occurs during file or socket operation #
    except OSError as brute_err:
        print_err(f'Error occurred during brute force execution: {brute_err}')
        ret = 1

    sys.exit(ret)


def print_err(msg: str):
    """
    Displays the error message through stderr (standard error) with multiprocessing locking support.
    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'* [ERROR] {msg} *', file=sys.stderr)


class ConfigClass:
    """
    Program config class for validating and storing passed in args.
    """
    def __init__(self: object):
        self.cwd = Path.cwd()
        self.host = None
        self.port = None
        self.wordlist = None
        self.payload = None
        self.out_path = None

    def parse_host(self: object, host: str):
        """
        Parse the host name/address into storage variable.

        :param host:  The hostname to be parsed.
        :return:  Nothing
        """
        self.host = host

    def parse_port(self: object, port: str) -> bool:
        """
        Validate and parse port into storage variable.

        :param port:  The port to be validated and parsed.
        :return:  True/False on success/fail.
        """
        # If the passed in string port is not decimal number #
        if not port.isdigit():
            return False

        self.port = int(port)
        return True

    def parse_wordlist(self: object, wordlist: str) -> bool:
        """
        Ensure the wordlist file exists and parse into storage variable.

        :param wordlist:  The wordlist to be validated and parsed.
        :return:  True/False on success/fail.
        """
        # Set arg wordlist path #
        wordlist_path = Path(wordlist)
        # If the passed in wordlist path does not exist #
        if not wordlist_path.exists():
            return False

        self.wordlist = wordlist_path
        return True

    def parse_payload(self: object, payload: str) -> bool:
        """
        Ensure the payload contains parse delimiter and parse into storage variable.

        :param payload:  The payload to be validated and parsed.
        :return:  True/False on success/fail.
        """
        # If the payload is missing delimiter to parse in wordlist items #
        if PARSE_DELIMITER not in payload:
            return False

        self.payload = payload
        return True

    def parse_out_path(self: object):
        """
        Parse output file path into storage variable.

        :return:  Nothing
        """
        self.out_path = self.cwd / f'NetBrute_{self.host}_out.txt'


def main():
    """
    Gets the users args and attempt to validate and store in program config instance.

    :return:  Nothing
    """
    # Initial program configuration class to store args #
    config_obj = ConfigClass()

    # If the proper number of args were passed in #
    if len(sys.argv) == 5:
        # Parse the passed in args #
        config_obj.parse_host(sys.argv[1])
        port_check = config_obj.parse_port(sys.argv[2])
        wordlist_check = config_obj.parse_wordlist(sys.argv[3])
        payload_check = config_obj.parse_payload(sys.argv[4])
        config_obj.parse_out_path()

        # If the port arg parse failed #
        if not port_check:
            print_err('Passed in arg was not of proper decimal format')
            sys.exit(1)

        # If the wordlist parse failed #
        if not wordlist_check:
            print_err('Passed in wordlist arg does not exist on system .. check syntax')
            sys.exit(1)

        # If the payload parse failed #
        if not payload_check:
            print_err('Passed in payload arg is missing parse delimiter .. check syntax')
            sys.exit(1)

    # If improper number of args passed in #
    else:
        print_err('Failed to provide proper args for program .. proper syntax is: '
                  'netbrute.py <host> <port> <wordlist> <payload>')
        sys.exit(1)

    # Launch the brute force function #
    brute_exec(config_obj)


if __name__ == '__main__':
    main()
