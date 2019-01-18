
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
    return data
