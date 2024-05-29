#!/usr/bin/env python3

import argparse
import os

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

def main():
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

    args = parser.parse_args()

    if args.command == 'add':
        result = add(args.a, args.b)
        print(f"Wynik dodawania: {result}")
    elif args.command == 'subtract':
        result = subtract(args.a, args.b)
        print(f"Wynik odejmowania: {result}")
    elif args.command == 'init':
        gitlike_init(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
