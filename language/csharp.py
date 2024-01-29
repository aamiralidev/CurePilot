import os
dotnet_path = os.path.expanduser('~/installations/dotnet/')
os.environ["DOTNET_ROOT"] = dotnet_path
from pythonnet import load 
load('coreclr')
import clr


def get_absolute_path(relative_path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)

clr.AddReference("System")
clr.AddReference(get_absolute_path("./dlls/Microsoft.CodeAnalysis.dll"))
clr.AddReference(get_absolute_path("./dlls/Microsoft.CodeAnalysis.CSharp.dll"))
clr.AddReference(get_absolute_path("./dlls/System.Runtime.CompilerServices.Unsafe.dll"))
clr.AddReference(get_absolute_path("./dlls/System.Numerics.Vectors.dll"))


from Microsoft.CodeAnalysis.CSharp import CSharpSyntaxTree, SyntaxKind
from Microsoft.CodeAnalysis.CSharp.Syntax import MethodDeclarationSyntax, ClassDeclarationSyntax, NamespaceDeclarationSyntax

from langchain_community.document_loaders.parsers.language.code_segmenter import (
    CodeSegmenter,
)

class CSharpSegmenter(CodeSegmenter):
    def __init__(self, code):
        super().__init__(code)
        self._code = code
        

    def extract_functions_classes(self):
        tree = CSharpSyntaxTree.ParseText(self._code)
        root = tree.GetRoot()
        functions_and_classes = []

        for member in root.Members:
            if isinstance(member, NamespaceDeclarationSyntax):
                for namespace_member in member.Members:
                    self.extract_member(namespace_member, functions_and_classes)
            else:
                self.extract_member(member, functions_and_classes)

        return functions_and_classes

    def extract_member(self, member, functions_and_classes):
        if isinstance(member, ClassDeclarationSyntax):
            functions_and_classes.append(member.ToString())
            for class_member in member.Members:
                if isinstance(class_member, MethodDeclarationSyntax):
                    functions_and_classes.append(class_member.ToString())
        elif isinstance(member, MethodDeclarationSyntax):
            functions_and_classes.append(member.ToString())

    def is_valid(self) -> bool:
        tree = CSharpSyntaxTree.ParseText(self._code)
        diagnostics = tree.GetDiagnostics()
        for diagnostic in diagnostics:
            if diagnostic.Severity == SyntaxKind.ErrorKeyword:
                return False
        return True
    
    def simplify_code(self):
        tree = CSharpSyntaxTree.ParseText(self._code)
        root = tree.GetRoot()
        simplified_code = []

        def extract_signature(node):
            def get_annotations(node):
                if len(list(node.AttributeLists)):
                    return '\n'.join([annotation.ToString() for annotation in node.AttributeLists])
                return None

            modifiers = ' '.join([mod.ToString() for mod in node.Modifiers])
            signature = None

            if isinstance(node, MethodDeclarationSyntax):
                return_type = node.ReturnType.ToString()
                annotations = get_annotations(node)
                if annotations:
                    signature = f"{annotations} \n{modifiers} {return_type} {node.Identifier.ValueText}{node.ParameterList}"
                else:
                    signature = f"{modifiers} {return_type} {node.Identifier.ValueText}{node.ParameterList}"

            elif isinstance(node, ClassDeclarationSyntax):
                annotations = get_annotations(node)
                if annotations:
                    signature = f"{annotations} \n{modifiers} {node.Identifier.ValueText}"
                else:
                    signature = f"{modifiers} {node.Identifier.ValueText}"

            return f"// Code for:\n{signature}" if signature else None


        def simplify_nodes(nodes):
            for node in nodes:
                signature = extract_signature(node)
                if signature:
                    simplified_code.append(signature)

                if isinstance(node, NamespaceDeclarationSyntax) or isinstance(node, ClassDeclarationSyntax):
                    simplify_nodes(node.Members)

        # Start recursive simplification from root
        simplify_nodes(root.Members)

        return "\n".join(simplified_code)





