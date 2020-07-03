from ipykernel.ipkernel import IPythonKernel
import re

class ExamKernel(IPythonKernel):
    implementation = 'Exam'
    implementation_version = '0.1'
    language = 'python'
    language_version = '3.6'
    language_info = {
        'name': 'python',
        'mimetype': 'text/plain',
        'extension': '.py',
    }
    banner = "Exam kernel - Restricted kernel for exams"

    def remove_empty_lines(self, code):
        '''
        Remove all empty lines at the beginning and end
        of the code snippet
        '''
        return code.strip('\n')

    def remove_terminal_commands(self, code):
        '''
        Remove all lines that start with an exclamation mark
        '''
        return re.sub(r'^!.*', '', code, flags=re.MULTILINE)

    def remove_magics(self, code):
        '''
        Remove all cell and line magics from the code
        '''
        # Cell magics
        code = re.sub(r'^\s*%%\w+', '', code)
        # Line magics
        code = re.sub(r'^\s*%\w+', '', code, flags=re.MULTILINE)
        return code

    def sanitize(self, code):
        '''
        Sanitize the code before executing it
        '''
        code = self.remove_empty_lines(code)
        code = self.remove_terminal_commands(code)
        code = self.remove_magics(code)
        return code

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        code = self.sanitize(code)
        return super().do_execute(code, silent, store_history, user_expressions, allow_stdin)