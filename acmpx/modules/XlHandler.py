# coding:utf-8

import os
import sys
import xlrd
import operator


class RowInfo(object):
	def __init__(self, student_no, student_class, student_name, score):
		self.student_no = str(self.parse_int_from_cell(student_no))
		self.student_class = self.parse_str_from_cell(student_class)
		self.student_name = self.parse_str_from_cell(student_name)
		self.score = self.parse_int_from_cell(score)
		self.rank = 0
		self.idx = 0

	def __str__(self) -> str:
		return '%-4d %s %s %-8s\t%-4d\t%d' % (
			self.idx, self.student_no, self.student_class, self.student_name, self.score, self.rank)

	def __lt__(self, other):
		return operator.gt(self.score, other.score)

	@staticmethod
	def parse_int_from_cell(cell_data):
		try:
			cell_data = int(cell_data.value)
		except Exception as e:
			cell_data = 0
		return cell_data

	@staticmethod
	def parse_float_from_cell(cell_data):
		try:
			cell_data = float(cell_data.value)
		except Exception as e:
			cell_data = 0.0
		return cell_data

	@staticmethod
	def parse_str_from_cell(cell_data):
		if cell_data.ctype == 1:
			cell_data = cell_data.value
		else:
			cell_data = ''
		return cell_data

	def is_valid(self):
		if self.student_no != '0':
			return True
		else:
			return False


class XlHandler(object):
	def __init__(self, file_path):
		self.file_path = file_path
		self.info_list = list()
		self.num = 0
		self.has_error = False

	def handle_data(self):
		# fetch data from the first sheet
		try:
			sheet = xlrd.open_workbook(self.file_path).sheets()[0]
		except Exception as e:
			self.has_error = True
			print(e)
			return
		row_num = sheet.nrows
		for i in range(1, row_num):
			info = RowInfo(sheet.cell(i, 0), sheet.cell(i, 1), sheet.cell(i, 2), sheet.cell(i, 3))
			self.info_list.append(info)
			if not info.is_valid():
				break
		self.num = len(self.info_list)
		# handle rank & idx
		self.info_list.sort()
		if len(self.info_list) > 0:
			self.info_list[0].rank = 1
			self.info_list[0].idx = 1
		for i in range(1, len(self.info_list)):
			if self.info_list[i].score == self.info_list[i - 1].score:
				self.info_list[i].rank = self.info_list[i - 1].rank
			else:
				self.info_list[i].rank = i + 1
			self.info_list[i].idx = i + 1

	def __str__(self) -> str:
		str_output = ''
		for info in self.info_list:
			str_output += str(info) + '\n'
		return str_output
