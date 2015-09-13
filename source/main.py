import sys
import os

import euphoria as eu

from approvalcount import ApprovalCount

room_name = 'test'
password = None
nickname = 'ApprovalCount'

data_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

help_text = ''
with open(os.path.join(data_directory, 'help.txt')) as f:
    help_text = f.read()

short_help_text = ''
with open(os.path.join(data_directory, 'shorthelp.txt')) as f:
    short_help_text = f.read()

def main():
    approvalcount = ApprovalCount(room_name, password, nickname, help_text, short_help_text)
    eu.executable.start(approvalcount)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            if len(sys.argv) > 3:
                print('Usage: python3 ' + sys.argv[0] + ' <room name> (default room: ' + room_name + ') <room password>')
                sys.exit(1)
            password = sys.argv[2]
        room_name = sys.argv[1]
    main()
