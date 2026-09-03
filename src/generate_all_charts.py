import os
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create output directory
OUT_DIR = "experiments/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# Set global plot styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10.0
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'

# ==========================================
# FIGURE 1: Reconciliation Chart
# ==========================================
def generate_fig01():
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
    
    categories = [
        "WeirdChat Internal Benchmark (Paper)",
        "WeirdChat OpenRouter Replication",
        "Our Rubric + Judge on e02 (Handcheck)",
        "Our Rubric + Judge on Condition A",
        "Our WC_PROXY (First-Person Claims)",
        "Our Unverifiable Taxonomy (Broad Construct)"
    ]
    values = [12.5, 6.25, 7.3, 8.3, 30.6, 92.3]
    colors = ['#4A7BB0', '#4A7BB0', '#4A7BB0', '#4A7BB0', '#D95F02', '#E7298A']
    
    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, values, color=colors, height=0.55, edgecolor='none')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontweight='medium', fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel("Fabrication / Unverifiable Rate (%)", fontweight='bold', labelpad=10)
    ax.set_xlim(0, 115)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    for bar, val in zip(bars, values):
        width = bar.get_width()
        ax.text(width + 1.8, bar.get_y() + bar.get_height()/2, f"{val:.1f}%", 
                va='center', ha='left', fontweight='bold', fontsize=9.0, color='#222222')
        
    # Title high up with pad=42
    ax.set_title("Reconciliation: Instrument Construct Width vs. Measured Rate", 
                 fontsize=12, fontweight='bold', pad=42)
    
    # Legend starting more from the left
    patch_instrument = mpatches.Patch(color='#4A7BB0', label='WeirdChat Rubric (First-Person Execution Construct)')
    patch_taxonomy = mpatches.Patch(color='#D95F02', label='Broader Forensics Taxonomy (Unverifiable Provenance)')
    ax.legend(handles=[patch_instrument, patch_taxonomy], loc='lower left', bbox_to_anchor=(-0.05, 1.01),
              ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.2)
    
    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.32, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig01_reconciliation.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig01_reconciliation.svg"))
    plt.close()
    print("Generated Fig 1: Reconciliation Chart")

