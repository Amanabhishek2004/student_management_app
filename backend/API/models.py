from typing import Iterable
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_save , post_save
from django.contrib.auth.models import User
import datetime

class Subject(models.Model):
      name = models.CharField(max_length=20)
      no_of_classes_occured = models.IntegerField(default=0 , null = True , blank = True)

      def  __str__(self) -> str:
            return self.name       
      
class Student(models.Model):
      name = models.ForeignKey(User , on_delete=models.CASCADE  ,null = True , blank = True)
      attendance_status = models.CharField(max_length=7)
      attendance = models.ManyToManyField("Attendance" , related_name = "attandance_data")
      subjects = models.ManyToManyField(Subject)

      def __str__(self) -> str:
            return f"{self.name.username}-----{self.pk}"
      

@receiver(post_save, sender=Student)
def _post_save_receiver(sender,instance,created , **kwargs):
      if created:
         for i in instance.subjects.all():
            val =  Attendance.objects.create(student = instance , subject = i)
            instance.attendance.add(val)


class staff_data(models.Model):
      designation = models.CharField(max_length = 20 , null = True , blank = True)
      name = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)

      def __str__(self) -> str:
            return f"{self.name.username} ---------> {self.designation}"
      

class assignements(models.Model):
      
      student = models.ForeignKey(Student,on_delete=models.CASCADE)
      submitted_to = models.ForeignKey("Assignmnet_given_by_teacher" , on_delete = models.CASCADE  , null = True)
      data = models.FileField(upload_to="./assignemnets", max_length=100 , blank=True , null=True)
      subject = models.ForeignKey(Subject , null = True , on_delete = models.CASCADE)
      is_draft = models.CharField( max_length = 24 , null = True)
      created_at = models.DateTimeField(auto_now_add=True , null = True)


      def __str__(self) -> str:
            return f"{self.student.name.username}--------->{self.submitted_to}------->{self.pk}------{self.student.pk}"



@receiver(post_save, sender=assignements)
def _post_save_assignment(sender,instance,created,**kwargs):
      if created:
             Grade.objects.create(value ="value" , assignement = instance , student = instance.student )
             assignmnets = Assignmnet_given_by_teacher.objects.filter(teacher_name = instance.submitted_to.teacher_name)
             val = Assignmnet_given_by_teacher.objects.filter(subject = instance.subject).first()
             val.data.add(instance)  



class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name="student_data")
    status = models.IntegerField(null=True, blank=True)
    no_of_classes_attended = models.IntegerField(default=0)
    updated_attendance = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        current_date = timezone.now().date()

        if self.pk is not None:
            previous = Attendance.objects.get(pk=self.pk)
            previous_date = previous.updated_attendance

            if previous_date is not None:
                if (current_date - previous_date).days < 1:
                    self.updated_attendance = previous_date
                else:
                    self.updated_attendance = current_date
                    self.subject.no_of_classes_occured += 1
            else:
                self.updated_attendance = current_date
                self.subject.no_of_classes_occured += 1
        else:
            self.updated_attendance = current_date
            self.subject.no_of_classes_occured += 1

        super().save(*args, **kwargs)

        if self.pk is not None:
            self.subject.save()

    def __str__(self):
        return f"{self.student}----{self.subject}------{self.no_of_classes_attended}"

      


class Grade(models.Model):
      value = models.CharField(max_length = 25 , null = True)
      assignement = models.ForeignKey(assignements ,on_delete = models.CASCADE , null = True , blank = True)
      student = models.ForeignKey(Student , on_delete = models.CASCADE , null = True , blank = True)


class Assignmnet_given_by_teacher(models.Model):

      title = models.CharField(max_length = 30)
      teacher_name = models.ForeignKey(staff_data , on_delete = models.CASCADE)
      data = models.ManyToManyField(assignements , blank = True)
      subject = models.ForeignKey(Subject , on_delete = models.CASCADE)


      def __str__(self) -> str:
            return f"{self.teacher_name.name.username} -----------> {self.subject}---------->{self.pk}"
      
class Assignment_uploaded(models.Model):
      For_data = models.ManyToManyField(Assignmnet_given_by_teacher,blank = True)
      name = models.ForeignKey(staff_data , on_delete = models.CASCADE)

      def __str__(self) -> str:
            return f"{self.name.name.username}"


@receiver(post_save, sender=Assignmnet_given_by_teacher)
def _post_save_assignment(sender,instance,created,**kwargs):
      if created:
            if  Assignment_uploaded.objects.filter(name = instance.teacher_name):
                 data =  Assignment_uploaded.objects.filter(name = instance.teacher_name).first()
                 data.For_data.add(instance)
                 data.save()
            else:
                 obj = Assignment_uploaded.objects.create(name = instance.teacher_name) 
                 obj.For_data.add(instance)
                 obj.save()




"""              
# TEACHER ------> ALL ASSIGNMENT POSTED BY HIM  ------> MANY TO MANY --------> STUDENT_ASSIGNMENT ----------> 
"""