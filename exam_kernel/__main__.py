import argparse
import os
import sys
from textwrap import dedent
from jupyter_client.kernelspec import KernelSpecManager

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

class KernelManager:

    def __init__(self):
        parser = argparse.ArgumentParser(description='ExamKernel manager.',
        usage=dedent('''
                python -m exam_kernel <command> [<args>]

                Available sub commands are:
                  install    install the kernel
                  uninstall  uninstall the kernel
            '''))

        parser.add_argument('command', help='Subcommand to run')
        parser.add_argument('--sys-prefix', action='store_true', help='If the kernel should be install to sys.prefix')
        parser.add_argument('--user', action='store_true', help='If the kernel should be to the user space')

        args = parser.parse_args(sys.argv[1:])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        if args.sys_prefix:
            args.prefix = sys.prefix
        if not args.prefix and not _is_root():
            args.user = True
        getattr(self, args.command)(prefix=args.prefix, user=args.user)

    def install(self, prefix=None, user=True):
        path = KernelSpecManager().install_kernel_spec(
            os.path.dirname(__file__),
            user=user, 
            prefix=prefix
        )
        print(f'Install kernel to {path}')

if __name__ == '__main__':
    KernelManager()