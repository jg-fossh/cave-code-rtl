# Cave Code RTL

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/Version-0.0.2-yellow.svg)

**Stop wasting precious tokens and filling that context window.**

Every time you feed a new file you are consuming tokens and filling up your context window. Save tokens by getting rid of excessive empty spaces and comments. This skill is specific for RTL (logic) and firmware engineers looking to save on input tokens.

## The Problem

You want to feed large source files or full project directories to warm up the model, but empty spaces can be consider as tokens by AI models yet they may not add any value to the reasoning performed by your AI agent. This means you are spending more than what you need. On top of empty spaces your files will most likely contain large amount of comments(like fancy file headers) that provide little knowlegde to the model. It can be more efficient to point your model to documentation to complement the source code than relying on in line coments.

## The Solution

`cave-code-rtl` is a skill that calls a local python scripts to remove comments and empty space from your code, essentially  compressing your effective code and thus shrinking your inputs to the AI prompt.

## Features

- 🔍 **Supported file types:** - `.vhd`, `.vhdl`, `.v`, `.sv`, `.vh`, `.svh`, `.c`, `.h`, `.cpp`, `.hpp`, `.cc`, `.hh`, `.cxx`, `.py`, `.tcl` and .`do`
- 🔍 **Supports Single files and Directories:** - Scans an specified path or take in a single file.
- 🔍 **Outputs saved to a new files:** - Compressed files are save as `*-compressed.*` in the same directory of the original file. This allows for the compressed files to be inspected and reused.

## Installation

Simply copy into your skills directory(e.g. .github/skills/code-code-rtl) 

```bash
# Clone the repository
cd /path/to/your/project/.github/skills/
git clone https://github.com/goncalovelosa/cave-code-rtl.git
```

## Workflow

Follow this checklist when creating AGENTS.md:
- [ ] **1. Gather Context:** Identify the file or directory to be compressed. (e.g. read `file.vhd` or compress the sources in `/path_of_sources`).
- [ ] **2. Compress Sources:** Compress the files using the python script `scripts/main.py`
- [ ] **3. Read and Use Compressed Source:** Read the files with name `*-compressed.*` where `*` is the wildcard character.

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

## Compatibility

The generated AGENTS.md files work with:
- **Claude Code** - Anthropic's coding assistant
- **Codex** - OpenAI's code generation
- **Cursor** - AI-powered IDE
- **Aider** - Terminal-based AI coding
- **OpenCode** - Open-source alternative
- **Windsurf** - Codeium's IDE
- **Any AI coding agent** that reads project context

## Examples

Real example files in `references/examples/`

## Commands

- Compress: `python scripts/main.py <your_input>`
- Single File Example: `python scripts/main.py references/examples/run.do`
- Path Example: `python scripts/main.py references/examples/`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
