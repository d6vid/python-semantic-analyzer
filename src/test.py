# 1. En general, las cosas solo aceptan valores unarios o binarios
import re
import os
from semantic_analyzer import SemanticAnalyzer
from general_helpers import get_information_from_txt

a = SemanticAnalyzer()
a.analyze_code(get_information_from_txt('src\code.txt'))
