"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List
from xblock.fragment import Fragment

from courseware.courses import get_course_with_access
from django.contrib.auth.models import User
from lms.djangoapps.grades.new.course_grade import CourseGradeFactory
from opaque_keys.edx.keys import CourseKey
from django.template import Template, Context

class StudentReportXBlock(XBlock):
    """
    It displays student report.
    """
    icon_class = 'other'

    display_name = String(
        display_name = "XBlock Name",
        help = "This name appears in the horizontal navigation at the top of the page.",
        scope = Scope.settings,
        default = "Student Report",
    )
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the StudentReportXBlock, shown to students
        when viewing courses.
        """
        if getattr(self.xmodule_runtime, 'is_author_mode', False):
            
            html = Template(self.resource_string("static/html/student_report_author.html"))
            frag = Fragment(html.render(Context(context)))
            frag.add_css(self.resource_string("static/css/student_report.css"))
            frag.add_javascript(self.resource_string("static/js/src/student_report.js"))
            frag.initialize_js('StudentReportXBlock')
            
            return frag
            
        else:
            
            course_id = context['progress_url'].split("/courses/")[1].split('/progress')[0]
            course_key = CourseKey.from_string(course_id)
            student = User.objects.prefetch_related("groups").filter(username=context['username']).first()
            course = get_course_with_access(student, 'load', course_key, depth=None, check_if_enrolled=True)
            course_grade = CourseGradeFactory().create(student, course)
            grade_summary = course_grade.summary
            data_summary = []
            
            hide_result = False
            for summary in grade_summary['section_breakdown']:
                if summary.has_key('prominent'):
                    data_dict = {}
                    data_dict['label'] = summary['detail'].split("=")[0]
                    data_dict['percentage'] = summary['detail'].split("=")[1]
                    if not data_dict['percentage']:
                        hide_result = True
                        break
                    data_summary.append(data_dict)
            
            final_result = str(grade_summary['percent'] * 100.0) + '%'
            
            if student.first_name and student.last_name:
                student_name = student.first_name + ' ' + student.last_name
            else:
                student_name = student.username

            context['data_summary'] = data_summary
            context['final_result'] = final_result
            context['is_passed'] = course_grade.passed
            context['hide_result'] = hide_result
            html = Template(self.resource_string("static/html/student_report.html"))
            frag = Fragment(html.render(Context(context)))
            frag.add_css(self.resource_string("static/css/student_report.css"))
            frag.add_javascript(self.resource_string("static/js/src/student_report.js"))
            frag.initialize_js('StudentReportXBlock')
            
            return frag

    def studio_view(self, context=None):

        html = Template(self.resource_string("static/html/student_report_author.html"))
        frag = Fragment(html.render(Context(context)))
        frag.add_css(self.resource_string("static/css/student_report.css"))
        frag.add_javascript(self.resource_string("static/js/src/student_report.js"))
        frag.initialize_js('StudentReportXBlock')
        
        return frag

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("StudentReportXBlock",
             """<student_report/>
             """),
            ("Multiple StudentReportXBlock",
             """<vertical_demo>
                <student_report/>
                <student_report/>
                <student_report/>
                </vertical_demo>
             """),
        ]