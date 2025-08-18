"""
@module
"""
import argparse
import json
import os
import sys
import time
import re
from loggers.loggings import logger
from analyser import Analyser
# from display_results import Results



def read_file(filename, dest_dir=None):
    """

    :param filename:
    :param dest_dir:
    :return:
    """
    cur_dir = os.getcwd()

    if not dest_dir:
        dest_dir = cur_dir

    filepath = dest_dir + filename

    with open(filepath, 'r',encoding='utf-8') as f:
        return f.read()


def read_json_file(filename, dest_dir=None):
    """

    :param filename:
    :param dest_dir:
    :return:
    """
    cur_dir = os.getcwd()

    if not dest_dir:
        dest_dir = cur_dir

    filepath = os.path.join(dest_dir, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_file(filename, filedata, dest_dir=None):
    """

    :param filename:
    :param filedata:
    :param dest_dir:
    :return:
    """
    cur_dir = os.getcwd()

    if not dest_dir:
        dest_dir = cur_dir

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    filepath = dest_dir + filename

    if isinstance(filedata, dict):
        with open(filepath, 'w',encoding='utf-8') as out:
            out.write(json.dumps(filedata, indent=4, sort_keys=True, ensure_ascii=False))
    elif isinstance(filedata, str):
        with open(filepath, 'w',encoding='utf-8') as out:
            out.write(filedata)
    else:
        with open(filepath, 'wb') as out:
            out.write(filedata)

    return True

def setup_directories():
    """

    :return:
    """
    os.getcwd()
    if not os.path.exists('output'):
        os.makedirs('output')
        logger.info("Created directory: output")
    else:
        logger.info("Directory output already exists")



if __name__ == '__main__':
    desc_text = "Oskar's parser for Kashubian"
    parser = argparse.ArgumentParser(description=desc_text)

    parser.add_argument("-t", "--text",
                        help="A text string representing the data to parse.",
                        dest='in_text',
                        required=False,
                        default='')
    parser.add_argument("-f", "--filename",
                        help="The path and name of the file containing the data to parse.",
                        dest='fname',
                        required=False,
                        default='')

    parser.add_argument("-ldb","--lexical_database", action="store_true",
                        help="If false, the lexical database will not be queried.")

    args = parser.parse_args()

    data = args.in_text if args.in_text else read_file(args.fname)
    use_ldb = args.lexical_database
    if not data:
        # print("No data to process, exiting")
        logger.error("No data provided to analyser, exiting...")
        sys.exit()

    setup_directories()
    text_name = re.split(r'[./]',args.fname)[-2]
    logger.info(f'Text to parse {text_name}')
    begin = time.time()
    a = Analyser(data, use_ldb, text_name)
    size = sys.getsizeof(a)
    logger.info("Object %s size in bytes: %d ",str(a),size)
    # logging.info("Object s% created, size in bytes: d%", a, size)
    r = a.do_analyse()
    end = time.time()
    a.final_stats()
    # print execution time
    duration = float(end - begin)
    logger.info("Text parsed in %f seconds", duration)
    # output = Results(r)
    # output.print_results()
