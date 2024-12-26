import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Data
inference_cost_x1 = [2,   4,   50, 54, 40, 42, 67, 84]
inference_cost_x2 = [2.5, 4.5, 80, 74, 68, 54, 77, 100]
performance_y1 =    [7,   13,  49, 45, 53, 59, 77, 70]
performance_y2 =    [8.5, 14.5, 53, 74, 80, 89, 89, 93]
labels = ["GPT-4o-mini", "GPT-4o", "Best of N", "ToT", "MACM", "Meta-reasoner", "o1-mini", "o1-preview"]

colors = sns.color_palette("husl", len(labels))  # Use Seaborn color palette

# Scatter points with error bounds represented as connected points
plt.figure(figsize=(10, 7))
for x, y, x_var, y_var, label, color in zip(inference_cost_x1, performance_y1, inference_cost_x2, performance_y2, labels, colors):
    # Calculate error points
    # Plot the original point and the error point
    if label == "Meta-reasoner":
        plt.scatter([x], [y], color=color, label=label, edgecolors='black', s=350, marker='*')
        plt.scatter([x_var], [y_var], color=color, edgecolors='black', s=350, marker='*')
    else:
        plt.scatter([x], [y], color=color, label=label, edgecolors='black', s=250)
        plt.scatter([x_var], [y_var], color=color, edgecolors='black', s=250)
    # Connect original point and error point with a line
    plt.plot([x, x_var], [y, y_var], linestyle='--', color=color, linewidth=2.5)

# Labels and title
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Inference Cost (%)", fontsize=14)
plt.ylabel("24-points Game Accuracy (%)", fontsize=14)
# plt.title("Math Performance vs Inference Cost", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Improve aesthetics with Seaborn style
sns.set_style("whitegrid")

# Show plot
plt.show()


plt.savefig('performance_vs_generations.png', dpi=300, bbox_inches='tight')
plt.show()
