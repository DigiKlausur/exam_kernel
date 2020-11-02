from .base import BaseTest
from textwrap import dedent
from jupyter_client import run_kernel

class TestBlockedMagics(BaseTest):

    def setUp(self):
        super().setUp()
        with open(self.config_file, 'w') as f:
            f.write(dedent('''
                c = get_config()

                c.ExamKernel.blocked_magics = ["time", "matplotlib", "config"]
            '''))

    def test_blocked_magics(self):
        for magic in ['time', 'matplotlib', 'config']:
            code = f'%%{magic}'
            with run_kernel(kernel_name='exam_kernel') as kc:
                msg_id = kc.execute(code)
                msg = kc.get_shell_msg(msg_id)
                content = msg['content']
                assert content['status'] == 'error'
                assert content['ename'] == 'ValueError'
                assert content['evalue'] == f'No magic named {magic} or {magic} blocked by kernel.'