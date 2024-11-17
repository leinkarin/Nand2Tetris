"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing

from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

BIT_FORMAT = "015b"


def do_first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    """
    This function is responsible for the first pass of the assembler.
    :param parser: Parser object
    :param symbol_table: SymbolTable object
    """
    rom_address = 0

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, rom_address)
        else:
            rom_address += 1


def a_command_handler(parser: Parser, symbol_table: SymbolTable, output_file: typing.TextIO, var_address: int) -> int:
    """
    This function is responsible for handling A_COMMANDS
    :param parser: Parser object
    :param symbol_table: SymbolTable object
    :param output_file: output file
    :param var_address: the address of the variable
    :return: the updated var_address
    """
    symbol = parser.symbol()
    new_line = "0"

    if symbol.isdigit():
        new_line += format(int(symbol), BIT_FORMAT)

    else:
        if symbol_table.contains(symbol):
            new_line += format(symbol_table.get_address(symbol), BIT_FORMAT)

        else:
            symbol_table.add_entry(symbol, var_address)
            new_line += format(var_address, BIT_FORMAT)
            var_address += 1

    if parser.has_more_commands():
        new_line += "\n"

    output_file.write(new_line)
    return var_address


def c_command_handler(parser: Parser, output_file: typing.TextIO) -> None:
    """
    This function is responsible for handling C_COMMANDS
    :param parser: Parser object
    :param output_file: output file
    """
    comp_mnemonic = parser.comp()

    new_line = "101" if "<<" in comp_mnemonic or ">>" in comp_mnemonic else "111"
    new_line += Code.comp(comp_mnemonic) + Code.dest(parser.dest()) + Code.jump(parser.jump())
    if parser.has_more_commands():
        new_line += "\n"
    output_file.write(new_line)


def do_second_pass(parser: Parser, symbol_table: SymbolTable, output_file: typing.TextIO) -> None:
    """
    This function is responsible for the second pass of the assembler.
    :param parser: Parser object
    :param symbol_table: SymbolTable object
    :param output_file: output file
    """
    var_address = 16

    while parser.has_more_commands():
        parser.advance()

        if parser.command_type() == "A_COMMAND":
            var_address = a_command_handler(parser, symbol_table, output_file, var_address)

        if parser.command_type() == "C_COMMAND":
            c_command_handler(parser, output_file)


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    do_first_pass(parser, symbol_table)
    input_file.seek(0)
    parser_2 = Parser(input_file)
    do_second_pass(parser_2, symbol_table, output_file)


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
