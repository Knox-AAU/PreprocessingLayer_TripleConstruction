import matplotlib.pyplot as plt
import numpy as np
import json


def read_scores_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        scores = [list(entry.values())[0][3] for entry in data]
    return scores


def evaluate_dataset(scores):
    # Plotting the distribution of points
    plt.hist(scores, bins=np.arange(-0.05, 1.15, 0.1), edgecolor='black')

    # Calculating and printing statistics
    average_score = np.mean(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)
    std_dev = np.std(scores)

    # Display statistics on the graph
    plt.text(1.01, 0.9, f"Avg: {average_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.85, f"Max: {max_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.8, f"Min: {min_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.75, f"SD: {std_dev:.2f}", transform=plt.gca().transAxes)

    plt.title('Distribution of Points: String Comparison Solution on Danish Dataset')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Show the plot
    plt.show()