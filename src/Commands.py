from src.Addresses import Address, RangeAddress
from src.Spreadsheets import Spreadsheet
from src.Cells import Cell
from config.commands_config import commands, commands_names, precedence
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
        tokens = cmd.split('=', maxsplit=1)
        try:
            adr = Address(tokens[0])
        except IndexError:
            raise NoTargetCommandAddressError from IndexError
        if len(tokens) == 1:
            return self.spreadsheet.cell(adr).value
        cell = Cell(adr)
        cell._raw_data = tokens[1]
        response = self.execute_command(tokens[1]) if tokens[1] else ''
        cell.value = response
        self.spreadsheet.add_cells([cell])
        self.update()
        return True

    def execute_command(self, command_stream: "str"):
        '''
        Function for handling arithmetic operations, or returning text/number
        '''
        if command_stream[0] == '=':
            tokens = self.split_tokens(command_stream[1:])
            return self._evaluate_expression(tokens)
        else:
            try:
                return self._convert_str_to_number(command_stream)
            except ValueError:
                return command_stream

    def update(self):
        '''
        Function recalculates all cells in spreadsheet
        '''
        for cell in self.spreadsheet.cells.values():
            cell.value = self.execute_command(cell._raw_data)

    def _check_number(self, command_stream: "str"):
        '''
        Function checks if command is just a number
        '''
        check_if_number = re.compile('^-?\d*\.?\d*$')
        return bool(re.match(check_if_number, command_stream))

    def _try_setting_text(self, command_text: "str") -> "str":
        '''
        Function checks if given command is text, not an arithmetic
        '''
        check_if_text = re.compile('^\"(.*)\"$')
        return re.match(check_if_text, command_text).group(0)

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
                if token.string in commands_names:
                    token = self._shell_command_data(token, tokens)
                output.append(token)
            elif token.type == 54:
                opr = token.string
                if opr == '(':
                    op_st.append(token)
                elif opr == ')':
                    while op_st and op_st[-1].string != '(':
                        output.append(op_st.pop())

                    op_st.pop()
                else:
                    try:
                        last_operator = op_st[-1].string
                    except IndexError:
                        last_operator = 0
                    if precedence[opr] > precedence.get(last_operator, 0):
                        op_st.append(token)
                    else:
                        while op_st and precedence[opr] <= precedence.get(last_operator, 0):
                            output.append(op_st.pop())
                            try:
                                last_operator = op_st[-1].string
                            except IndexError:
                                last_operator = 0
                        op_st.append(token)
        if op_st:
            output.extend(op_st[::-1])
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
                number = self._convert_str_to_number(token.string)
                nb_stack.append(number)
            elif token.type == 54:
                func = commands[token.string]
                val = func(nb_stack.pop(), nb_stack.pop())
                nb_stack.append(val)
        return nb_stack.pop()

    def _shell_command_data(self, token: "TokenInfo", tokens: "list[TokenInfo]"):
        '''
        Function shells needed data to calculate a command
        '''
        tp, start, end, ln = 2, token.start, token.end, token.line
        func = commands[token.string]
        next(tokens)
        adrA = next(tokens)
        next(tokens)
        adrB = next(tokens)
        next(tokens)
        range_adr = RangeAddress(Address(adrA.string),
                                 Address(adrB.string))
        val = self._calculate_command(func, range_adr)
        token = TokenInfo(tp, val, start, end, ln)
        return token

    def _calculate_command(self, command, addres_range: "RangeAddress"):
        '''
        Function takes values from spreadsheet, and applay numeric function
        '''
        adr = addres_range.addresses
        values = [self.spreadsheet.cell(x).value for x in adr]
        return str(command(values))

    def _convert_str_to_number(self, text_number: "str"):
        '''
        Function converts string number for the most suitble data type
        '''
        number = 0
        if '.' in text_number:
            mantisa = text_number.split('.')[1]
            if int(mantisa) == 0:
                number = int(text_number)
            else:
                number = float(text_number)
        else:
            number = int(text_number)
        return number
