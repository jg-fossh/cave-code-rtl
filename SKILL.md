---
name: cave-code-rtl
description: |
  RTL Code token compressor that makes prompts smaller and consume less tokens. Use when: (1) Analyzing code files, (2) Updating existing code files, (3) Consolidating multiple code files, (4) When learning a new codebase.
author: jg-fossh@gmail.com
version: 0.0.1
license: MIT
platforms: [linux, macos, windows]
metadata:
    tags: [cave, code, rtl, compress, token, cross-platform]
    related_skills: [claude-code, hermes-agent, copilot]
prerequisites:
    commands: [bash, python]
allowed-tools:
  - bash
  - read
  - write
---

# Cave Code

Compress code by removing comments and spaces. RTL Code token compressor that makes prompts smaller and consume less tokens. Use when: (1) Analyzing code files, (2) Updating existing code files, (3) Consolidating multiple code files, (4) When learning a codebase.


## Workflow Checklist

Copy and check off as you progress:

- [ ] **1. Gather Context:** Identify the file or directory to be compressed. (e.g. read `file.vhd` or compress the sources in `/path_of_sources`). Files should named by file name followed by a dot and an extension, following form for filename <base>.<extension>
- [ ] **2. Compress Sources:** Compress the files using the python script `scripts/main.py`. The script indicates when it is done with a "Done!" printout. If the files are not supported the script with printout an error. In such case indicate that compression is not supported and continue to use original files.
- [ ] **3. Read and Use Compressed Source:** `read` the files with name `compressed` appended to their name such that <base>-compressed.<extension> is the new compressed file. (e.g. original file `main.c`, compressed file would be named `main-compressed.c`, or an original file named `top.vhd`, compressed file would be `top-compressed.vhd`).

## Quick Start

For single files:

```bash
python scripts/main.py /<path>/<base>.<extension>
```

For a directory:

```bash
python scripts/main.py /<sources>/<path>
```

After the python script finishes `read` the compressed files. These contain `compressed` in their name.

## Scripts

### main.py

`main.py` Removes comments and empty spaces. Supports the following `extensions`:
- VHDL: `.vhd`, `.vhdl`
- Verilog: `.v`, `.vh`
- SystemVerilog: `.v`, `.sv`, `.vh`, `.svh`
- C: `.c`, `.h`, `.cpp`, `.hpp`
- C++, systmeC: `.cc`, `.cpp`, `.cxx`, `.hh`, `.hpp`
- Tcl & Do: `.tcl`, `.do`
- Python: `.py`

**Output:** 
1. Saves output to `<base>-compressed.<extension>`
2. Printout of "Done!" when successful or Error message when files are not supported.

## Best Practices

Check you can use @tools: Python and (Bash or PowerShell).

## Examples

Real example files in `references/examples/`

- `references/examples/tb_top.v` - Original file name `tb_top` with extension `v` 
- `references/examples/compress-tb_top.v` - compress output file to `tb_top.v`
- `references/examples/top.vhd` - Original file name `top` with extension `vhd` 
- `references/examples/compress-top.vhd` - compress output file to `top.vhd`

- Compress Single File Example: `python scripts/main.py references/examples/run.do`
- Compress Files in Path Example: `python scripts/main.py references/examples/`

## Compatibility

Works with all AI coding agents:
- Claude Code
- Codex
- Cursor
- OpenCode
- Windsurf
- Copilot
- Hermes
- Any agent that reads project context


