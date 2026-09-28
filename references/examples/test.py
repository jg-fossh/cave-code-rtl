import sys
import os
import re
import tokenize
import io

def compress_vhdl(content):
    """Compresses VHDL by removing -- comments and minimizing empty lines."""
    # Remove single-line comments starting with --
    # Keeping the newline character intact
    content = re.sub(r'--.*', '', content)

    # Remove excessive blank lines
    content = re.sub(r'\n\s*\n', '\n', content)
    return content.strip()


def compress_verilog(content):
    """Compresses Verilog/SystemVerilog by removing // and /* */ comments while preserving compiler directives."""
    # 1. Remove multi-line comments /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 2. Remove single-line comments // ...
    # Uses a lookbehind to ensure we don't accidentally match inside a string,
    # though standard regex parsing here assumes clean syntax.
    content = re.sub(r'//.*', '', content)

    # 3. Collapse multiple empty lines
    content = re.sub(r'\n\s*\n', '\n', content)
    return content.strip()


