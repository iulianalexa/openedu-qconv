"""
    Quiz Manager is a script that helps with the convertion and generation of quizzes.
"""

import re
import sys
import json
import glob
import click
import yaml
import os
from parsers import mxml
from parsers import md


@click.group()
def cli():
    """
    Entrypoint of the application
    """

@cli.command()
@click.option(
    "-i", "--input-file", "input_file_path", required=False, help="Input file path"
)
@click.option(
    "-d", "--input-path", "input_dir_path", required=False, help="Input directory (read all `.input_format` files from the input path)"
)
@click.option(
    "-o", "--output-file", "output_file_path", required=False, help="Output file path"
)
@click.option(
    "-od", "--output-path", "output_dir_path", required=False, help="Output directory (write questions in `Question_Title.output_format` files)"
)
@click.option(
    "-if",
    "--input-format",
    type=click.Choice(["JSON", "XML", "MD"], case_sensitive=False),
    help="The input format",
)
@click.option(
    "-of",
    "--output-format",
    type=click.Choice(["JSON", "XML", "MD"], case_sensitive=False),
    help="The output format",
)
@click.option(
	"-cf",
	"--config",
	"config_file_path",
	required=False,
	help="Config file path"
)
@click.option(
    "-c",
    "--category",
    required=False,
    help="Category specifier for XML quizzes",
)
def convert(**kwargs):
    """
    Converts files to different formats.
    """
    config = {key: parse_list(value) for key, value in kwargs.items() if value is not None}
    
    if "config_file_path" in config:
        try:
            config_fd = open(config["config_file_path"], "r")
        except FileNotFoundError:
            raise click.UsageError(
                "Config file does not exist."
            )
    		
        with config_fd:
            config_in_file = yaml.safe_load(config_fd)
        
        if type(config_in_file) != list:
            raise click.UsageError(
                "Invalid config file format."
            )
		
        for entry in config_in_file:
            for config_key in entry:
                if config_key not in config:
                    config[config_key] = entry[config_key]
                elif config_key == "input_file_path" or config_key == "input_dir_path":
                    if type(config[config_key]) == str:
                        config[config_key] = [config[config_key]]
                        config[config_key].extend(entry[config_key])
                    
    input_file_path = config["input_file_path"] if "input_file_path" in config else None
    output_file_path = config["output_file_path"] if "output_file_path" in config else None
    input_dir_path = config["input_dir_path"] if "input_dir_path" in config else None
    output_dir_path = config["output_dir_path"] if "output_dir_path" in config else None
		
    if input_file_path is None and input_dir_path is None:
        raise click.UsageError(
            "One of --input-path or --input-file must be set."
        )

    if output_dir_path is None and output_file_path is None:
        raise click.UsageError(
            "One of --output-path or --output-file must be set."
        )

    if "input_format" not in config:
        if input_file_path is None:
            raise click.UsageError(
                "--input-format must be specified if using --input-path"
            )

        if type(input_file_path) == str and input_file_path.split(".")[-1].lower() in ["json", "xml", "md"]:
            config["input_format"] = input_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Input format can't be extracted from input"
                " file extention. Use --input-format to specify the input format."
            )

    if "output_format" not in config:
        if output_file_path is None:
            raise click.UsageError(
                "--output-format must be specified if using --output-path"
            )

        if output_file_path.split(".")[-1].lower() in ["json", "xml", "md"]:
            config["output_format"] = output_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Output format can't be extracted from output"
                " file extention. Use --output-format to specify the output format."
            )

    print(f"Converting from {config['input_format']} to {config['output_format']}")
    print(f"Paths:\n\tinput: {input_file_path}\n\toutput: {output_file_path}")

    input_content = ""
    read_files = []

    if input_file_path is not None:
        if type(input_file_path) == str:
            read_files.append(input_file_path)
        elif type(input_file_path) == list:
            read_files.extend(input_file_path)

    if input_dir_path is not None:
        if type(input_dir_path) == str:
            read_files.extend(glob.glob(input_dir_path + f"/*.md"))
        elif type(input_dir_path) == list:
            for path in input_dir_path:
                read_files.extend(glob.glob(path + f"/*.md"))
           
    read_files = [os.path.abspath(x) for x in read_files] 
    read_files = list(set(read_files))
            
    for path in read_files:
        with open(path, "r", encoding="UTF-8") as input_file:
            input_content += input_file.read()
        input_content += "\n\n\n"
        
    input_content = input_content.rstrip("\n")

    conversion = ""
    if config["input_format"].upper() == "JSON":
        if config["output_format"].upper() == "XML":
            conversion = mxml.quiz_json_to_mxml(json.loads(input_content), config["category"])
        elif config["output_format"].upper() == "MD":
            conversion = md.quiz_json_to_md(json.loads(input_content))
    elif config["input_format"].upper() == "XML":
        if config["output_format"].upper() == "JSON":
            conversion = mxml.quiz_mxml_to_json(input_content)
        elif config["output_format"].upper() == "MD":
            conversion = md.quiz_json_to_md(json.loads(mxml.quiz_mxml_to_json(input_content)))
    elif config["input_format"].upper() == "MD":
        if config["output_format"].upper() == "JSON":
            conversion = md.quiz_md_to_json(input_content)
        if config["output_format"].upper() == "XML":
            conversion = mxml.quiz_json_to_mxml(json.loads(md.quiz_md_to_json(input_content)))

    if output_dir_path is None:
        with open(output_file_path, "w", encoding="UTF-8") as output_file:
            output_file.write(''.join(conversion))
    else:
        if config["output_format"].upper() == "MD":
            for q in conversion:
                q_name = re.sub('[`().,;:?"/]', '', q.partition('\n')[0][2:])
                q_name = re.sub(' ', '_', q_name)
                with open(output_dir_path + "/" + q_name + ".md", "w", encoding="UTF-8") as output_file:
                    output_file.write(q.strip("\n"))

def parse_list(input_str):
    output_list = [x.strip() for x in input_str.split(',')]
    if len(output_list) <= 1:
        return input_str
    
    return output_list    

if __name__ == "__main__":
    cli()
