from .base import BaseTest
from textwrap import dedent
from jupyter_client import run_kernel

class TestBlockedImports(BaseTest):

    def setUp(self):
        super().setUp()
        with open(self.config_file, 'w') as f:
            f.write(dedent('''
                c = get_config()

                c.ExamKernel.blocked_imports = ["re", "math", "os"]
            '''))

    def test_blocked_import(self):
        for lib in ['re', 'math', 'os']:
            code = f'import {lib}'
            with run_kernel(kernel_name='exam_kernel') as kc:
                msg_id = kc.execute(code)
                msg = kc.get_shell_msg(msg_id)
                content = msg['content']
                assert content['status'] == 'error'
                assert content['ename'] == 'ModuleNotFoundError'
                assert content['evalue'] == f'No module named {lib} or {lib} blocked by kernel.'