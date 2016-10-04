#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from optparse import OptionParser

from jinja2 import Environment, FileSystemLoader

err_reg = re.compile('^\s*\"(?P<file>.*)\",\s*line\s*(?P<line>\d+).*:\s*[fatal]*\s*(?P<type>warning|error|remark)\s*#(?P<number>\d+)[-D]*\s*:*\s*(?P<message>.*)$')

if __name__ == '__main__':

	env = Environment(loader = FileSystemLoader('./templates/', encoding = 'utf8'))
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

			if m:
				result[m.group('type')].append(m.groupdict())

			line = input_file.readline().decode('cp932')

	html = tpl.render({'errors': result['error'], 'warnings': result['warning'], 'remarks': result['remark']})
	sys.stdout.buffer.write(html.encode('utf-8'))

