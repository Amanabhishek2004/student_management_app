from rest_framework import serializers
from .models import *



class userserilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]




class StudentReadSerializer(serializers.ModelSerializer):
    Attendance_in_each_subject = serializers.SerializerMethodField(read_only=True)
    individual_data = serializers.SerializerMethodField(read_only=True)
    name = userserilizer()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "individual_data",
            "attendance_status",
            "Attendance_in_each_subject",
        ]

    def get_Attendance_in_each_subject(self, obj):
        qs = obj.subjects.all()
        Attendance_obj = Attendance.objects.filter(student = obj)
        data = []
        for subject in qs:
            record = {
                "attendance_id": Attendance_obj.filter(subject = subject).first().pk,
                "id":subject.pk,
                "subject_name": subject.name,
                "no_of_classes_occured": subject.no_of_classes_occured,
            }
            attendance_record = Attendance.objects.filter(
                student=obj, subject=subject
            ).first()
            if attendance_record:
                record["no_of_classes_attended"] = (
                    attendance_record.no_of_classes_attended
                )
            else:
                record["no_of_classes_attended"] = 0

            data.append(record)

        return data

    def get_individual_data(self, obj):
        pk = obj.pk
        return f"http://127.0.0.1:8000/api/students/{pk}/"
    
class Asssignment_given_by_teacher_Seriaizer(serializers.ModelSerializer):
    class Meta:
        model = Assignmnet_given_by_teacher
        fields = ["title", "id"]


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ["id", "value"]

class AssignmentSerializer(serializers.ModelSerializer):

    Assignment_status = serializers.SerializerMethodField(read_only = True)
    file_name = serializers.SerializerMethodField(read_only=True)
    data = serializers.FileField(write_only=True, required=False, allow_null=True)
    grade = serializers.SerializerMethodField(read_only=True)
    submitted_to = serializers.PrimaryKeyRelatedField(
    queryset=Assignmnet_given_by_teacher.objects.all() , required=False)


    class Meta:

        model = assignements
        
        fields = [
            "id",
            "student",
            "is_draft",
            "subject",
            "Assignment_status",
            "data",
            "grade",
            "file_name",
            "submitted_to",
        ]

    def get_file_name(self, obj):
        if obj.data:
            return obj.data.name

    def get_submitted_to(self, obj):
        return Asssignment_given_by_teacher_Seriaizer(obj.submitted_to).data

    def get_grade(self, obj):
        grade_instance = Grade.objects.filter(assignement=obj).first()
        if grade_instance:
            serialized_data = GradeSerializer(grade_instance)
            return serialized_data.data
        else:
            return "not given still"

    def get_Assignment_status(self, obj):
        print(obj)
        if obj.is_draft == "False":
            return "SUBMITTED"
        else:
            return "SUBMITTED AS DRAFT"
        

class StaffInlineSerializer(serializers.ModelSerializer):
       
       class Meta:
           model = staff_data
           fields = "__all__"       




class AssignmentGivenDataSerializer(serializers.ModelSerializer):


       teacher_data = serializers.SerializerMethodField(read_only = True)
       data  = serializers.SerializerMethodField(read_only = True)

       class Meta:
           model = Assignmnet_given_by_teacher
           fields = ['id',"title" ,"teacher_name", "teacher_data","data" , "id" , "subject"]    


       def get_data(self , obj):
            
            all_assignments = []

            for i in obj.data.all():
               all_assignments.append(AssignmentSerializer(i).data)    

            return all_assignments     
       
       def get_teacher_data(self , obj):
            
            return StaffInlineSerializer(obj.teacher_name).data

class AttendanceSerializer(serializers.ModelSerializer):

    no_of_classes_occured = serializers.SerializerMethodField(read_only = True)    

    class Meta:    
        model = Attendance
        fields = ["subject" , "student" , "no_of_classes_attended" , "no_of_classes_occured" ,"status"]

    def get_no_of_classes_occured(self , obj):
        subject = Subject.objects.get(id = obj.subject.pk)
        return subject.no_of_classes_occured    
    
