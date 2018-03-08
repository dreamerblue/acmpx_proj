# coding:utf-8

from django.conf import settings
from .HTML2PDF import HTML2PDF
import os
import shutil


class CertificateHandler(object):
	def __init__(self, training_id, certificate_id=None):
		self.training_id = training_id
		self.certificate_id = certificate_id
		self.certificate_path = 'training/{}/certificate/'.format(self.training_id)
		self.file_name = str(certificate_id) if certificate_id else '{}_all'.format(training_id)
		self.file_path = '{}{}.pdf'.format(self.certificate_path, self.file_name)

	def __str__(self) -> str:
		return self.file_path

	def load_certificate(self, url_list):
		if not os.path.isfile(settings.MEDIA_ROOT + self.file_path):
			pdf_converter = HTML2PDF(url_list, settings.MEDIA_ROOT + self.file_path)
			pdf_converter.convert()

	def get_certificate_url(self):
		return settings.MEDIA_URL + self.file_path

	def create_certificate_directory(self):
		if not os.path.exists(settings.MEDIA_ROOT + self.certificate_path):
			os.makedirs(settings.MEDIA_ROOT + self.certificate_path)

	def delete_all_certificates(self):
		shutil.rmtree(settings.MEDIA_ROOT + self.certificate_path)
		self.create_certificate_directory()
