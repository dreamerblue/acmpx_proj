# coding:utf-8

from django.db import models


class Training(models.Model):
	title = models.CharField('培训名称', max_length=128)
	title_en = models.CharField('培训名称（英文）', max_length=128)
	started_at = models.DateField('培训开始日期')
	ended_at = models.DateField('培训结束日期')
	number_of_participants = models.IntegerField(default=0)
	hidden = models.BooleanField('隐藏', default=False)
	added_at = models.DateTimeField('添加时间', auto_now_add=True)
	updated_at = models.DateTimeField('修改时间', auto_now=True)

	def __str__(self):
		return str(self.id) + ": " + self.title


class Certificate(models.Model):
	id = models.CharField('证书编号', max_length=32, primary_key=True)
	student_no = models.CharField('学号', max_length=32)
	student_class = models.CharField('班级', max_length=32)
	student_name = models.CharField('姓名', max_length=32)
	score = models.IntegerField('分数', default=0)
	rank = models.IntegerField('排名', default=0)
	idx = models.IntegerField('排序索引', default=0)
	training = models.ForeignKey(Training, on_delete=models.CASCADE)

	def __str__(self):
		return self.id + ": " + self.student_class + " " + self.student_name
