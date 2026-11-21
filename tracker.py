import csv
import matplotlib.pyplot as plt
from pathlib import Path


def describe_guidance(actual, guidance_text):
    if not guidance_text:
        return "guidance unavailable"

    difference = actual - float(guidance_text)

    if difference > 0:
        return f"beat the top of guidance by {difference:g} pp"
    if difference < 0:
        return f"came in {abs(difference):g} pp below the top of guidance"
    return "matched the top of guidance"


csv_path = Path(__file__).with_name("earnings.csv")

quarters = []
ross_values = []
tjx_values = []

with csv_path.open(newline="", encoding="utf-8") as earnings_file:
    for row in csv.DictReader(earnings_file):
        ross_comp = float(row["ross_comp"])
        tjx_comp = float(row["tjx_comp"])
        quarters.append(row["quarter"])
        ross_values.append(ross_comp)
        tjx_values.append(tjx_comp)
        gap = ross_comp - tjx_comp

        ross_result = describe_guidance(ross_comp, row["ross_guidance_high"])
        tjx_result = describe_guidance(tjx_comp, row["tjx_guidance_high"])

        print(row["quarter"])
        print(f"  Ross: {ross_comp:g}% comp growth ({ross_result})")
        print(f"  TJX:  {tjx_comp:g}% comp growth ({tjx_result})")

        if gap > 0:
            print(f"  Ross led by {gap:g} pp.")
        elif gap < 0:
            print(f"  TJX led by {abs(gap):g} pp.")
        else:
            print("  Ross and TJX tied.")

        print()

plt.plot(quarters, ross_values, marker="o", label="Ross")
plt.plot(quarters, tjx_values, marker="o", label="TJX")
plt.title("Ross vs. TJX Comparable Sales Growth")
plt.ylabel("Comp growth (%)")
plt.legend()
plt.tight_layout()
plt.savefig(csv_path.with_name("comp_growth.png"), dpi=150)

gaps = [ross - tjx for ross, tjx in zip(ross_values, tjx_values)]

plt.figure()
plt.bar(quarters, gaps)
plt.axhline(0, color="black", linewidth=1)
plt.title("Ross vs. TJX Comp Growth Gap")
plt.ylabel("Ross minus TJX (percentage points)")
plt.tight_layout()
plt.savefig(csv_path.with_name("comp_gap.png"), dpi=150)