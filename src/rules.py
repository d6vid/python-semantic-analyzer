from enum import Enum

class Rules(Enum):
    # General
    VARIABLE_DECLARATION = r'\b\w+\s+\w+\s*=\s*\S+\b'
    VARIABLE_ASSIGNATION = r'\b\w+\s*=\s*\S+\b'
    FUNCTION_DECLARATION = r'\b(\w+)\s+(\w+)\s*\((.*?)\)\s*{'
    IF_STATEMENT = r'\bif\s*\([^)]*\)\s*{' # Necesita solo reconocer un corchete abierto
    WHILE_STATEMENT = r'\bwhile\s*\((?:[^()]|\([^()]*\))*\)\s*{' # Necesita solo reconocer un corchete abierto
    RETURN_STATEMENT = r'\breturn\s+\S+\b'
    END_SCOPE = r'\}'
    
    # Operaciones
    BINARY_OPERATION = r'\b(\w+)\s*([+\-*/%]|==|!=|<=|>=|<|>)\s*(\w+)\b'
    ARBITRARY_OPERATION = r'\b(\w+)\s*((?:[+\-*/%]|==|!=|<=|>=|<|>)\s*\w+\s*)+\b'
    
    # Valores
    INTEGER_LITERAL = r'^[-+]?[0-9]+$'
    STRING_LITERAL = r'(\'[^\']*\'|\"[^\"]*\")'
    FLOAT_LITERAL = r'\b(?:\d+\.\d*|\.\d+)(?:[eE][-+]?\d+)?\b'
