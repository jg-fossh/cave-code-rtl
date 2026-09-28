import sys
import os
import re
import io

def compress_tcl_do(code: str) -> str:
    """
    Compress Tcl/.do code by removing comments and minimizing whitespace.
    """
    lines = code.splitlines()
    compress_lines = []
    
    for line in lines:
        stripped = line.strip()

        # 1. Skip completely empty lines
        if not stripped:
            continue

        # 2. Remove full-line comments
        if stripped.startswith('#'):
            continue

        # 3. Handle inline comments safely
        # In Tcl, an inline comment must be preceded by a semicolon or space
        if '#' in stripped:
            # Split at '#' only if preceded by whitespace or a semicolon
            parts = re.split(r'(?<=[\s;])#', stripped, maxsplit=1)
            stripped = parts[0].strip()

        # 4. Remove extra whitespace but preserve command structure
        if stripped:  # Only process non-empty lines
            # Collapse multiple spaces to single space
            stripped = re.sub(r'\s+', ' ', stripped)
            compress_lines.append(stripped)
    
    # Join with a single newline to preserve command structure
    return '\n'.join(compress_lines)


def compress_cpp(code: str) -> str:
    """
    Compresses C++ code to drastically reduce token usage while maintaining 
    full logic and syntactical validity.
    """
    # 1. Remove multi-line comments (/* ... */)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # 2. Remove single-line comments (// ...)
    lines = code.splitlines()
    clean_lines = []
    for line in lines:
        if '//' in line and '"' not in line:
            line = line.split('//')[0]
        clean_lines.append(line)
    code = '\n'.join(clean_lines)

    # 3. Collapse multiple blank lines into a single newline
    code = re.sub(r'\n\s*\n', '\n', code)
    
    # 4. Split into lines and process
    lines = [line.strip() for line in code.splitlines()]
    
    # 5. Separate preprocessor directives from the rest of the code
    include_lines = []
    main_code_parts = []
    
    for line in lines:
        if line.startswith('#'):
            include_lines.append(line)
        else:
            # Remove spaces around tokens: { } ( ) , ; = + - * / < > :
            if line:  # Only process non-empty lines
                line = re.sub(r'\s*([{}()\[\],;=+\-*/<>:])\s*', r'\1', line)
                main_code_parts.append(line)
    
    # Join the main code parts together (compressed)
    compressed_main = ''.join(main_code_parts)
    
    # Combine includes and compressed main function
    result_lines = include_lines + [compressed_main]
    
    # Join everything into one line (this is what makes it a single-line compressed output)
    return ''.join(result_lines)


def compress_vhdl(content: str) -> str:
    """Compresses VHDL by removing -- comments and minimizing empty lines."""
    # Remove single-line comments starting with --
    content = re.sub(r'--.*', '', content)

    # Remove excessive blank lines
    content = re.sub(r'\n\s*\n', '\n', content)
    
    # Remove extra whitespace around operators and parentheses
    content = re.sub(r'\s*([{};:,+\-*/<>])\s*', r'\1', content)
    
    # Keep some spacing for readability but minimize overall
    content = re.sub(r'\s*=\s*', '=', content)
    
    # Collapse multiple spaces into single space
    content = re.sub(r'\s+', ' ', content)
    
    # Remove all remaining newlines to create a single line
    content = content.replace('\n', '')
    
    return content.strip()


def compress_verilog(content: str) -> str:
    """Compresses Verilog/SystemVerilog by removing // and /* */ comments while preserving compiler directives."""
    # 1. Remove multi-line comments /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 2. Remove single-line comments // ...
    content = re.sub(r'//.*', '', content)

    # 3. Collapse multiple empty lines
    content = re.sub(r'\n\s*\n', '\n', content)
    
    # 4. Remove extra whitespace around most operators and parentheses
    content = re.sub(r'\s*([{};:,+\-*/<>])\s*', r'\1', content)
    
    # 5. Keep some spacing for readability
    content = re.sub(r'\s*=\s*', '=', content)
    
    # 6. Collapse multiple spaces into single space
    content = re.sub(r'\s+', ' ', content)
    
    # 7. Remove all remaining newlines to create a single line
    content = content.replace('\n', '')
    
    return content.strip()


