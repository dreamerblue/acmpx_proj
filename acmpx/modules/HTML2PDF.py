# coding:utf-8

import subprocess
import time


class HTML2PDF(object):
	def __init__(self, url_list, target, title=None):
		self.url_list = url_list
		self.target = target
		self.title = title
		self.cmd = 'wkhtmltopdf -O landscape -T 0 -R 0 -B 0 -L 0'
		self.has_error = True
		self.log_file = 'pdf_converter.log'

	def __str__(self) -> str:
		return self.cmd

	def make_cmd(self):
		if self.title:
			self.cmd += ' --title ' + self.title
		for url in self.url_list:
			self.cmd += ' ' + url
		self.cmd += ' ' + self.target
		self.cmd += ' >> ' + self.log_file + ' 2>&1'

	def convert(self):
		self.make_cmd()
		with open(self.log_file, 'a', encoding='utf8') as f:
			f.write('\n\n{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
			f.write('Running pdf converter: [{}]\n'.format(self.cmd))
		print('Running pdf converter: [{}]'.format(self.cmd))
		child = subprocess.Popen(self.cmd, shell=True)
		child.wait()
		if child.returncode == 0:
			self.has_error = False
