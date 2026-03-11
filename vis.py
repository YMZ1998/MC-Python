import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, cauchy
import matplotlib

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

# Create figure and subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Gaussian Distribution vs Cauchy Distribution - Comparison', fontsize=16, fontweight='bold')

# Parameter settings
x = np.linspace(-10, 10, 1000)

# 1. Probability Density Function Comparison (same center)
ax1 = axes[0, 0]

# Gaussian distribution (mean=0, std=1)
gaussian_pdf = norm.pdf(x, loc=0, scale=1)

# Cauchy distribution (location=0, scale=1)
cauchy_pdf = cauchy.pdf(x, loc=0, scale=1)

ax1.plot(x, gaussian_pdf, 'b-', linewidth=2.5, label='Gaussian (μ=0, σ=1)')
ax1.plot(x, cauchy_pdf, 'r-', linewidth=2.5, label='Cauchy (x₀=0, γ=1)')

# Fill tail regions
ax1.fill_between(x[x > 3], 0, gaussian_pdf[x > 3], alpha=0.3, color='blue')
ax1.fill_between(x[x > 3], 0, cauchy_pdf[x > 3], alpha=0.3, color='red')

ax1.set_xlabel('x')
ax1.set_ylabel('Probability Density f(x)')
ax1.set_title('PDF Comparison')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim([-6, 6])
ax1.set_ylim([0, 0.5])

# 2. Tail Behavior Comparison (log scale)
ax2 = axes[0, 1]

# Use log scale to examine tails
x_tail = np.linspace(1, 10, 500)
gaussian_tail = norm.pdf(x_tail, loc=0, scale=1)
cauchy_tail = cauchy.pdf(x_tail, loc=0, scale=1)

ax2.semilogy(x_tail, gaussian_tail, 'b-', linewidth=2.5, label='Gaussian')
ax2.semilogy(x_tail, cauchy_tail, 'r-', linewidth=2.5, label='Cauchy')

# Add reference lines for theoretical decay rates
# Gaussian: ~exp(-x²/2)
ref_gaussian = np.exp(-x_tail ** 2 / 2) / np.sqrt(2 * np.pi)
# Cauchy: ~1/(πx²)
ref_cauchy = 1 / (np.pi * x_tail ** 2)

ax2.semilogy(x_tail, ref_gaussian, 'b--', linewidth=1, alpha=0.7, label='Gaussian asymptote ~exp(-x²)')
ax2.semilogy(x_tail, ref_cauchy, 'r--', linewidth=1, alpha=0.7, label='Cauchy asymptote ~1/x²')

ax2.set_xlabel('x (x > 0)')
ax2.set_ylabel('Probability Density f(x) (log scale)')
ax2.set_title('Tail Decay Comparison (Log Scale)')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim([1, 10])

# 3. Cumulative Distribution Function Comparison
ax3 = axes[1, 0]

gaussian_cdf = norm.cdf(x, loc=0, scale=1)
cauchy_cdf = cauchy.cdf(x, loc=0, scale=1)

ax3.plot(x, gaussian_cdf, 'b-', linewidth=2.5, label='Gaussian')
ax3.plot(x, cauchy_cdf, 'r-', linewidth=2.5, label='Cauchy')

# Mark key quantiles
quantiles = [0.25, 0.5, 0.75, 0.95, 0.99]
colors = ['orange', 'green', 'purple', 'brown', 'magenta']

for q, color in zip(quantiles, colors):
    gaussian_q = norm.ppf(q, loc=0, scale=1)
    cauchy_q = cauchy.ppf(q, loc=0, scale=1)

    ax3.axvline(gaussian_q, color=color, linestyle=':', alpha=0.5, linewidth=0.8)
    ax3.axvline(cauchy_q, color=color, linestyle=':', alpha=0.5, linewidth=0.8)

    # Add labels at top
    ax3.text(gaussian_q, 1.02, f'{gaussian_q:.2f}', ha='center', fontsize=8, color=color, alpha=0.7)
    ax3.text(cauchy_q, -0.02, f'{cauchy_q:.2f}', ha='center', fontsize=8, color=color, alpha=0.7)

ax3.set_xlabel('x')
ax3.set_ylabel('Cumulative Probability F(x)')
ax3.set_title('CDF Comparison with Quantiles')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim([-8, 8])
ax3.set_ylim([-0.05, 1.05])

# 4. Random Samples Comparison
ax4 = axes[1, 1]

np.random.seed(42)  # Fixed seed for reproducibility
n_samples = 10000

# Generate random samples
gaussian_samples = np.random.normal(loc=0, scale=1, size=n_samples)
cauchy_samples = np.random.standard_cauchy(size=n_samples)

# Clip extreme values for visualization (Cauchy can have extreme values)
cauchy_samples_clipped = cauchy_samples[(cauchy_samples > -20) & (cauchy_samples < 20)]

# Plot histograms
bins = np.linspace(-6, 6, 100)
ax4.hist(gaussian_samples, bins=bins, density=True, alpha=0.6, color='blue', label='Gaussian samples')
ax4.hist(cauchy_samples_clipped, bins=bins, density=True, alpha=0.6, color='red', label='Cauchy samples (clipped)')

# Overlay theoretical curves
ax4.plot(x, gaussian_pdf, 'b-', linewidth=2, alpha=0.8)
ax4.plot(x, cauchy_pdf, 'r-', linewidth=2, alpha=0.8)