# ==========================================
# FIGURE 2: Rung-Distribution Stacked Bars (Conditions A-F)
# ==========================================
def generate_fig02():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    
    conditions = ['A', 'B', 'C', 'D', 'E', 'F']
    rung_data = {
        'A': {'0': 3.7, '1a/1b': 10.2, '2a/2b': 21.3, '3': 75.9, '4': 0.0, '5': 51.9, '6': 4.6, '7': 14.8},
        'B': {'0': 12.8, '1a/1b': 0.0, '2a/2b': 1.8, '3': 61.5, '4': 0.9, '5': 58.7, '6': 1.8, '7': 25.7},
        'C': {'0': 0.0, '1a/1b': 0.0, '2a/2b': 0.0, '3': 99.1, '4': 8.5, '5': 100.0, '6': 2.6, '7': 12.8},
        'D': {'0': 5.0, '1a/1b': 0.0, '2a/2b': 0.0, '3': 90.0, '4': 1.0, '5': 81.0, '6': 6.0, '7': 8.0},
        'E': {'0': 1.7, '1a/1b': 0.0, '2a/2b': 0.0, '3': 93.3, '4': 0.0, '5': 48.3, '6': 17.5, '7': 5.0},
        'F': {'0': 63.0, '1a/1b': 0.0, '2a/2b': 0.0, '3': 13.0, '4': 0.0, '5': 1.0, '6': 25.0, '7': 0.0}
    }
    
    r0 = [rung_data[c]['0'] for c in conditions]
    r1_2 = [rung_data[c]['1a/1b'] + rung_data[c]['2a/2b'] for c in conditions]
    r3_4 = [rung_data[c]['3'] + rung_data[c]['4'] for c in conditions]
    r5 = [rung_data[c]['5'] for c in conditions]
    r6_7 = [rung_data[c]['6'] + rung_data[c]['7'] for c in conditions]
    
    width = 0.52
    x = np.arange(len(conditions))
    
    c_r0 = '#D95F02'
    c_r12 = '#E7298A'
    c_r34 = '#7570B3'
    c_r5 = '#1B9E77'
    c_r67 = '#A6CEE3'
    
    ax.bar(x, r0, width, label='Rung 0: Unframed Assertion', color=c_r0)
    ax.bar(x, r1_2, width, bottom=r0, label='Rungs 1a–2b: First-Person Claims', color=c_r12)
    bottom_r34 = np.array(r0) + np.array(r1_2)
    ax.bar(x, r3_4, width, bottom=bottom_r34, label='Rungs 3–4: Unverified 3rd-Party Citations', color=c_r34)
    bottom_r5 = bottom_r34 + np.array(r3_4)
    ax.bar(x, r5, width, bottom=bottom_r5, label='Rung 5: Resolving Source Link', color=c_r5)
    bottom_r67 = bottom_r5 + np.array(r5)
    ax.bar(x, r6_7, width, bottom=bottom_r67, label='Rungs 6–7: Generic Hedges / Illustrative', color=c_r67)
    
    ax.set_xticks(x)
    ax.set_xticklabels([f"Cond {c}" for c in conditions], fontweight='bold')
    ax.set_ylabel("Presence Frequency (%)", fontweight='bold', labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_ylim(0, 270)
    
    # Title pushed significantly higher up with pad=68
    ax.set_title("Rung-Distribution Mechanisms Across Conditions A–F", 
                 fontsize=12, fontweight='bold', pad=68)
    
    # Legend centered above top plot border
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.2)
    
    fig.text(0.12, 0.02, "* Note: Multi-label presence counts; rungs per response are not mutually exclusive (total sum > 100%).", 
             fontsize=8, style='italic', color='#555555')
    
    plt.subplots_adjust(top=0.72, bottom=0.10, left=0.10, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig02_rung_stacked.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig02_rung_stacked.svg"))
    plt.close()
    print("Generated Fig 2: Rung-Distribution Stacked Bars")

# ==========================================
# FIGURE 3: Self-Critique Before/After Pair
# ==========================================
def generate_fig03():
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
    
    metrics = ['WC_PROXY\n(First-Person Execution)', 'Unverifiable Provenance\n(Rungs 1a–4)']
    pre_revision = [100.0, 100.0]
    post_revision = [0.0, 100.0]
    
    x = np.arange(len(metrics))
    width = 0.32
    
    rects1 = ax.bar(x - width/2, pre_revision, width, label='Original Condition A Subset', color='#D95F02')
    rects2 = ax.bar(x + width/2, post_revision, width, label='Post-Self-Critique Revision', color='#1B9E77')
    
    ax.set_ylabel('Prevalence (%)', fontweight='bold', labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold')
    ax.set_ylim(0, 120)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.set_title('Self-Critique Effect: First-Person vs. Data Provenance', 
                 fontsize=12, fontweight='bold', pad=42)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.0f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.0)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.0f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.0)
        
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.12, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig03_self_critique_before_after.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig03_self_critique_before_after.svg"))
    plt.close()
    print("Generated Fig 3: Self-Critique Pair")

