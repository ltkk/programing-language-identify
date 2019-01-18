from sklearn.model_selection import train_test_split
import os


def save_fasttext_format(X_data, y_data, output_file, prefix='__lb__'):
    with open(output_file, 'w', encoding='utf8') as fp:
        for x, y in zip(X_data, y_data):
            fp.write(prefix + y + ' ' + x + '\n')


Xs = []
ys = []

data_dir = "../data_crawler/data"

for file in os.listdir(data_dir):
    if file.endswith('.txt'):
        label = file[:-4]
        for line in open(os.path.join(data_dir, file), encoding='utf8').readlines():
            Xs.append(line.strip())
            ys.append(label)

X_train, X_test, y_train, y_test = train_test_split(Xs, ys, test_size=0.2, random_state=42)

save_fasttext_format(X_train, y_train, 'data/train.txt')
save_fasttext_format(X_test, y_test, 'data/test.txt')
