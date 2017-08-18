import os
import argparse
import tatsu
from codecs import open
from pprint import pprint

from jinja2 import Environment, PackageLoader

def generate_feature(template, streams, items):
    generated_code = {
    'header':  template['header'].render(streams=streams, items=items),
    'content': template['content'].render(streams=streams, items=items),
    'footer': template['footer'].render(streams=streams, items=items)
    }
    return generated_code

def split_template_location(location):
    return location.split('.', maxsplit=1)

def get_template(package_name):
    env = Environment(
        loader=PackageLoader(package_name, '')
    )

    template = {
        'header': env.get_template('source.header.tpl'),
        'footer': env.get_template('source.footer.tpl'),
        'content': env.get_template('source.content.tpl')
    }
    return template

def generate_code(ast, generate):
    items = []
    for entry in ast:
        if 'item' in entry and entry['item'] is not None:
            items.append(entry['item'])

    streams = []
    for entry in ast:
        if 'stream' in entry and entry['stream'] is not None:
            streams.append(entry['stream'])

    generated_serialization = {'header':'', 'content':'', 'footer':''}
    generated_stream = {'header':'', 'content':'', 'footer':''}

    if 'serialization' in generate:
        generated_serialization = generate_feature(get_template(generate['serialization']), streams, items)
    if 'stream' in generate:
        generated_stream = generate_feature(get_template(generate['stream']), streams, items)

    print(generated_serialization['header'])
    print(generated_stream['header'])
    print(generated_serialization['content'])
    print(generated_stream['content'])
    print(generated_serialization['footer'])
    print(generated_stream['footer'])
    return

def parse_idl(input):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    grammar = open(dir_path + '/rxtender.ebnf').read()
    definitions = open(input).read()

    parser = tatsu.compile(grammar)
    ast = parser.parse(definitions)

    #pprint(ast, width=20, indent=4)
    return ast

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', help='rxtender definition file of a source stream')
    parser.add_argument('--serialization', help='module used for serialization')
    parser.add_argument('--stream', help='module used for stream routing')
    args = parser.parse_args()

    ast = parse_idl(args.input) if args.input else None
    generate = {}
    if args.serialization:
        generate['serialization'] = args.serialization
    if args.stream:
        generate['stream'] = args.stream

    if ast:
        generate_code(ast, generate)


if __name__ == '__main__':
    main()