def compress_python(content: str) -> str:
    """Safely removes comments and docstrings from Python code."""
    # Split into lines for processing
    lines = content.split('\n')
    result_lines = []
    
    # Track if we're inside a multi-line string
    in_multiline_string = False
    multiline_delimiter = ""
    
    for line in lines:
        # Check if this line starts a multi-line string
        stripped_line = line.strip()
        
        # Handle multi-line strings properly
        if not in_multiline_string and (stripped_line.startswith('"""') or stripped_line.startswith("'''")):
            # This line starts a multi-line string
            if stripped_line.count('"""') == 1 or stripped_line.count("'''") == 1:
                # Odd number means it's starting and ending on same line
                if (stripped_line.startswith('"""') and stripped_line.endswith('"""')) or \
                   (stripped_line.startswith("'''") and stripped_line.endswith("'''")):
                    # Single line docstring - skip the whole line
                    continue
                else:
                    # Multi-line string starting
                    in_multiline_string = True
                    multiline_delimiter = '"""' if stripped_line.startswith('"""') else "'''"
                    # Check if it ends on this same line too
                    if (multiline_delimiter == '"""' and stripped_line.count('"""') == 2) or \
                       (multiline_delimiter == "'''" and stripped_line.count("'''") == 2):
                        in_multiline_string = False
                    continue
            else:
                # Multi-line string starting but already ending on this line
                continue
        
        elif in_multiline_string:
            # Check if we're ending the multi-line string
            if (multiline_delimiter == '"""' and stripped_line.endswith('"""')) or \
               (multiline_delimiter == "'''" and stripped_line.endswith("'''")):
                in_multiline_string = False
            continue
        
        # Skip lines that are just comments
        if stripped_line.startswith('#'):
            continue
            
        # Remove inline comments from lines that contain code
        # Find the first # that's not inside a string
        comment_start = line.find('#')
        if comment_start != -1:
            # Check if the # is inside a string by looking at quotes before it
            quote_count = 0
            in_string = False
            for i, char in enumerate(line[:comment_start]):
                if char == '"' or char == "'":
                    if not in_string:
                        in_string = True
                        quote_count = 1
                    elif line[i-1] != '\\' and quote_count == 1:
                        in_string = False
                        quote_count = 0
                    else:
                        quote_count += 1
                elif char == '"' or char == "'":
                    if not in_string:
                        in_string = True
                        quote_count = 1
                    elif line[i-1] != '\\' and quote_count == 1:
                        in_string = False
                        quote_count = 0
                    else:
                        quote_count += 1
            
            # If we're not inside a string, remove the comment
            if not in_string:
                line = line[:comment_start]
        
        # Add non-empty lines to result
        if line.strip():
            result_lines.append(line)
    
    # Join and clean up extra whitespace
    return '\n'.join(result_lines).strip()



def main():
    if len(sys.argv) < 2:
        # If not enough  arguments
        print("Usage: python compress_hdl.py <file_path_or_directory>")
        sys.exit(1)

    # grab the file or path
    target_path = sys.argv[1]

    if os.path.isfile(target_path):
        files = [target_path]
    elif os.path.isdir(target_path):
        files = [os.path.join(root, f) for root, _, filenames in os.walk(target_path) 
                 for f in filenames if f.endswith(('.v', '.sv', '.vh', '.svh', '.vhd', '.vhdl', '.cc', '.hh', '.cpp', '.hpp', '.cxx', '.c', '.h', '.py'))]
    else:
        print(f"Error: Path '{target_path}' not found.")
        sys.exit(1)

    total_orig_chars = 0
    total_comp_chars = 0

    # iterate over the file or path
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_code = f.read()
            
            base, ext = os.path.splitext(file_path)

            if ext in ['.vhd', '.vhdl']:
                compressed_code = compress_vhdl(original_code)

            elif ext in ['.v', '.sv', '.vh', '.svh']:
                compressed_code = compress_verilog(original_code)

            elif ext in ['.py']:
                compressed_code = compress_python(original_code)

            elif ext in ['.c', '.h', '.cc', '.hh', '.cpp', '.hpp', '.cxx']:
                compressed_code = compress_cpp(original_code)

            elif ext in ['.tcl', '.do']:
                compressed_code = compress_tcl_do(original_code)

            else:
                print(f"Unsupported extension '{ext}'. Only .tcl, .do, .vhd, .vhdl, .v, .sv, .vh, .svh, .c, .h, .cpp, .hpp and .py are supported.")
                sys.exit(1)
            
            # Save the compressed file with a .min suffix next to the original
            output_path = f"{base}-compressed{ext}"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(compressed_code)
                
            orig_len = len(original_code)
            comp_len = len(compressed_code)
            total_orig_chars += orig_len
            total_comp_chars += comp_len
            
            saved_pct = ((orig_len - comp_len) / orig_len) * 100 if orig_len > 0 else 0
            # print(f"Compressed: {os.path.basename(file_path)} -> {os.path.basename(output_path)} (-{saved_pct:.1f}% chars)")
            
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    if total_orig_chars > 0:
        overall_saved = ((total_orig_chars - total_comp_chars) / total_orig_chars) * 100
        print(f"Done! Total character reduction: ~{overall_saved:.1f}% (Rough token savings).")


if __name__ == "__main__":
    main()
