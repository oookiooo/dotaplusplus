#!/usr/bin/env python3

import argparse
import os
import filecmp
import difflib
from colorama import init, Fore, Style

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def gitlike_init(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        init_file_path = os.path.join(path, '.gitlikeinit')
        with open(init_file_path, 'w') as f:
            f.write('Gitlike repository initialized.')
        print(f'Initialized empty Gitlike repository in {path}')
    except Exception as e:
        print(f'Error initializing Gitlike repository: {e}')

def gitlike_diff(dir1, dir2):
    try:
        diff = filecmp.dircmp(dir1, dir2)
        print_diff_files(diff)
    except Exception as e:
        print(f'Error comparing directories: {e}')

def print_diff_files(diff):
    for file_name in diff.diff_files:
        print(f'Different file: {file_name}')
        file1_path = os.path.join(diff.left, file_name)
        file2_path = os.path.join(diff.right, file_name)
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()
            for line in difflib.unified_diff(file1_lines, file2_lines, fromfile=file1_path, tofile=file2_path):
                if line.startswith('-'):
                    print(Fore.RED + line + Style.RESET_ALL, end='')
                elif line.startswith('+'):
                    print(Fore.BLUE + line + Style.RESET_ALL, end='')
                else:
                    print(line, end='')

    for sub_diff in diff.subdirs.values():
        print_diff_files(sub_diff)

def main():
    # Initialize colorama
    init(autoreset=True)

    parser = argparse.ArgumentParser(description="Prosty kalkulator CLI i narzędzie Gitlike")
    subparsers = parser.add_subparsers(dest='command', help='Dostępne polecenia')

    # Subparser for the add command
    parser_add = subparsers.add_parser('add', help='Dodaj dwie liczby')
    parser_add.add_argument('a', type=int, help='Pierwsza liczba')
    parser_add.add_argument('b', type=int, help='Druga liczba')

    # Subparser for the subtract command
    parser_subtract = subparsers.add_parser('subtract', help='Odejmij dwie liczby')
    parser_subtract.add_argument('a', type=int, help='Pierwsza liczba')
    parser_subtract.add_argument('b', type=int, help='Druga liczba')

    # Subparser for the gitlike init command
    parser_init = subparsers.add_parser('init', help='Inicjalizuj pusty Gitlike repozytorium')
    parser_init.add_argument('path', type=str, help='Ścieżka do katalogu')

    # Subparser for the gitlike diff command
    parser_diff = subparsers.add_parser('diff', help='Porównaj pliki w dwóch katalogach')
    parser_diff.add_argument('dir1', type=str, help='Ścieżka do pierwszego katalogu')
    parser_diff.add_argument('dir2', type=str, help='Ścieżka do drugiego katalogu')

    args = parser.parse_args()

    if args.command == 'add':
        result = add(args.a, args.b)
        print(f"Wynik dodawania: {result}")
    elif args.command == 'subtract':
        result = subtract(args.a, args.b)
        print(f"Wynik odejmowania: {result}")
    elif args.command == 'init':
        gitlike_init(args.path)
    elif args.command == 'diff':
        gitlike_diff(args.dir1, args.dir2)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
