from ipykernel.ipkernel import IPythonKernel
from traitlets.config import LoggingConfigurable
from traitlets import List, Unicode
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

    allowed_imports = List([], help='The imports that can be used', config=True)
    blocked_imports = List([], help='The imports that are blocked. If allowed_imports is not empty it supercedes this', config=True)
    init_code = Unicode('', help='The code that should always be executed when the kernel is loaded.', config=True)

    def __init__(self, **kwargs):
        super(ExamKernel, self).__init__(**kwargs)
        self.standard_import = re.compile(r'^\s*import\s+(\w+)', flags=re.MULTILINE)
        self.from_import = re.compile(r'^\s*from\s+(\w+)', flags=re.MULTILINE)
        self.blocked_imports.append('importlib')
        self.init_kernel()  

    def init_kernel(self):
        '''
        Execute the init_code at when the kernel is loaded
        '''
        super().do_execute(self.init_code, silent=False)

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

    def find_import(self, line):
        match = self.standard_import.match(line) or self.from_import.match(line)
        if match:
            return match.group(1).strip()

    def sanitize_imports(self, code):

        if len(self.allowed_imports) == 0 and len(self.blocked_imports) == 0:
            return code

        sanitized = []
        if len(self.allowed_imports) > 0:            
            for line in code.split('\n'):
                lib = self.find_import(line)
                if lib and lib not in self.allowed_imports:
                    line = "raise ModuleNotFoundError('No module named {0} or {0} blocked by kernel.')".format(lib)
                sanitized.append(line)
        else:
            for line in code.split('\n'):
                lib = self.find_import(line)
                if lib and lib in self.blocked_imports:
                    line = "raise ModuleNotFoundError('No module named {0} or {0} blocked by kernel.')".format(lib)
                sanitized.append(line)
        return '\n'.join(sanitized)

    def sanitize(self, code):
        '''
        Sanitize the code before executing it
        '''
        code = self.remove_empty_lines(code)
        code = self.remove_terminal_commands(code)
        code = self.remove_magics(code)
        code = self.sanitize_imports(code)
        return code

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        code = self.sanitize(code)
        return super().do_execute(code, silent, store_history, user_expressions, allow_stdin)