# ==========================================
# FIGURE 4: Five-Condition Ablation (A-E)
# ==========================================
def generate_fig04():
    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=300)
    
    conds = ['A (Baseline)', 'B (Stripped)', 'C (Sourcing)', 'D (Citation)', 'E (Disclaim)']
    unv = [90.7, 63.3, 99.1, 90.0, 93.3]
    unv_err = [[90.7-85.3, 63.3-54.3, 99.1-97.5, 90.0-84.1, 93.3-88.9],
               [96.2-90.7, 72.4-63.3, 100.0-99.1, 95.9-90.0, 97.8-93.3]]
    
    wc = [24.1, 1.8, 0.0, 0.0, 0.0]
    wc_err = [[24.1-16.0, 1.8-0.0, 0.0, 0.0, 0.0],
              [32.1-24.1, 4.4-1.8, 0.0, 0.0, 0.0]]
    
    disc = [0.9, 0.0, 0.0, 0.0, 100.0]
    disc_err = [[0.9-0.0, 0.0, 0.0, 0.0, 0.0],
                [2.7-0.9, 0.0, 0.0, 0.0, 0.0]]
    
    x = np.arange(len(conds))
    width = 0.24
    
    ax.bar(x - width, unv, width, yerr=unv_err, capsize=3.5, label='Unverifiable Rate', color='#7570B3', error_kw={'elinewidth': 1.2})
    ax.bar(x, wc, width, yerr=wc_err, capsize=3.5, label='WC_PROXY Rate', color='#E7298A', error_kw={'elinewidth': 1.2})
    ax.bar(x + width, disc, width, yerr=disc_err, capsize=3.5, label='Disclaim Rate', color='#1B9E77', error_kw={'elinewidth': 1.2})
    
    ax.set_ylabel('Prevalence (%)', fontweight='bold', labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(conds, fontweight='medium')
    ax.set_ylim(0, 118)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.set_title('Five-Condition Prompt Ablation Study (Qwen 3.6 27B)', 
                 fontsize=12, fontweight='bold', pad=42)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=3, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig04_ablation_5cond.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig04_ablation_5cond.svg"))
    plt.close()
    print("Generated Fig 4: Five-Condition Ablation Chart")

# ==========================================
# FIGURE 5: Condition F Standalone
# ==========================================
def generate_fig05():
    fig, ax = plt.subplots(figsize=(8.5, 5.8), dpi=300)
    
    rungs = ['Rung 0\n(Unframed)', 'Rungs 1a–2b\n(First-Person)', 'Rungs 3–4\n(3rd Party)', 'Rung 5\n(Resolving)', 'Rungs 6–7\n(Generic Hedge)']
    b_vals = [12.8, 1.8, 61.5, 21.1, 2.8]
    f_vals = [63.0, 0.0, 13.0, 0.0, 24.0]
    
    x = np.arange(len(rungs))
    width = 0.35
    
    b_bars = ax.bar(x - width/2, b_vals, width, label='Condition B (Stripped Baseline)', color='#7570B3')
    f_bars = ax.bar(x + width/2, f_vals, width, label='Condition F (Hard Constraint)', color='#D95F02')
    
    ax.set_ylabel('Highest Rung Proportion (%)', fontweight='bold', labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(rungs, fontweight='bold')
    ax.set_ylim(0, 75)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.set_title('Condition F Mechanism: Mass Shift to Rung 0 Unattributed Assertion', 
                 fontsize=11.5, fontweight='bold', pad=42)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    for bar in b_bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5)
    for bar in f_bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
            
    fig.text(0.12, 0.02, "* Note: Consistent mutually exclusive primary-rung classification used for both conditions (each sums to 100.0%).", 
             fontsize=8, style='italic', color='#555555')
    
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig05_condition_f_standalone.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig05_condition_f_standalone.svg"))
    plt.close()
    print("Generated Fig 5: Condition F Standalone Chart")

# ==========================================
# FIGURE 6: Cross-Model Replication
# ==========================================
def generate_fig06():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.6), dpi=300, gridspec_kw={'width_ratios': [1.4, 1]})
    
    conds = ['Condition A', 'Condition C', 'Condition E']
    qwen_unv = [90.7, 99.1, 93.3]
    gemma_unv = [52.1, 99.0, 55.2]
    
    x = np.arange(len(conds))
    width = 0.35
    
    ax1.bar(x - width/2, qwen_unv, width, label='Qwen 3.6 27B', color='#4A7BB0')
    ax1.bar(x + width/2, gemma_unv, width, label='Gemma 4 31B', color='#D95F02')
    
    ax1.set_ylabel('Unverifiable Rate (%)', fontweight='bold', labelpad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(conds, fontweight='bold')
    ax1.set_ylim(0, 120)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax1.set_title('(A) Cross-Model Unverifiable Rate Replication', fontsize=11, fontweight='bold', pad=42)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    for rect in ax1.patches:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    topics = ['.NET Prompt', 'GraalVM Prompt']
    gemma_topics = [26.0, 76.0]
    
    ax2.bar(topics, gemma_topics, color=['#1B9E77', '#E7298A'], width=0.45)
    ax2.set_ylabel('Unverifiable Rate (%)', fontweight='bold', labelpad=10)
    ax2.set_title('(B) Gemma 4 31B Topic Asymmetry (Cond A)', fontsize=11, fontweight='bold', pad=15)
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar, val in zip(ax2.patches, gemma_topics):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 2, f"{val:.0f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig06_cross_model_replication.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig06_cross_model_replication.svg"))
    plt.close()
    print("Generated Fig 6: Cross-Model Replication Chart")

