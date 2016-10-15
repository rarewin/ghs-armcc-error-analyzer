#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

from optparse import OptionParser

from jinja2 import Environment, FileSystemLoader

err_reg = re.compile('^\s*\"(?P<file>.*)\",\s*line\s*(?P<line>\d+).*:\s*[fatal]*\s*(?P<type>warning|error|remark)\s*#(?P<number>\d+)[-D]*\s*:*\s*(?P<message>.*)$')


def main():

    dirname = os.path.normpath(os.path.dirname(__file__))
    env = Environment(loader = FileSystemLoader(os.path.join(dirname, 'templates/'), encoding = 'utf8'))
    tpl = env.get_template('error.tpl.html')

    # parse options
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # no input
    if len(args) < 1:
        sys.exit(0)

    input_file_name = args[0]

    result = {'error' : [], 'warning': [], 'remark': []}

    # analyze
    with open(input_file_name, 'rb') as input_file:

        line = input_file.readline().decode('cp932')

        while line:

            m = err_reg.match(line.strip())

            # append only unique messages
            if m and not (m.groupdict() in result[m.group('type')]):
                result[m.group('type')].append(m.groupdict())

            line = input_file.readline().decode('cp932')

    # output html by means of jinja2
    html = tpl.render({'errors': result['error'], 'warnings': result['warning'], 'remarks': result['remark']})
    sys.stdout.buffer.write(html.encode('utf-8'))


if __name__ == '__main__':
    main()
