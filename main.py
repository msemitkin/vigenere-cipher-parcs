from Pyro4 import expose

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        shift, input_text = self.read_input()
        # chunk_size = int(ceil(len(input_text) / len(self.workers)))
        chunks = list(self.split_to_chunks(input_text, len(self.workers)))

        mapped = []
        for i in range(0, len(chunks)):
            mapped.append(self.workers[i].mymap(chunks[i], shift))

        print("Map finished: ", mapped)

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    def split_to_chunks(self, text, number_of_chunks):
        k, m = divmod(len(text), number_of_chunks)
        return (text[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(number_of_chunks))

    @staticmethod
    @expose
    def mymap(chunk, shift):
        result = ""
        for char in chunk:
            if char not in alphabet:
                result += char
            else:
                result += alphabet[(alphabet.index(char) + shift) % len(alphabet)]
        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        result = ""
        for x in mapped:
            result += x.value
        return result

    def read_input(self):
        with open(self.input_file_name, 'r') as file:
            lines = file.readlines()
            text = ""
            shift = int(lines[0])
            for line in lines[1:]:
                text += line
            return shift, text

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
