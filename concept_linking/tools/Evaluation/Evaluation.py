import matplotlib.pyplot as plt
import numpy as np
import json


def read_scores_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        scores = [list(entry.values())[0][3] for entry in data]
    return scores


def evaluate_dataset(scores, title):
    # Counter for "?" occurrences
    question_mark_count = 0

    # Convert "?" to NaN and handle them in calculations
    scores_numeric = np.array([float(score) if score != "?" else np.nan for score in scores])

    # Plotting the distribution of points
    plt.hist(scores_numeric, bins=np.arange(-0.05, 1.15, 0.1), edgecolor='black')

    # Calculating and printing statistics
    average_score = np.nanmean(scores_numeric)
    max_score = np.nanmax(scores_numeric)
    min_score = np.nanmin(scores_numeric)
    std_dev = np.nanstd(scores_numeric)

    # Count occurrences of "?"
    question_mark_count = np.sum(np.isnan(scores_numeric))

    # Display statistics on the graph
    plt.text(1.01, 0.9, f"Avg: {average_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.85, f"Max: {max_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.8, f"Min: {min_score:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.75, f"SD: {std_dev:.2f}", transform=plt.gca().transAxes)
    plt.text(1.01, 0.7, f"?: {question_mark_count} occurrences", transform=plt.gca().transAxes)

    plt.title(title)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()