[![progress-banner](https://backend.codecrafters.io/progress/shell/f43761b4-d65c-43e7-9973-32a5538cc488)](https://app.codecrafters.io/users/dtetedonkor?r=2qF)

# Build Your Own Shell

A Python implementation of a POSIX-style shell built as part of the [CodeCrafters "Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

The goal of this project is to progressively build a functional shell from scratch while learning about:

* Shell command parsing
* REPLs and interactive input
* Built-in commands
* External program execution
* Input/output redirection
* Quoting and escaping
* Tab completion
* File and directory path completion
* Process execution

## Current Features

The shell currently supports:

* Built-in commands:

  * `cd`
  * `pwd`
  * `echo`
  * `type`
  * `exit`
  * `complete`
* Execution of external programs
* Command searching through the system `PATH`
* Single and double quote handling
* Escape characters
* Output redirection
* Append redirection
* Standard error redirection
* Tab completion for commands
* Tab completion for files
* Tab completion for directories
* Nested path completion
* File completion with hyphenated filenames
* Directory completion with trailing `/`

### Tab Completion

The shell distinguishes between files and directories when completing paths:

```text
$ ls p<TAB>
$ ls project/
```

Directories receive a trailing `/` so completion can continue into nested directories:

```text
$ ls project/<TAB>
$ ls project/src/
```

Files receive a trailing space:

```text
$ ls project/src/m<TAB>
$ ls project/src/main.py 
```

The shell also configures Python `readline` completion delimiters so characters such as `-` are treated as part of a filename rather than separating completion words.

## Project Structure

The main shell implementation is located in:

```text
app/main.py
```

The shell is being developed incrementally as each CodeCrafters stage is completed.

## Running the Shell

Run the shell locally with:

```sh
./your_program.sh
```

You can also run the Python entry point directly:

```sh
python app/main.py
```

## Running CodeCrafters Tests

Submit the current implementation to CodeCrafters with:

```sh
codecrafters submit
```

The CodeCrafters platform runs the appropriate test suite against the shell and reports which stages have passed.

## CodeCrafters Challenge

This project is based on the [CodeCrafters Build Your Own Shell Challenge](https://app.codecrafters.io/courses/shell/overview).

If you're viewing this repository on GitHub, you can visit [CodeCrafters](https://codecrafters.io/) to learn more about the challenge and try it yourself.
