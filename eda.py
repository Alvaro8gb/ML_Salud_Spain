import seaborn as sns
import matplotlib.pyplot as plt

def plot_histogram(data, title='Distribution', xlabel='Value', ylabel='Count',
                   figsize=(10, 6), rotation=0, color='#4C72B0', bins=30):

    fig, ax = plt.subplots(figsize=figsize)

    if pd.api.types.is_numeric_dtype(data):
        clean = data.dropna()

        mean = clean.mean()
        q1   = clean.quantile(0.25)
        q3   = clean.quantile(0.75)

        ax.hist(clean, bins=bins, color=color, edgecolor='white',
                linewidth=0.5, alpha=0.85)

        line_cfg = [
            (mean, '#E74C3C', '-',  f'Media: {mean:.2f}'),
            (q1,   '#2ECC71', '--', f'Q1: {q1:.2f}'),
            (q3,   '#F39C12', '--', f'Q3: {q3:.2f}'),
        ]
        for val, col, ls, label in line_cfg:
            ax.axvline(val, color=col, linestyle=ls, linewidth=1.8, label=label)

        ax.legend(framealpha=0.9, fontsize=9)

    else:
        counts = data.value_counts().sort_index()
        total  = counts.sum()

        bars = ax.bar(range(len(counts)), counts.values, color=color,
                      edgecolor='white', linewidth=0.5, alpha=0.85)

        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(counts.index, rotation=rotation, ha='right' if rotation > 0 else 'center')

        for bar, count in zip(bars, counts.values):
            pct = count / total * 100
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + total * 0.005,
                f'{pct:.1f}%',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='#333333'
            )

    #ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='grey')
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    plt.show()
