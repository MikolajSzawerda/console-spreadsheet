from src.Addresses import Address
from src.Spreadsheets import Spreadsheet
from config.commands_config import commands, commands_names
from src.Errors import NoTargetCommandAddressError
import re
from tokenize import tokenize, TokenInfo
from io import BytesIO


class CommandInterpreter():
    '''
    Class for handling different command in text form
    '''
    def __init__(self, spreadsheet: "Spreadsheet"):
        self._spreadsheet = spreadsheet

    @property
    def spreadsheet(self):
        return self._spreadsheet

    def parse_command(self, cmd: "str"):
        '''
        Function returns value from given address, or invokes function
        to handel arithmetic operations
        '''
        tokens = cmd.split('=')
        try:
            adr = Address(tokens[0])
        except IndexError:
            raise NoTargetCommandAddressError from IndexError
        if len(tokens) == 1:
            return self.spreadsheet.cell(adr).value
        response = self.execute_command(tokens[1])
        self.spreadsheet.set_cell_val(adr, response)
        return True

    def execute_command(self, command_stream: "str"):
        '''
        Function for handling arithmetic operations, or returning text
        '''
        try:
            return self._try_setting_text(command_stream)
        except AttributeError:
            pass
        if self._check_number(command_stream):
            number = 0
            if '.' in command_stream:
                number = float(command_stream)
            else:
                number = int(command_stream)
            return number
        tokens = self.split_tokens(command_stream)
        value = self._evaluate_expression(tokens)
        return value

    def _check_number(self, command_stream: "str"):
        check_if_number = re.compile('^-?\d*\.?\d*$')
        return bool(re.match(check_if_number, command_stream))

    def _try_setting_text(self, command_text: "str") -> "str":
        '''
        Function checks if given command is text, not an arithmetic
        '''
        check_if_text = re.compile('^\"(.*)\"$')
        return re.match(check_if_text, command_text).group(1)

    def split_tokens(self, command_stream: "str"):
        '''
        Function divide command into tokens easy to handle,
        and return token stack in RPN order
        '''
        tokenization = tokenize(
            BytesIO(command_stream.encode('utf-8')).readline
            )
        postfix_tokens = self._convert_to_postfix(tokenization)
        return postfix_tokens

    def _convert_to_postfix(self, tokens: "list[TokenInfo]"):
        '''
        Function orders tokens in RPN form
        Type:
            1 - address, command
            54 - operator
            2 - number
        '''
        output = []
        op_st = []
        for token in tokens:
            if token.type in [1, 2]:
                output.append(token)
            elif token.type == 54:
                if op_st:
                    output.append(op_st.pop())
                op_st.append(token)
        output.extend(op_st)
        return output

    def _evaluate_expression(self, tokens: "list[TokenInfo]"):
        '''
        Function evaluate math expression given in RPN form
        '''
        nb_stack = []
        for token in tokens:
            if token.type == 1:
                try:
                    adr = Address(token.string)
                    val = self.spreadsheet.cell(adr).value
                    nb_stack.append(val)
                except Exception:
                    pass
            elif token.type == 2:
                number = 0
                if '.' in token.string:
                    number = float(token.string)
                else:
                    number = int(token.string)
                nb_stack.append(number)
            elif token.type == 54:
                func = commands[token.string]
                val = func(nb_stack.pop(), nb_stack.pop())
                nb_stack.append(val)
        return nb_stack.pop()

    def _calculate_command(self, command, addres_range):
        pass
