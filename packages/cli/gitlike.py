#!/usr/bin/env python3

import argparse

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def main():
    parser = argparse.ArgumentParser(description="Prosty kalkulator CLI")
    subparsers = parser.add_subparsers(dest='command', help='Dostępne polecenia')

    parser_add = subparsers.add_parser('add', help='Dodaj dwie liczby')
    parser_add.add_argument('a', type=int, help='Pierwsza liczba')
    parser_add.add_argument('b', type=int, help='Druga liczba')

    parser_subtract = subparsers.add_parser('subtract', help='Odejmij dwie liczby')
    parser_subtract.add_argument('a', type=int, help='Pierwsza liczba')
    parser_subtract.add_argument('b', type=int, help='Druga liczba')

    args = parser.parse_args()

    if args.command == 'add':
        result = add(args.a, args.b)
        print(f"Wynik dodawania: {result}")
    elif args.command == 'subtract':
        result = subtract(args.a, args.b)
        print(f"Wynik odejmowania: {result}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
