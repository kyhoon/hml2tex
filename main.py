import pickle
import pandas as pd
import re
import argparse
from collections import OrderedDict

from bs4 import BeautifulSoup as bs
from bs4 import NavigableString


def main(args):
    print()
    with open(args.cmap, 'rb') as f:
        print("Opening Convert Map...")
        cmap = pickle.load(f)
    with open(args.input, encoding='cp949') as f:
        soup = bs(f.read(), 'xml')
        # Scripts
        print("Replacing Scripts...")
        for tag in soup.findAll('SCRIPT'):
            for k, v in cmap['Scripts'].items():
                tag.string = re.sub(k, v, tag.string)

        # TODO: Brackets

        # Cells
        print("Replacing Cells...")
        for tag in soup.findAll(['RECTANGLE', 'CELL']):
            if len(tag.text)!=0:
                tag.insert_before(NavigableString('#BEGIN#'))
                tag.insert_after(NavigableString('#END#'))

        # Remove Tags
        print("Removing Tags...")
        for tag in soup.findAll(['HEAD', 'SECDEF', 'SHAPECOMMENT']):
            tag.extract()
        for tag in soup.findAll('SCRIPT'):
            tag.insert_before(NavigableString(r' $'))
            tag.insert_after(NavigableString(r'$'))
        for tag in soup.findAll('P'):
            tag.insert(0, NavigableString('\n'))
        for tag in soup.findAll(True):
            tag.replaceWithChildren()

        # Paragraphs
        soup = str(soup)
        print("Replacing Paragraphs...")
        for k, v in cmap['Paragraphs'].items():
            soup = re.sub(k, v, soup)

    print("Saving File...")
    with open(args.output, 'w', encoding='cp949') as f:
        f.write(soup)
    print("Done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hml2tex')
    # File IO options
    parser.add_argument('--input', '-i', type=str, help="location of the input file")
    parser.add_argument('--output', '-o', type=str, help="location of the output file")
    parser.add_argument('--cmap', '-c', type=str, default="convertMap.pkl",
                        help="location of the convert map file")

    args = parser.parse_args()
    main(args)
