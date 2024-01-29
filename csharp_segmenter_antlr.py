csharp = False

if csharp: 
    from language.csharp import CSharpCodeSegmenter
else: 
    import os 





# from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
# from parser.CSharpLexer import CSharpLexer
# from parser.CSharpParser import CSharpParser
# from parser.CSharpParserListener import CSharpParserListener
# from typing import List

# class CSharpSegmenter:
#     """Code segmenter for C# using ANTLR."""

#     def __init__(self, code: str):
#         self.code = code
#         self.source_lines = self.code.splitlines()

#     def is_valid(self) -> bool:
#         try:
#             input_stream = FileStream(self.code, encoding='utf-8-sig')
#             lexer = CSharpLexer(input_stream)
#             stream = CommonTokenStream(lexer)
#             parser = CSharpParser(stream)
#             parser.compilation_unit()
#             return True
#         except Exception:
#             return False

#     def extract_functions_classes(self) -> List[str]:
#         input_stream = FileStream(self.code, encoding='utf-8-sig')
#         lexer = CSharpLexer(input_stream)
#         stream = CommonTokenStream(lexer)
#         parser = CSharpParser(stream)
#         tree = parser.compilation_unit()

#         walker = ParseTreeWalker()
#         listener = CSharpExtractorListener(self.source_lines)
#         walker.walk(listener, tree)

#         return listener.extracted_elements

#     def simplify_code(self) -> str:
#         # Implement the code simplification logic here
#         # This may involve traversing the AST and replacing or omitting certain nodes
#         pass

# class CSharpExtractorListener(CSharpParserListener):
#     def __init__(self, source_lines):
#         self.source_lines = source_lines
#         self.extracted_elements = []

#     # Override methods from CSharpParserListener
#     def enterClassDefinition(self, ctx):
#         # Extract class definitions
#         start_line = ctx.start.line
#         end_line = ctx.stop.line
#         self.extracted_elements.append('\n'.join(self.source_lines[start_line-1:end_line]))

#     def enterMethodDefinition(self, ctx):
#         # Extract method definitions
#         start_line = ctx.start.line
#         end_line = ctx.stop.line
#         self.extracted_elements.append('\n'.join(self.source_lines[start_line-1:end_line]))

# # Example Usage
# code = r"C:\Users\aamir.ali\environments\lspclient\datasets\WebServices\HISApi\Source\HISApi\Controllers\Api\DrugsController.cs"
# segmenter = CSharpSegmenter(code)
# print(segmenter.extract_functions_classes())
