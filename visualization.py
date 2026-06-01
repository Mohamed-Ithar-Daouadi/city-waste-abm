
import matplotlib.pyplot as plt

COLORS = ["blue", "red"]

COMPARISON_LABELS = [
"C1: Few vs Many Bins",
"C2: Random vs BFS Robot",
"C3: Low vs High Tourists",
"C4: Rare vs Frequent Transporters",
"C5: Open vs Dense City",
]

METRICS = [
    ("StreetWaste", "Total Waste on Streets"),
    ("OverflowingBins", "Overflowing Bins"),
    ("RobotEfficiency", "Robot Efficiency"),
    ("DistrictWaste", "Avg Waste per District"),
    ("TransporterWorkload", "Transporter Trips"),
]

def print_summary_table(all_results):
    pairs = [all_results[i:i+2] for i in range(0, len(all_results), 2)]
    
    for i in range(len(pairs)):
        pair = pairs[i]
        label = COMPARISON_LABELS[i]
        print(f"\n{label}")
        print("-" * 80)
        
        for result in pair:
            df = result["data"]
            waste = int(df["StreetWaste"].iloc[-1])
            overflow = int(df["OverflowingBins"].iloc[-1])
            efficiency = round(df["RobotEfficiency"].iloc[-1], 3)
            district = round(df["DistrictWaste"].iloc[-1], 1)
            trips = int(df["TransporterWorkload"].iloc[-1])
            
            print(f" {result['name']:<38} Waste: {waste:>4} | Overflow: {overflow:>2} | Eff: {efficiency:>5} | Dist: {district:>4} | Trips: {trips:>3}")
    print("\n")


def plot_results(all_results):
    pairs = [all_results[i:i+2] for i in range(0, len(all_results), 2)]

    fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 16))
    fig.suptitle("City Waste ABM Metrics", fontsize=16, fontweight="bold")

    for row_idx in range(len(pairs)):
        pair = pairs[row_idx]
        comp_label = COMPARISON_LABELS[row_idx]
        
        for col_idx in range(len(METRICS)):
            metric_key, metric_title = METRICS[col_idx]
            ax = axes[row_idx][col_idx]

            for s_idx in range(len(pair)):
                result = pair[s_idx]
                df = result["data"]
                if metric_key in df.columns:
                    ax.plot(df.index, df[metric_key], label=result["name"], color=COLORS[s_idx])
            
            if col_idx == 0:
                ax.set_ylabel(comp_label, fontweight="bold")

            ax.set_title(metric_title)
            ax.set_xlabel("Step")
            ax.legend(fontsize=7)
            ax.grid(True)

    plt.tight_layout()
    plt.savefig("results.png", dpi=150)
    print("Chart saved as results.png")
    plt.show()