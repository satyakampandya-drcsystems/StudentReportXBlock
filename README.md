# StudentReportXBlock
open edX XBlock to show the student report for the course.

# Usecase:
open edX allows any Instructor to hide the progress tab so as an Instructor if you want your students can see the their grade report at the end of the course (Assuming section prerequisite has been set) then you may add this XBlock as last component on last unit of the last section.

# How to Install (For sysadmin):
pip install git+https://github.com/naresh21/StudentReportXBlock.git#egg=student_report-xblock


# How to use (For Instructor):
- Go to studio
- Select your course
- Go to advanced settings
- Add "student_report" to Advanced Module List and save changes
- Go to outline where you want to add this XBlock
- From Advanced select "Student Report"

Thats it !!
