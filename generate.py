import argparse
from textgenerator import TextGenerator

parser = argparse.ArgumentParser()
parser.add_argument("--model")
parser.add_argument("--prefix", nargs='+')
parser.add_argument("--length", type=int)
args = parser.parse_args()

# print(args.model, args.prefix, args.length)

model = TextGenerator(args.model)

print(model.generate(args.prefix, args.length))

'py generate.py --model=model.pickle --prefix обломов --length=200'
