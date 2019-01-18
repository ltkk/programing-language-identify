from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from fastText import train_supervised


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))


def test(model, test_path):
    data = {}
    with open(test_path, encoding='utf8') as fp:
        for line in fp.readlines():
            line = line.strip()
            words = line.split()
            label = words[0]
            pred = model.predict(' '.join(words[1:]))[0][0]
            if label not in data:
                data[label] = {}
                data[label]['correct'] = 0
                data[label]['total'] = 0
            data[label]['total'] += 1
            if label == pred:
                data[label]['correct'] += 1
    summaries = {}
    for key in data:
        summaries[key] = round(data[key]['correct'] / data[key]['total'], 2)
    return summaries, data


if __name__ == "__main__":
    train_data = "data/train.txt"
    valid_data = "data/test.txt"

    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(
        # input=train_data, epoch=25, lr=0.1, wordNgrams=2
        input=train_data, epoch=5, lr=0.1, wordNgrams=1, verbose=2, loss="softmax", label='__lb__'
    )
    # print_results(*model.test(valid_data))
    summaries, details = test(model, valid_data)
    print(summaries)
    model.save_model("model/ft.li.1701.bin")
