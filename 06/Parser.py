"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from typing import List


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        lines = []

        for line in input_file.readlines():
            stripped_line = line.strip().replace(" ", "")
            lines.append(stripped_line)

        self.filter_command_lines_in_place(lines)
        self._all_lines = lines
        self._curr_line = ""
        self._curr_line_ind = -1

    # this is a helper for the constractor
    def filter_command_lines_in_place(self, lines: List[str]) -> None:
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("//") or line == '':
                lines.pop(i)
            elif "//" in line:
                lines[i] = line[:line.find("//")].strip()
                i += 1
            else:
                i += 1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return len(self._all_lines) - (self._curr_line_ind + 1) > 0

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if not self.has_more_commands():
            return None
        self._curr_line_ind += 1
        self._curr_line = self._all_lines[self._curr_line_ind]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        command_types = {
            "@": "A_COMMAND",
            "(": "L_COMMAND"
        }

        first_char = self._curr_line[0]

        return command_types.get(first_char, "C_COMMAND")

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        command = self.command_type()
        if command == "A_COMMAND":
            return self._curr_line[1:]
        elif command == "L_COMMAND":
            return self._curr_line[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type() != "C_COMMAND":
            return "not a c-command!"
        return self._curr_line.split("=")[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if "=" in self._curr_line:
            return self._curr_line.split("=")[1].split(";")[0].replace(" ", "")
        else:
            return self._curr_line.split(";")[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if ";" in self._curr_line:
            return self._curr_line.split(";")[1]
        return "null"
