# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:30:42 2017

@author: Mutni
"""

import unittest
from prettytable import PrettyTable
from collections import defaultdict

class Repository():
    def __init__(self):
        self.student = dict() #CWID is the key and instance of Student is the value
        self.instructor = dict() #CWID is the key and instance of instructors is the value
        self.grades = list()
        self.majors = defaultdict(set)
        self.read_student()
        self.read_instructor()
        self.read_grades()
        self.read_majors()
        self.process_grades()
        self.student_summary()
        self.instructor_summary()
        
    def read_student(self):
        try:
            f = open('students.txt', 'r')
        except FileNotFoundError:
            print("Can’t open students")
        else:
           with f:
               for line in f:
                   CWID, name, major = line.strip().split('\t')
                   self.student[CWID] = Student(CWID,name,major)

                   
    def read_instructor(self):
        try:
            f = open('instructors.txt', 'r')
        except FileNotFoundError:
            print("Can’t open instructors")
        else:
            with f:
                for line in f:
                    CWID, name, depart = line.strip().split('\t')
                    self.instructor[CWID] = Instructor(CWID, name,depart)

    def read_grades(self):
       try:
           f = open('grades.txt', 'r')
       except FileNotFoundError:
           print("Can’t open grades")
       else:
            with f:
                for line in f:
                    CWID ,coursename, LetterGrade, InstructorCWID = line.strip().split('\t')
                    self.grades.append(Grades(CWID,coursename,LetterGrade,InstructorCWID))

    def read_majors(self):
       try:
           f = open('majors.txt', 'r')
       except FileNotFoundError:
           print("Can’t open majors")
       else:
            with f:
                for line in f:
                    major, Course = line.strip().split('\t')
                    self.majors[major].add(Course)

    def student_summary(self):
            pt=PrettyTable(field_names = ['CWID', 'Name','Completed Courses', 'Remaining Courses'])
            for student in self.student.values():
                taken = student.courses_taken()
                required = self.majors[student.Major]
                pt.add_row([student.CWID, student.Name,taken,  sorted(required.difference(taken)) ])
            print(pt)
        
    def instructor_summary(self):
            ptt = PrettyTable(field_names = ['CWID', 'Name', 'Dept','Course',' Students'])
            for instructor in self.instructor.values():
                for taught in  instructor.coursesTaught:
                    ptt.add_row([instructor.CWID, instructor.Name, instructor.Department, taught,  instructor.coursesTaught[taught]])
            print(ptt)
            

    def process_grades(self):
        for grade in self.grades:
           CWID = grade.StudentCWID
           course = grade.coursename
           lettergrade = grade.LetterGrade
           inst = grade.InstructorCWID
           self.student[CWID].add_course(course, lettergrade)
           self.instructor[inst].add_course(course)

            
class Student():
    def __init__(self,CWID,Name, Major):
        self.CWID = CWID
        self.Name = Name
        self.Major = Major
        self.Takencourse = dict()# key is course name and the  value is grade 
        
    def courses_taken(self):
        return sorted(self.Takencourse.keys())
    
    def add_course(self, name, grade):
        self.Takencourse[name] = grade


class Instructor():
    def __init__(self , CWID, Name, Department ):
        self.CWID=CWID
        self.Name = Name
        self.Department = Department
        self.coursesTaught = defaultdict(int)# key is course name and vale is number of student 

    def courses_taught(self):
        return self.coursesTaught.keys()
    
    def add_course(self, name):
        self.coursesTaught[name] += 1
        
class Grades():
    def __init__(self, StudentCWID ,coursename, LetterGrade, InstructorCWID):
        self.StudentCWID = StudentCWID
        self.coursename = coursename
        self.LetterGrade = LetterGrade
        self.InstructorCWID = InstructorCWID


        

class FilesTest(unittest.TestCase):
     def test_repository(self):
         r = Repository()
         self.assertEqual(r.student['11788'].courses_taken(), ['SSW 540'])
         self.assertEqual(r.instructor['98765'].coursesTaught['SSW 567'], 4)
 

        
def main():
    Repository()
        

         
if __name__ == '__main__':
    main()
    unittest.main(exit = False, verbosity = 2)