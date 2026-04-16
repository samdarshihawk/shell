import sys
import os
import subprocess
import readline

builtin_commands = ["echo", "exit", "type", "pwd", "cd"]



def completer(text, state):
    """
    Readline completer for builtin commands.

    Called repeatedly with state=0, 1, 2, ... until it returns None.

    """

    if state == 0:
        completer._matches = [
            cmd + " " for cmd in builtin_commands if cmd.startswith(text)
        ]
    
    if state < len(completer._matches):
        return completer._matches[state]
    return None


completer._matches = []



def setup_readline():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    readline.set_completer_delims("\t\n")


def parse_arguments(command_line):
    args = []
    current = []
    i = 0
    n = len(command_line)

    in_single_quote = False
    in_double_quote = False

    stdout_file = None
    stderr_file = None
    stdout_mode = 'w'
    stderr_mode = 'w'
    redirect_pending = None  # None, 'stdout', or 'stderr'

    while i < n:
        ch = command_line[i]

        if in_single_quote:
            if ch == "'":
                in_single_quote = False
            else:
                current.append(ch)

        elif in_double_quote:
            if ch == '\\':
                if i + 1 < n and command_line[i + 1] in ('"', '\\'):
                    i += 1
                    current.append(command_line[i])
                else:
                    current.append(ch)
            elif ch == '"':
                in_double_quote = False
            else:
                current.append(ch)

        else:
            if ch == '\\':
                i += 1
                if i < n:
                    current.append(command_line[i])
            elif ch == '>':
                # Determine which fd is being redirected
                if current == ['2']:
                    current = []
                    redirect_type = 'stderr'
                elif current == ['1']:
                    current = []
                    redirect_type = 'stdout'
                else:
                    redirect_type = 'stdout'
                    if current:
                        # Finalize the current token before the redirect
                        if redirect_pending == 'stdout':
                            stdout_file = ''.join(current)
                        elif redirect_pending == 'stderr':
                            stderr_file = ''.join(current)
                        else:
                            args.append(''.join(current))
                        current = []

                if i + 1 < n and command_line[i + 1] == '>':
                    mode = 'a'
                    i += 1
                else:
                    mode = 'w'
                
                if redirect_type == 'stdout':
                    stdout_mode = mode
                else: 
                    stderr_mode = mode

                redirect_pending = redirect_type
            elif ch == "'":
                in_single_quote = True
            elif ch == '"':
                in_double_quote = True
            elif ch == ' ' or ch == '\t':
                if current:
                    if redirect_pending == 'stdout':
                        stdout_file = ''.join(current)
                        redirect_pending = None
                    elif redirect_pending == 'stderr':
                        stderr_file = ''.join(current)
                        redirect_pending = None
                    else:
                        args.append(''.join(current))
                    current = []
            else:
                current.append(ch)

        i += 1

    if in_single_quote or in_double_quote:
        raise ValueError("Unclosed quote")

    if current:
        if redirect_pending == 'stdout':
            stdout_file = ''.join(current)
        elif redirect_pending == 'stderr':
            stderr_file = ''.join(current)
        else:
            args.append(''.join(current))

    return args, stdout_file, stderr_file, stdout_mode, stderr_mode


def main():

    setup_readline()

    while True:

        command = input("$ ")
        # sys.stdout.write("$ ")
        # sys.stdout.flush()
        # command = input()

        try:
            parts, stdout_file, stderr_file, stdout_mode, stderr_mode = parse_arguments(command)
        except ValueError:
            print("syntax error: unclosed quote")
            continue

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        stdout_target = None
        stderr_target = None

        try:
            if stdout_file:
                try:
                    stdout_target = open(stdout_file, stdout_mode)
                except OSError as e:
                    print(f"shell: {stdout_file}: {e.strerror}")
                    continue

            if stderr_file:
                try:
                    stderr_target = open(stderr_file, stderr_mode)
                except OSError as e:
                    print(f"shell: {stderr_file}: {e.strerror}")
                    continue

            out = stdout_target if stdout_target else sys.stdout
            err = stderr_target if stderr_target else sys.stderr

            # Handle exit builtin
            if cmd == "exit":
                exit_code = int(args[0]) if args else 0
                sys.exit(exit_code)

            if cmd == "echo":
                print(' '.join(args), file=out)
                continue

            if cmd == "pwd":
                print(os.getcwd(), file=out)
                continue

            if cmd == "cd":
                path = args[0] if args else os.environ.get("HOME", "/")

                if path == "~":
                    path = os.environ.get("HOME", "/")

                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"cd: {path}: No such file or directory", file=err)
                except OSError as e:
                    print(f"cd: {path}: {e.strerror}", file=err)
                continue

            if cmd == "type":
                target = args[0] if args else ""
                if target in builtin_commands:
                    print(f"{target} is a shell builtin", file=out)
                else:
                    path_env = os.environ.get("PATH", "")
                    paths = path_env.split(os.pathsep)
                    found = False
                    for p in paths:
                        full_path = os.path.join(p, target)

                        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                            print(f"{target} is {full_path}", file=out)
                            found = True
                            break

                    if not found:
                        print(f"{target}: not found", file=err)

                continue

            try:
                subprocess.run(parts, stdout=stdout_target, stderr=stderr_target)
            except FileNotFoundError:
                print(f"{cmd}: command not found", file=err)

        finally:
            if stdout_target:
                stdout_target.close()
            if stderr_target:
                stderr_target.close()


if __name__ == "__main__":
    main()