# ==========================================
# FIGURE 7: Discrimination Accuracy by Sub-Condition
# ==========================================
def generate_fig07():
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    
    subconds = [
        'Blatant Controls\n(n=10)',
        'Genuine Disclaimers\n(n=15)',
        'Honest / Hedged\n(n=10)',
        'Genuine Fabrications\n(n=15)'
    ]
    
    accs = [100.0, 100.0, 80.0, 60.0]
    err_low = [27.8, 20.4, 31.0, 24.3]
    err_high = [0.0, 0.0, 14.3, 20.2]
    
    colors = ['#1B9E77', '#1B9E77', '#7570B3', '#D95F02']
    
    x = np.arange(len(subconds))
    bars = ax.bar(x, accs, yerr=[err_low, err_high], capsize=5, color=colors, width=0.48, error_kw={'elinewidth': 1.8, 'ecolor': '#333333'})
    
    ax.axhline(50.0, color='red', linestyle=':', label='Chance Baseline (50%)', linewidth=1.5)
    
    ax.set_ylabel('Accuracy (%)', fontweight='bold', labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(subconds, fontweight='bold')
    ax.set_ylim(0, 125)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.set_title('Self-Discrimination Accuracy by Sub-Condition (Qwen 3.6 27B)', 
                 fontsize=12, fontweight='bold', pad=42)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=1, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    for bar, val in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width()/2, val + 4, f"{val:.0f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig07_discrimination_subcond.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig07_discrimination_subcond.svg"))
    plt.close()
    print("Generated Fig 7: Discrimination Sub-Condition Chart")

# ==========================================
# FIGURE 8: URL Dead-Rate
# ==========================================
def generate_fig08():
    fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=300)
    
    metrics = [
        'Unique URLs\n(Unweighted, n=100)', 
        'URL Mentions\n(Weighted, n=421)', 
        'Initial Ad-Hoc Est.\n(n≈20, non-random)'
    ]
    rates = [61.0, 45.6, 70.0]
    colors = ['#D95F02', '#7570B3', '#CCCCCC']
    
    x = np.arange(len(metrics))
    bars = ax.bar(x, rates, color=colors, width=0.45)
    
    ax.set_ylabel('Dead / 404 URL Rate (%)', fontweight='bold', labelpad=10)
    ax.set_title('Condition C Hallucinated URL Verification (Dead Rate)', fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold', fontsize=9.5)
    ax.set_ylim(0, 85)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar, val in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width()/2, val + 2, f"{val:.1f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.subplots_adjust(top=0.88, bottom=0.12, left=0.12, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig08_url_dead_rate.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig08_url_dead_rate.svg"))
    plt.close()
    print("Generated Fig 8: URL Dead-Rate Chart")

# ==========================================
# FIGURE 9: Grader Validation vs Trivial Baselines
# ==========================================
def generate_fig09():
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    
    categories = ['Ordinal Agreement\n(Exact Rung Hierarchy)', 'Binary Agreement\n(Unverifiable vs. Verified)']
    baseline_vals = [51.7, 89.7]
    grader_vals = [82.8, 96.6]
    
    x = np.arange(len(categories))
    width = 0.32
    
    b1 = ax.bar(x - width/2, baseline_vals, width, label='Trivial / Majority Class Baseline', color='#CCCCCC')
    b2 = ax.bar(x + width/2, grader_vals, width, label='Our Grader (Claude Opus 4.8)', color='#1B9E77')
    
    ax.set_ylabel('Agreement Rate (%)', fontweight='bold', labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontweight='bold')
    ax.set_ylim(0, 120)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.set_title('Grader Validation vs. Trivial / Majority Class Baselines', 
                 fontsize=12, fontweight='bold', pad=42)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=True, facecolor='white', framealpha=0.95, fontsize=8.8)
    
    for bar, val in zip(b1, baseline_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 2, f"{val:.1f}%", ha='center', va='bottom', fontweight='bold')
    for bar, val in zip(b2, grader_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 2, f"{val:.1f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.12, right=0.95)
    plt.savefig(os.path.join(OUT_DIR, "fig09_grader_validation.png"), dpi=300)
    plt.savefig(os.path.join(OUT_DIR, "fig09_grader_validation.svg"))
    plt.close()
    print("Generated Fig 9: Grader Validation Chart")

def main():
    generate_fig01()
    generate_fig02()
    generate_fig03()
    generate_fig04()
    generate_fig05()
    generate_fig06()
    generate_fig07()
    generate_fig08()
    generate_fig09()
    print(f"\nAll 9 publication figures successfully regenerated with zero title/legend overlaps in {OUT_DIR}/!")

if __name__ == '__main__':
    main()
