# openedu-qconv
Question format conversion and processing

The Question Converter is used to manage [questions](https://github.com/open-education-hub/methodology/blob/main/chapters/develop-organize/drills/reading/questions.md).
The main purpose is to convert questions from the `Storage Format` (i.e. Markdown for `Open-Education-Hub`, or any other format you might choose) to the `Deployment Format` (e.g. [`Moodle XML`](https://docs.moodle.org/402/en/Moodle_XML_format) if you use [`Moodle`](https://moodle.org/)).

The converter uses an intermediary `json` format, so if a new question format is needed, it can be easily added by providing the `newfmt_to_json()` and `json_to_newfmt()` functions.

# Requirements

All the requirements are found in the [`Makefile`](/Makefile) and can be installed using:

```console
make install
```

# Usage

You can run the script with the following command:

```console
python3 src/question_converter.py
```

To get the full usage instructions, you can run:

```console
python3 src/question_converter.py convert --help
```

```
Usage: quiz_manager.py convert [OPTIONS]

  Converts files to different formats.

Options:
  -i, --input-file TEXT           Input file path
  -d, --input-path TEXT           Input directory (read all `.input_format`
                                  files from the input path)
  -o, --output-file TEXT          Output file path
  -od, --output-path TEXT          Output directory (write questions in
                                  `Question_Title.output_format` files)
  -if, --input-format [JSON|XML|MD]
                                  The input format
  -of, --output-format [JSON|XML|MD]
                                  The output format
  -cf, --config TEXT              Config file path
  -c, --category TEXT             Category specifier for XML quizzes
  --help                          Show this message and exit.
```

In order to specify input files, you can use the `--input-file` or the `--input-path` options.

The `--input-file` option will expect the path to a file that contains one or multiple questions.
You can also add multiple input files by separating them with a comma.
In `Markdown`, multiple questions in the same file are separated by two empty lines.
If you have multiple questions, one saved in each file, you can use the `--input-path` option.
You may add multiple input directories by separating them with a comma, or use both input files and input directories by combining the `--input-path` and `--input-file` options.

This will expect a path to a directory which contains multiple `.md`, `.xml` or `.json` questions.

Similar to the input files, you can save the output in one file, using the `--output-file` option, or in a directory which will contain multiple files, each with one question, using the `--output-path` option.

For example, if we want to convert to `Moodle XML` all the questions from the [`Operating Systems` class, the `app-interact` chapter](https://github.com/open-education-hub/operating-systems/tree/main/content/chapters/app-interact/lab/quiz), we will run:

```console
python3 src/question_converter.py convert --input-path <path-to-operating-systems-repo>/content/chapters/app-interact/lab/quiz/ --input-format md --output-file questions.xml
```

This will create the `questions.xml` file, that will contain all the questions from the `io/lab/quiz/` directory, converted to the `Moodle XML` format:

```xml
  [...]
  <question type="multichoice">
    <name>
      <text>File Descriptor of `stderr`</text>
    </name>
    <questiontext format="markdown">
      <text>Which file descriptor is associated by default to `stderr`?</text>
    </questiontext>
    <tags/>
    <generalfeedback format="markdown">
      <text/>
    </generalfeedback>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answer fraction="0" format="markdown">
      <text>it varies from process to process</text>
    </answer>
    <answer fraction="0" format="markdown">
      <text>it varies from one Linux distribution to another</text>
    </answer>
    <answer fraction="0" format="markdown">
      <text>`stderr` has no associated file descriptor</text>
    </answer>
    <answer fraction="100.0" format="markdown">
      <text>2</text>
    </answer>
    <answer fraction="0" format="markdown">
      <text>0</text>
    </answer>
    <answer fraction="0" format="markdown">
      <text>1</text>
    </answer>
  </question>
  [...]
```

The `questions.xml` file can then be imported into Moodle and all the questions will be added to the question bank.

If, on the other hand, we export some questions from Moodle, and we want to convert them to Markdown questions, we can use:

```console
python3 src/question_converter.py convert --input-file questions.xml --output-path test_output/ --output-format md
```

This will populate the `test_output/` directory with Markdown questions:

```console
$ ls -l test_output/
total 96
-rw-rw-r-- 1 user user  572 sep  8 11:14 Cause_of_bind_Error.md
-rw-rw-r-- 1 user user  928 sep  8 11:14 Client-Server_Number_of_Copies.md
-rw-rw-r-- 1 user user  657 sep  8 11:14 Deluge_TCP_or_UDP.md
-rw-rw-r-- 1 user user  835 sep  8 11:14 Effect_of_execve_Syscall.md
-rw-rw-r-- 1 user user 1179 sep  8 11:14 Fewer_than_Two_Copies.md
-rw-rw-r-- 1 user user  279 sep  8 11:14 File_Descriptor_of_stderr.md
-rw-rw-r-- 1 user user  234 sep  8 11:14 File_handler_in_C.md
-rw-rw-r-- 1 user user 1240 sep  8 11:14 Firefox_TCP_or_UDP.md
-rw-rw-r-- 1 user user  504 sep  8 11:14 Flush_Libc_Buffer.md
-rw-rw-r-- 1 user user  616 sep  8 11:14 IO_Errors.md
-rw-rw-r-- 1 user user  865 sep  8 11:14 Limitation_of_Anonymous_Pipes.md
-rw-rw-r-- 1 user user  648 sep  8 11:14 mmap_vs_read_and_write_Benchmark.md
-rw-rw-r-- 1 user user  607 sep  8 11:14 open_equivalent_of_fopen_w.md
-rw-rw-r-- 1 user user  566 sep  8 11:14 O_TRUNC_Flag_Behaviour.md
-rw-rw-r-- 1 user user 1967 sep  8 11:14 Pipe_Ends.md
-rw-rw-r-- 1 user user  596 sep  8 11:14 printf_Under_Strace.md
-rw-rw-r-- 1 user user  755 sep  8 11:14 Prints_Working_after_Closing_stdio.md
-rw-rw-r-- 1 user user 2219 sep  8 11:14 Receiver_Socked_File_Descriptor.md
-rw-rw-r-- 1 user user  783 sep  8 11:14 senderpy_and_receiverpy_Client-Server_Parallel.md
-rw-rw-r-- 1 user user 2591 sep  8 11:14 Syscalls_Used_by_cp.md
-rw-rw-r-- 1 user user  214 sep  8 11:14 Syscall_Used_by_fopen.md
-rw-rw-r-- 1 user user  411 sep  8 11:14 write_filetxt_Permissions.md
```

You can see that the questions are saved in a file with the question name as the filename.

## Configuration File

If you would like to pass the parameters through a config file, you can do this by writing a YAML file and passing it via the `-cf` or `--config` option.

Here is a config example:
```yaml
- input_dir_path: questions/
- input_file_path:
	- questions1.md
	- questions2.md
- output_file_path: questions.xml
- output_format: xml
- input_format: md
```

Here is a list of all possible config options:
- `input_file_path`: Input file path
- `input_dir_path`: Input directory (read all `.input_format` files from the input path)
- `output_file`: Output file path
- `output_path`: Output directory (write questions in `Question_Title.output_format` files)
- `input_format`: The input format
- `output_format`: The output format
- `category`: Category specifier for XML quizzes

## Question Format

The `Moodle XML` format is described in detail on the [`Moodle docs website`](https://docs.moodle.org/402/en/Moodle_XML_format).
The Markdown format is described in the [methodology repository](https://github.com/open-education-hub/methodology/blob/main/chapters/develop-organize/drills/reading/questions.md).

If you want to use the Markdown questions with Moodle (i.e. convert them to `Moodle XML`), few more rules need to be followed, or else the Moodle import will fail:

- The `## Question Text` header **must** be present and **must not** be empty.
- The `## Question Answers` header **must** be present and **must** contain at least one correct answer.

All the other fields are optional.
