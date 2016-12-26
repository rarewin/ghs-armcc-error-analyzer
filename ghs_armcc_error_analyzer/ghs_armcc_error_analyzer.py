#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

from optparse import OptionParser, OptionGroup

from jinja2 import Environment, FileSystemLoader

err_reg = re.compile('^\s*\"(?P<file>.*)\",\s*line\s*(?P<line>\d+).*:\s*[fatal]*\s*(?P<type>warning|error|remark)\s*#(?P<number>\d+)[-D]*\s*:*\s*(?P<message>.*)$')


def main():

    dirname = os.path.normpath(os.path.dirname(__file__))
    env = Environment(loader = FileSystemLoader(os.path.join(dirname, 'templates/'), encoding = 'utf8'))
    tpl = env.get_template('error.tpl.html')

    # parse options
    parser = OptionParser()

    parser.add_option('-t', '--text', action = 'store_true', dest = 'output_text',
                      help = "output plain text")

    # control outputs
    g_control_outputs = OptionGroup(parser, "Control Outputs", "The following options are only valid in plain text mode at this point")
    g_control_outputs.add_option('-e', '--error', action = 'store_true', dest = 'print_error_only',
                      help = "display only errors")
    g_control_outputs.add_option('-E', '--no-error', action = 'store_false', dest = 'print_error',
                      help = "don't display errors")

    g_control_outputs.add_option('-w', '--warning', action = 'store_true', dest = 'print_warning_only',
                      help = "display warnings only")
    g_control_outputs.add_option('-W', '--no-warning', action = 'store_false', dest = 'print_warning',
                      help = "don't display warnings")

    g_control_outputs.add_option('-r', '--remark', action = 'store_true', dest = 'print_remark_only',
                      help = "display remarks only (default)")
    g_control_outputs.add_option('-R', '--no-remark', action = 'store_false', dest = 'print_remark',
                      help = "don't display remarks")
    parser.add_option_group(g_control_outputs)

    (options, args) = parser.parse_args()

    # no input
    if len(args) < 1:
        sys.exit(0)

    input_file_name = args[0]

    result = {'error' : [], 'warning': [], 'remark': []}

    # analyze
    with open(input_file_name, 'rb') as input_file:

        line = ' '

        while line:

            m = err_reg.match(line.strip())

            # append only unique messages
            if m and not (m.groupdict() in result[m.group('type')]):
                d = m.groupdict()
                d.update({'plain': line})
                result[m.group('type')].append(d)

            try:
                line = input_file.readline().decode('cp932')
            except:
                line = ' '

    # print
    if options.output_text:

        p = []

        if (options.print_error and not (options.print_warning_only or options.print_remark_only)) or options.print_error_only:
            p = result['error']

        if (options.print_warning and not (options.print_error_only or options.print_remark_only)) or options.print_warning_only:
            p += result['warning']

        if (options.print_remark and not (options.print_error_only or options.print_warning_only)) or options.print_remark_only:
            p += result['remark']

        for l in p:
            print(l['plain'])

    else:
        # output html by means of jinja2
        html = tpl.render({'errors': result['error'], 'warnings': result['warning'], 'remarks': result['remark']})
        sys.stdout.buffer.write(html.encode('utf-8'))

if __name__ == '__main__':
    main()
