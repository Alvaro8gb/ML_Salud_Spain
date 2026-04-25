if pd.api.types.is_numeric_dtype(data):
    clean = data.dropna()

    mean   = clean.mean()
    median = clean.median()  
    q1     = clean.quantile(0.25)
    q3     = clean.quantile(0.75)

    ax.hist(clean, bins=bins, color=color, edgecolor='white',
            linewidth=0.5, alpha=0.85)

    line_cfg = [
        (mean,   '#E74C3C', '-',  f'Media: {mean:.2f}'),
        (median, '#8E44AD', '-',  f'Mediana: {median:.2f}'),  # <-- nueva línea
        (q1,     '#2ECC71', '--', f'Q1: {q1:.2f}'),
        (q3,     '#F39C12', '--', f'Q3: {q3:.2f}'),
    ]

    for val, col, ls, label in line_cfg:
        ax.axvline(val, color=col, linestyle=ls, linewidth=1.8, label=label)

    ax.legend(framealpha=0.9, fontsize=9)
