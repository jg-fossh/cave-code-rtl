# Cave Code RTL

Compress code by removing comments and spaces to reduce token usage for AI prompts. This tool helps RTL and firmware engineers save on input tokens when analyzing or working with source files.

## Project Overview

A token compression tool that removes comments and unnecessary whitespace from RTL (Register Transfer Level) and firmware code files, reducing context window usage in AI coding agents.

## Dev Setup

Install Python 3.6+ to use the compression script:

```bash
# Clone this repository
git clone https://github.com/jg-fossh/cave-code-rtl.git
cd cave-code-rtl
```

## Project Structure

```bash
cave-code-rtl/
├─ scripts/
│ └─ main.py # compress source files
└─ references/
  └─ examples/ # Contains example code and compressed examples.
    ├── main.c # example of raw C 
    ├── main.cpp # example of raw C++
    ├── run.do # example of a Do or Tcl file
    ├── tb_top.v # example of Verilog file
    ├── top.vhd # example of a VHDL file
    └── test.py # example of Raw python
```

## Commands

The tool is a single Python script that processes files directly along with the SKILL.md which includes the usage and directives for agents.

```shell
# unix-like enviroments(bash, zsh, etc) use forwardslash 
python scripts/main.py <filename>
# Windows cmd or powershell use backslashes
python scripts\main.py <filename>
```

Compress single files:
```bash
python scripts/main.py <filename>
```

To Compress directory:
```bash
python scripts/main.py <directory>
```

Example:
```bash
python scripts/main.py references/examples/
```

## Supported Extensions

- VHDL: `.vhd`, `.vhdl`
- Verilog: `.v`, `.vh` 
- SystemVerilog: `.sv`, `.svh`
- C/C++: `.c`, `.h`, `.cpp`, `.hpp`, `.cc`, `.hh`, `.cxx`
- Python: `.py`
- Tcl/Do: `.tcl`, `.do`

## Output Format

Compressed files are saved as `<original_filename>-compressed.<extension>` in the same directory.

Example:
- `main.cpp` → `main-compressed.cpp`
- `tb_top.v` → `tb_top-compressed.v`

## Testing

To test the tool:
1. Run `python scripts/main.py references/examples/run.do` 
2. Check that `run-compressed.do` is created with reduced size
3. Verify comments are removed and whitespace minimized
