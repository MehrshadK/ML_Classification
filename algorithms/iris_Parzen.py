import csv
import math
import operator
import matplotlib.pyplot as plt
import random
import numpy as np


def load_dataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def euclidean_distance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def get_neighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclidean_distance(testInstance, trainingSet[x], length)
        if dist <= k:
            distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(len(distances)):
        neighbors.append(distances[x][0])
    return neighbors


def get_response(neighbors):
    classVotes = {}
    if len(neighbors) == 0:
        return random.randint(0, 2)
    else:
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def get_accuracy(testSet, predictions):
    correct = 0
    for x in range(len(predictions)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def main():

    # prepare data
    trainingSet = []
    testSet = []
    split = 0.3
    load_dataset('iris.data', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))

    ls = np.arange(0.01, 1, 0.05)
    parzen = []
    # generate predictions
    for r in ls:
        predictions = []
        accuracy = 0
        for x in range(len(testSet)):
            neighbors = get_neighbors(trainingSet, testSet[x], r)
            result = get_response(neighbors)
            predictions.append(result)
            # print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
            accuracy = get_accuracy(testSet, predictions)
        parzen.append(accuracy)
        print('Accuracy: ' + repr(accuracy) + '%')


    x_label = "value of r in parzen"
    y_label = "accuracy with split="
    y_label += str(split)

    plt.plot(ls, parzen)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

    
if __name__ == "__main__":
    main()
