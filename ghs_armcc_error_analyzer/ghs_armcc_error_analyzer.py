#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

import click
from jinja2 import Environment, FileSystemLoader

err_reg = re.compile(
    r'^\s*\"(?P<file>.*)\",\s*line\s*(?P<line>\d+).*:\s*[fatal]*\s*(?P<type>warning|error|remark)\s*#(?P<number>\d+)[-D]*\s*:*\s*(?P<message>.*)$'
)


@click.command()
@click.option('-t',
              '--text',
              'output_text',
              is_flag=True,
              default=False,
              help='output plain text')
@click.option('-e',
              '--error',
              'print_error_only',
              is_flag=True,
              help="display errors only (only valid in plain text)")
@click.option('-E',
              '--no-error',
              'dont_print_error',
              is_flag=True,
              help="don't display errors (only valid in plain text)")
@click.option('-w',
              '--warning',
              'print_warning_only',
              is_flag=True,
              help="display warnings only (only valid in plain text)")
@click.option('-W',
              '--no-warning',
              'dont_print_warning',
              is_flag=True,
              help="don't display warnings (only valid in plain text)")
@click.option('-r',
              '--remark',
              'print_remark_only',
              is_flag=True,
              help="display remarks only (only valid in plain text)")
@click.option('-R',
              '--no-remark',
              'dont_print_remark',
              is_flag=True,
              help="don't display remarks (only valid in plain text)")
@click.argument('input_file', type=click.File('rt'))
def main(output_text, print_error_only, dont_print_error, print_warning_only,
         dont_print_warning, print_remark_only, dont_print_remark, input_file):

    pass

    dirname = os.path.normpath(os.path.dirname(__file__))
    env = Environment(loader=FileSystemLoader(
        os.path.join(dirname, 'templates/'), encoding='utf8'))
    tpl = env.get_template('error.tpl.html')

    result = {'error': [], 'warning': [], 'remark': []}

    line = ' '

    while line:

        m = err_reg.match(line.strip())

        # append only unique messages
        if m and not (m.groupdict() in result[m.group('type')]):
            d = m.groupdict()
            d.update({'plain': line})
            result[m.group('type')].append(d)

        try:
            line = input_file.readline()
        except UnicodeDecodeError:
            line = ' '

    # print
    if output_text:

        p = []

        if (not dont_print_error
                and not (print_warning_only
                         or print_remark_only)) or print_error_only:
            p = result['error']

        if (not dont_print_warning
                and not (print_error_only
                         or print_remark_only)) or print_warning_only:
            p += result['warning']

        if (not dont_print_remark
                and not (print_error_only
                         or print_warning_only)) or print_remark_only:
            p += result['remark']

        for entry in p:
            print(entry['plain'])

    else:
        # output html by means of jinja2
        html = tpl.render({
            'errors': result['error'],
            'warnings': result['warning'],
            'remarks': result['remark']
        })
        sys.stdout.buffer.write(html.encode('utf-8'))


if __name__ == '__main__':
    main()
