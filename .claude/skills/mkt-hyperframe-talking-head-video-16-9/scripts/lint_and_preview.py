#!/usr/bin/env python3
"""Run `npx hyperframes lint`, then start `npx hyperframes preview` in
background and print the Studio URL.

Usage:
    python3 lint_and_preview.py --workspace <folder>
    python3 lint_and_preview.py --workspace <folder> --no-preview
"""
import argparse
import subprocess
import sys
from pathlib import Path


def run_lint(workspace: Path) -> int:
    print(f'[lint] cd {workspace}; npx hyperframes lint')
    proc = subprocess.run(
        ['npx', 'hyperframes', 'lint'],
        cwd=str(workspace),
        capture_output=True, text=True,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def start_preview(workspace: Path):
    print(f'[preview] starting `npx hyperframes preview` in background…')
    # Detach so script returns immediately.
    proc = subprocess.Popen(
        ['npx', 'hyperframes', 'preview'],
        cwd=str(workspace),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print(f'[preview] PID {proc.pid} — Studio likely at http://localhost:3002')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--no-preview', action='store_true', help='Lint only, skip preview')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()

    rc = run_lint(workspace)
    if rc != 0:
        print(f'[lint] FAILED with code {rc}. Fix errors before previewing.', file=sys.stderr)
        sys.exit(rc)

    print(f'[lint] OK')

    if args.no_preview:
        return

    start_preview(workspace)
    print('\n## Preview Studio')
    print('URL: http://localhost:3002')
    print('Hand-off complete. Refresh Studio to scrub timeline.')


if __name__ == '__main__':
    main()
