from rules import Rules
from symbol_table_node import SymbolTableNode
from literals_mapping import references as GetLiteralRule
from general_helpers import remove_element_from_list, add_whitespace_between_specific_chars, get_last_element_that_is_not_specific_ones, get_type_of_value
import re

class SemanticAnalyzer:
    
    errors = ""  
    
    def __init__(self):
        self.current_symtable = SymbolTableNode()
        self.contexts = []

    def analyze_code(self, code):
        self.contexts.append("global")
        list_lines = code.splitlines()
        for line in list_lines:
            self.__analyze_line(line, list_lines.index(line)+1)
        print(SemanticAnalyzer.errors)

    def __analyze_line(self, line, line_number):
        processed_line = add_whitespace_between_specific_chars(line, {',','(', ')', '{', '}', '='})
        words = processed_line.split()

        # Validar el tipo de linea
        if re.search(Rules.VARIABLE_DECLARATION.value, line):
            
            # Agararrando data de linea (asume que en declaracion siempre hay asignacion)
            symbol = words[1]
            type = words[0]
            classification = "variable"

            # Si hay definicion ademas de declaracion
            if len(words) > 2:
                expression = words[3:]
                if len(expression) == 1:
                    entry_assign = self.current_symtable.lookup_symbol_upwards(expression[0])
                    if entry_assign is not None:
                        if not entry_assign["tipo"] == type:
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Asignacion incorrecta en declaracion de " + symbol  
                    else:
                        if get_type_of_value(expression[0]) is None:
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + expression[0] + " no esta declarado"
                        elif not re.search(GetLiteralRule[type].value, expression[0]):
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Asignacion incorrecta en declaracion de " + symbol     
                else:
                    self.__analize_binary_expression(type, expression, line_number)

            # Agregando data a SymTable
            self.current_symtable.add_entry_to_table(symbol, {symbol: {"tipo": type, "clasificacion": classification, "under_scope": self.__get_last_return_context()}})

        elif re.search(Rules.VARIABLE_ASSIGNATION.value, line):

            # Agararrando data de linea
            symbol_assigned = words[0]
            expression = words[2:]

            # Revisar si simbolo existe (y de paso traerme la referencia mas reciente)
            entry = self.current_symtable.lookup_symbol_upwards(symbol_assigned)
            if entry is not None:              
                # Analizar expresion
                if len(expression) == 1:
                    value = expression[0]
                    if not re.search(GetLiteralRule[entry["tipo"]].value, value) and self.current_symtable.lookup_symbol_upwards(value) is None:
                        SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Asignacion incorrecta de " + symbol_assigned               
                else:
                    self.__analize_binary_expression(entry["tipo"], expression, line_number) 

            else:
                SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + symbol_assigned + " no esta declarado"

        elif re.search(Rules.FUNCTION_DECLARATION.value, line):
            
            # Sacando valores
            symbol = words[1]
            type = words[0]
            classification = "function"
            parameters = words[words.index("(")+1:words.index(")")]
            parameters = remove_element_from_list(parameters, ",")

            # Agregar a la tabla de simbolos
            self.current_symtable.add_entry_to_table(symbol, {symbol: {"tipo": type, "clasificacion": classification, "under_scope": self.__get_last_return_context()}})
            
            # Entrando a nuevo scope (nueva tabla de simbolos)
            new_scope = self.current_symtable.add_child()
            self.current_symtable = new_scope
            self.contexts.append(symbol)
            for i in range(len(parameters)):
                if(parameters[i] in list(GetLiteralRule.keys())):
                    self.current_symtable.add_entry_to_table(parameters[i+1], {parameters[i+1]: {"tipo": parameters[i], "clasificacion": "variable", "under_scope": self.__get_last_return_context()}})

        elif re.search(Rules.IF_STATEMENT.value, line):
            expression = words[words.index("(")+1:words.index(")")]
            
            # Analizar si expresion booleana es valida
            self.__analize_binary_expression("bool", expression, line_number)

            # Entrando a nuevo scope (nueva tabla de simbolos)
            new_scope = self.current_symtable.add_child()
            self.current_symtable = new_scope
            self.contexts.append("if")

        elif re.search(Rules.WHILE_STATEMENT.value, line):
            expression = words[words.index("(")+1:words.index(")")]

            # Analizar si expresion booleana es valida
            self.__analize_binary_expression("bool", expression, line_number)

            # Entrando a nuevo scope (nueva tabla de simbolos)
            new_scope = self.current_symtable.add_child()
            self.current_symtable = new_scope
            self.contexts.append("while")

        elif re.search(Rules.RETURN_STATEMENT.value, line):
            
            # Revisar si funcion proxima deberia de retornar algo
            fn_to_verify = self.current_symtable.lookup_function_symbol_upwards(self.__get_last_return_context())
            return_flag = 1
            if fn_to_verify["tipo"] == "void" and len(words) > 1:
                SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Declaracion de retorno en funcion tipo void"
                return_flag = 0

            if return_flag == 1:
                # Obteniendo valor de retorno
                return_value = words[1:] if len(words) > 1 else None 

                # Si el valor de retorno es simple
                if return_value is not None and len(return_value) == 1:
                    return_value = return_value[0]

                    if self.current_symtable.lookup_symbol_upwards(return_value) is not None:
                        var_to_return = self.current_symtable.lookup_symbol_upwards(return_value)
                        if not var_to_return["tipo"] == fn_to_verify["tipo"]:
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Valor de retorno no coincide con la declaración de " + self.__get_last_return_context()    
                    else:
                        if get_type_of_value(return_value) is None:
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + return_value + " no esta declarado"
                        elif not re.search(GetLiteralRule[fn_to_verify["tipo"]].value, return_value):
                            SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "Valor de retorno no coincide con la declaración de " + self.__get_last_return_context()
                elif return_value is not None:
                    self.__analize_binary_expression(fn_to_verify["tipo"], return_value, line_number)

        elif re.search(Rules.END_SCOPE.value, line):
            
            # Matar el contexto actual
            self.current_symtable = self.current_symtable.get_father()
            self.contexts.pop()

    def __analize_binary_expression(self, type, expression, line_number):
        
        # Verificar el operando, segun el tipo de variable en donde se encuentra mencionado
        def verify_operand(variable_type, operand):
            if not re.search(GetLiteralRule[variable_type].value, operand):
                entry = self.current_symtable.lookup_symbol_upwards(operand)
                if entry is None:
                    SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + operand + " no es compatible con el tipo de variable"
                elif entry["tipo"] is not variable_type:
                    SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + operand + " no es del mismo tipo que la variable"
        
        op1 = expression[0]
        op2 = expression[2]

        if type is not 'bool':
            verify_operand(type, op1)
            verify_operand(type, op2)
        else:
            entry_op1 = self.current_symtable.lookup_symbol_upwards(op1)
            entry_op2 = self.current_symtable.lookup_symbol_upwards(op2)
            type_op1 = entry_op1["tipo"] if entry_op1 is not None else get_type_of_value(op1)
            type_op2 = entry_op2["tipo"] if entry_op2 is not None else get_type_of_value(op2)
            if type_op1 != type_op2:
                SemanticAnalyzer.errors = SemanticAnalyzer.errors + "\nError - Linea " + str(line_number) + ": " + "" + op1 + " no es del mismo tipo que " + op2

    def __get_last_return_context(self):
        return get_last_element_that_is_not_specific_ones(self.contexts,{'if','while'})