import sys

from ufal.udpipe import Model, Pipeline, ProcessingError # pylint: disable=no-name-in-module

# # In Python2, wrap sys.stdin and sys.stdout to work with unicode.
# if sys.version_info[0] < 3:
#     import codecs
#     import locale
#     encoding = locale.getpreferredencoding()
#     sys.stdin = codecs.getreader(encoding)(sys.stdin)
#     sys.stdout = codecs.getwriter(encoding)(sys.stdout)
#
# # if len(sys.argv) < 4:
# #     sys.stderr.write('Usage: %s input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file\n' % sys.argv[0])
# #     sys.exit(1)
sys.stderr.write('Loading model: ')


class UDParser(object):

    models = {"en": "UniversalPetrarch/preprocessing/udpipe-1.2.0/model/english-ud-2.0-170801.udpipe",
              "es": "UniversalPetrarch/preprocessing/udpipe-1.2.0/model/spanish-ancora-ud-2.0-170801.udpipe",
              "ar": ""}

    pipeline = None
    error = ProcessingError()
    model = None

    def __init__(self, lang="en"):
        model_file = "/Users/sxs149331/PycharmProjects/UniversalPetrarch-master/"+self.models[lang]
        print(model_file)
        self.model = Model.load(model_file)
        if not self.model:
            sys.stderr.write("Model Loading Failed")
            sys.exit(1)
        sys.stderr.write('done\n')
        self.pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")

    def parse(self, text):
        #print self.pipeline
        processed = self.pipeline.process(text.strip(), self.error)
        if self.error.occurred():
            raise ValueError(self.error.message)

        lines = processed.split("\n")
        result = []
        for line in lines:
            if line.startswith("#"):
                continue
            result.append(line)

        return ("\n").join(result)


parser = UDParser()

print((parser.parse("How are you?")))