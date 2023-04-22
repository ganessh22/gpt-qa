import argparse
import json
import os


def read_qa_text_file(file_path):
    """
    This function reads a text file containing question-answer pairs and returns them as a list of
    tuples.
    
    :param file_path: The file path of the text file containing the question-answer pairs
    :return: The function `read_qa_text_file` returns a list of tuples, where each tuple contains a
    question and its corresponding answer.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    qa_pairs = []
    i = 0
    while i < len(lines):
        question = lines[i].strip()
        i += 2
        answer = lines[i].strip()
        i += 1
        qa_pairs.append((question, answer))
    return qa_pairs


def find_txt_files(directory_path):
    """
    This function finds all the .txt files in a given directory and returns a list of their file paths.
    
    :param directory_path: The directory path is a string that represents the path to a directory on the
    file system. This function will search for all text files (files with the extension ".txt") within
    this directory and its subdirectories
    :return: The function `find_txt_files` returns a list of file paths for all the files with a `.txt`
    extension in the specified directory and its subdirectories.
    """
    txt_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process txt files directory and output jsonl file path.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing txt files')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output jsonl file path')
    return parser.parse_args()


def write_qa_jsonl(qa_list, output_file_path):
    flag = "a" if os.path.isfile(output_file_path) else "w"
    with open(output_file_path, flag) as f:
        for question, answer in qa_list:
            jsonl_line = json.dumps({'prompt': question, 'completion': answer})
            f.write(jsonl_line + '\n')


if __name__ == "__main__":
    args = parse_arguments()
    all_qa_pairs = []
    for txt_file in find_txt_files(args.directory):
        all_qa_pairs.extend(txt_file)
    write_qa_jsonl(all_qa_pairs, args.output)
