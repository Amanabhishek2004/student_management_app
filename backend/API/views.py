from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from.serializers import *
from .models import *
import datetime

# Create your views here.


class StudentListCreateView(generics.ListAPIView):
     
      queryset = Student.objects.all()
      serializer_class = StudentReadSerializer



class AssignmentViewAPI(generics.ListAPIView ,generics.CreateAPIView):
      queryset = assignements.objects.all()
      serializer_class = AssignmentSerializer
  
     # completed the creation as well as the duplicate data handling
 
      def create(self, request, *args, **kwargs):
            
            student_id =  int(self.request.data["student"])
            submitted_to = int(self.request.data["submitted_to"])

            object = Assignmnet_given_by_teacher.objects.get(id = submitted_to)
            
            for i in object.data.all():
                  if i.student.id ==  student_id:
                        return Response({
                     "Message":"You have already submitted the assignment"
                        })        
            
            return super().create(request, *args, **kwargs)
      



class AssignmnetUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
      queryset = assignements.objects.all()
      serializer_class = AssignmentSerializer


class AssignmentGivenDataAPI(generics.ListAPIView , generics.CreateAPIView):
    
    # This route will be designed both ways for listing all the data as well as listing specific subject data

      queryset = Assignmnet_given_by_teacher.objects.all()
      serializer_class = AssignmentGivenDataSerializer

      def get_queryset(self):
            
            subject = self.request.GET.get("subject")
            querysets = Assignmnet_given_by_teacher.objects.all()
            if subject:
                  subject_obj = Subject.objects.get(name = subject)
                  querysets = Assignmnet_given_by_teacher.objects.filter(subject = subject_obj)
            
            return querysets

class MarkAttendanceAPI(generics.RetrieveUpdateAPIView):

      queryset = Attendance.objects.all()
      serializer_class = AttendanceSerializer

      def update(self, request, *args, **kwargs):
            
            subject = self.request.GET.get("sub")
            student = self.request.GET.get("stu")
            data = int(self.request.GET.get("data"))

            obj = Attendance.objects.filter(subject__name = subject).filter(student__name__username = student).first()

            if obj.status == data and datetime.date.today() == obj.updated_attendance:
                     return Response({"message": "No changes in attendance status."}, status=status.HTTP_200_OK)
            
            if datetime.date.today() != obj.updated_attendance:              
                  obj.subject.no_of_classes_occured+=1

            if obj.status==1 and data == 1: 
                if datetime.date.today() != obj.updated_attendance:
                      obj.no_of_classes_attended+=1
                      obj.status = data
                      obj.save()
            if data !=obj.status:
                  # if datetime.date.today() == obj.updated_attendance:
                  obj.status = data                  
                  if data == 0:   
                      obj.no_of_classes_attended-=1      
                      obj.save()

                  if data == 1:
                        obj.no_of_classes_attended+=1
                        obj.save()
                            
            return super().update(request, *args, **kwargs)