# Error Level Analysis (ELA) Forensic Methodology

## 1. Principles of JPEG Compression Forensics
JPEG compression operates on $8 \times 8$ pixel discrete cosine transform (DCT) macro-blocks. When an image is originally saved, all macro-blocks are compressed at a consistent error level.

When an image is modified:
1. An attacker crops a signature, stamp, or alters text (e.g. changing an expiration date from `2024` to `2028`).
2. The modified block has not undergone the same number of quantization cycles as the background.
3. Upon re-compression at a known quality level (e.g., 90% or 95%), unaltered areas exhibit minimal error delta, while modified areas produce an elevated error level.

---

## 2. Mathematical Definition

Let $I(x, y)$ be the original RGB image, and $I_q(x, y)$ be the image after decompression from a standardized re-compression at quality factor $q=90$.

The per-channel error difference is:
$$\Delta_c(x, y) = |I_c(x, y) - I_{q, c}(x, y)| \quad \text{for } c \in \{R, G, B\}$$

The amplified forensic visualization value is:
$$E(x, y) = \min(255, \alpha \cdot \max_{c} \Delta_c(x, y))$$
where scale factor $\alpha \approx 10-20$ expands low-intensity compression deltas into human-observable and machine-measurable contrasts.

---

## 3. Thresholds & Heuristics
- **Homogeneous Backgrounds:** Authentic documents display uniform, low-intensity grain across text, background paper texture, and microprint.
- **Tampered / Spliced Injections:** Exhibit bright, high-contrast halos along boundary edges or distinctly darker/brighter DCT macro-blocks.
- **Mean Error Delta $\bar{E}$:** Normal documents typically range between $2.0 \le \bar{E} \le 8.5$. An extreme localized standard deviation $\sigma > 15.0$ in text/photo regions indicates composite splicing.