# Add boxplot showing outliers
ax4_box = ax4.inset_axes([0.6, 0.7, 0.35, 0.2])
box_data = [gaussian_samples[gaussian_samples < 10],
            cauchy_samples[cauchy_samples < 10]]
ax4_box.boxplot(box_data, labels=['Gaussian', 'Cauchy'], patch_artist=True,
                boxprops=dict(facecolor='lightgray', alpha=0.7))
ax4_box.set_title('Sample Boxplot (clipped)', fontsize=9)
ax4_box.grid(True, alpha=0.3)

ax4.set_xlabel('x')
ax4.set_ylabel('Density')
ax4.set_title(f'Random Samples Comparison (n={n_samples})')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim([-6, 6])

plt.tight_layout()

# Add statistics table
stats_text = """
Gaussian Distribution (μ=0, σ=1):
  • Mean = 0, Variance = 1
  • 95% of data in [-1.96, 1.96]
  • 99.7% of data in [-3, 3] (3σ rule)

Cauchy Distribution (x₀=0, γ=1):
  • Mean undefined, Infinite variance
  • 95% of data in [-12.7, 12.7]
  • 50% of data in [-1, 1]
  • Much heavier tails!
"""

fig.text(0.02, 0.02, stats_text, fontsize=10, verticalalignment='bottom',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))

plt.show()

# Additional: Create a bimodal mixture comparison (related to your thesis)
fig2, ax5 = plt.subplots(1, 1, figsize=(10, 6))

# Create example of mixture distributions (simulating the paper's scenario)
x_detailed = np.linspace(-8, 8, 1000)

# Two-Gaussian mixture
gaussian_mix = 0.6 * norm.pdf(x_detailed, loc=-1, scale=0.8) + \
               0.4 * norm.pdf(x_detailed, loc=2, scale=1.2)

# Two-Cauchy mixture
cauchy_mix = 0.6 * cauchy.pdf(x_detailed, loc=-1, scale=0.8) + \
             0.4 * cauchy.pdf(x_detailed, loc=2, scale=1.2)

# Add some "noise points" to simulate experimental data
np.random.seed(123)
noise_x = np.random.uniform(-7, 7, 20)
noise_y = np.random.exponential(0.05, 20)  # Small positive noise

ax5.plot(x_detailed, gaussian_mix, 'b-', linewidth=3, alpha=0.7, label='Two-Gaussian Mixture')
ax5.plot(x_detailed, cauchy_mix, 'r-', linewidth=3, alpha=0.7, label='Two-Cauchy Mixture')
ax5.scatter(noise_x, noise_y, color='gray', alpha=0.5, s=20, label='Simulated experimental noise')

# Fill difference regions
ax5.fill_between(x_detailed, gaussian_mix, cauchy_mix,
                 where=(cauchy_mix > gaussian_mix),
                 color='red', alpha=0.2, label='Cauchy > Gaussian region')
ax5.fill_between(x_detailed, gaussian_mix, cauchy_mix,
                 where=(gaussian_mix > cauchy_mix),
                 color='blue', alpha=0.2, label='Gaussian > Cauchy region')

ax5.set_xlabel('x')
ax5.set_ylabel('Probability Density')
ax5.set_title('Bimodal Mixture Models Comparison (Simulating Your Thesis Case)')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Add explanatory text
note_text = """Simulating your thesis scenario:
• Cauchy mixture is more robust to tail noise
• Gaussian mixture is more sensitive to outliers
• Cauchy's "heavy tails" better accommodate scattered data points
• This explains why Cauchy fitting was more practical"""
ax5.text(0.02, 0.98, note_text, transform=ax5.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor="lavender"))

plt.tight_layout()
plt.show()

print("=" * 60)
print("KEY OBSERVATIONS:")
print("1. Cauchy has higher peak and heavier tails")
print("2. Tail decay: Gaussian (exponential) vs Cauchy (polynomial)")
print("3. Cauchy produces extreme values more frequently")
print("4. Cauchy's 95%/99% quantiles are much larger than Gaussian's")
print("5. For noisy data, Cauchy mixture fitting can be more robust")
print("=" * 60)

# Add numerical comparison at specific points
print("\n" + "=" * 60)
print("NUMERICAL COMPARISON AT KEY POINTS:")
print("=" * 60)
print(f"{'x':>6} {'Gaussian PDF':>15} {'Cauchy PDF':>15} {'Ratio (Cauchy/Gauss)':>20}")
print("-" * 60)
for x_val in [0, 1, 2, 3, 4, 5]:
    g_val = norm.pdf(x_val, 0, 1)
    c_val = cauchy.pdf(x_val, 0, 1)
    ratio = c_val / g_val if g_val > 0 else float('inf')
    print(f"{x_val:>6.1f} {g_val:>15.6f} {c_val:>15.6f} {ratio:>20.2f}")

print("\nAt x=3:")
print(f"  • Gaussian probability: {norm.pdf(3, 0, 1):.6f}")
print(f"  • Cauchy probability: {cauchy.pdf(3, 0, 1):.6f}")
print(f"  • Cauchy is {cauchy.pdf(3, 0, 1) / norm.pdf(3, 0, 1):.1f} times more likely!")