import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ── tiny GPT: 1-layer, 1-head, causal self-attn + FFN ──────────────────────
T, D, H_dim, C = 16, 32, 16, 8   # seq_len, d_model, d_head, vocab

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis, keepdims=True))
    return e / e.sum(axis, keepdims=True)

def cross_entropy(logits, y):
    p = softmax(logits)
    return -np.log(p[np.arange(len(y)), y] + 1e-10).mean(), p

def init_params():
    s = 0.02
    return {
        "Wq": np.random.randn(D, H_dim)*s, "Wk": np.random.randn(D, H_dim)*s,
        "Wv": np.random.randn(D, H_dim)*s, "Wo": np.random.randn(H_dim, D)*s,
        "W1": np.random.randn(D, D*2)*s,   "b1": np.zeros(D*2),
        "W2": np.random.randn(D*2, D)*s,   "b2": np.zeros(D),
        "Wout": np.random.randn(D, C)*s,   "bout": np.zeros(C),
    }

def forward(x, p):
    # x: (B, T, D)
    B = x.shape[0]
    mask = np.triu(np.full((T,T), -1e9), 1)

    Q = x @ p["Wq"]; K = x @ p["Wk"]; V = x @ p["Wv"]
    A = softmax(Q @ K.transpose(0,2,1) / H_dim**0.5 + mask)
    attn = A @ V @ p["Wo"]
    h = x + attn
    ff = np.maximum(0, h @ p["W1"] + p["b1"]) @ p["W2"] + p["b2"]
    h2 = h + ff
    logits = h2[:, -1, :] @ p["Wout"] + p["bout"]  # last token
    return logits, A, h, h2, ff, Q, K, V, attn

def backward(x, y, p, lr):
    B = x.shape[0]
    logits, A, h, h2, ff, Q, K, V, attn = forward(x, p)
    loss, probs = cross_entropy(logits, y)

    # output layer grad
    dlogits = probs.copy(); dlogits[np.arange(B), y] -= 1; dlogits /= B
    p["Wout"] -= lr * h2[:,-1,:].T @ dlogits
    p["bout"] -= lr * dlogits.sum(0)

    dh2_last = dlogits @ p["Wout"].T  # (B, D)
    dh2 = np.zeros_like(h2)
    dh2[:, -1, :] = dh2_last

    # FFN backward
    dff = dh2.copy()
    dW2 = np.einsum('bti,btj->ij', np.maximum(0, h @ p["W1"] + p["b1"]), dff)
    db2 = dff.sum((0,1))
    dh_ff = (dff @ p["W2"].T) * (h @ p["W1"] + p["b1"] > 0)
    dW1 = np.einsum('bti,btj->ij', h, dh_ff)
    db1 = dh_ff.sum((0,1))
    p["W1"] -= lr * dW1; p["b1"] -= lr * db1
    p["W2"] -= lr * dW2; p["b2"] -= lr * db2

    dh = dh2 + dh_ff @ p["W1"].T  # residual

    # attn backward (simplified)
    dattn_out = dh
    attn_out = A @ V                                          # (B,T,H_dim)
    dWo = np.einsum('bth,btd->hd', attn_out, dattn_out)
    p["Wo"] -= lr * dWo
    dattn_out_h = dattn_out @ p["Wo"].T                       # (B,T,H_dim)
    dV = np.einsum('bts,bsh->bth', A, dattn_out_h)
    p["Wv"] -= lr * np.einsum('btd,bth->dh', x, dV)
    p["Wq"] -= lr * np.einsum('btd,bth->dh', x, dattn_out_h) * 0.01
    p["Wk"] -= lr * np.einsum('btd,bth->dh', x, dattn_out_h) * 0.01

    return loss, probs

# ── data ────────────────────────────────────────────────────────────────────
B_size = 32
X_data = np.random.randn(B_size, T, D).astype(np.float32)
y_data = np.random.randint(0, C, B_size)

# ── entropy helper ───────────────────────────────────────────────────────────
def entropy_alpha(probs, n_classes):
    H_max = np.log(n_classes)
    H = -(probs * np.log(probs + 1e-10)).sum(-1).mean()
    B = min(float(H / H_max), 1 - 1e-6)
    return -np.log(1 - B)

# ── ablation ─────────────────────────────────────────────────────────────────
steps = 300
eta_target = 0.02

results = {}

for name in ["Fixed", "Cosine", "ADS"]:
    p = init_params()
    losses, lrs = [], []

    # calibrate eta0 for ADS
    if name == "ADS":
        _, probs0 = cross_entropy(forward(X_data, p)[0], y_data)
        a0 = entropy_alpha(probs0, C)
        eta0 = eta_target * (1 + a0)

    for t in range(steps):
        if name == "Fixed":
            lr = eta_target
        elif name == "Cosine":
            lr = eta_target * 0.5 * (1 + np.cos(np.pi * t / steps))
        else:  # ADS
            _, probs = cross_entropy(forward(X_data, p)[0], y_data)
            alpha = entropy_alpha(probs, C)
            lr = eta0 / (1 + alpha)

        loss, _ = backward(X_data, y_data, p, lr)
        losses.append(loss); lrs.append(lr)

    results[name] = (losses, lrs)
    print(f"{name:8s}  final_loss={losses[-1]:.4f}  final_lr={lrs[-1]:.5f}")

# ── plot ─────────────────────────────────────────────────────────────────────
colors = {"Fixed": "tab:orange", "Cosine": "tab:green", "ADS": "tab:blue"}
ls_map = {"Fixed": "-", "Cosine": "--", "ADS": "-"}
lw_map = {"Fixed": 1.8, "Cosine": 1.8, "ADS": 2.2}

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Tiny GPT Ablation: Entropy-Aware vs Fixed vs Cosine LR\n"
             r"($\eta_t = \eta_0/(1+\alpha(B_t))$, $\alpha=-\log(1-B_t)$, 1-layer causal attn)",
             fontsize=11)

for name, (losses, lrs) in results.items():
    label = f"{name} (η={lrs[0]:.3f}→{lrs[-1]:.3f})"
    axes[0].semilogy(losses, label=label, color=colors[name], ls=ls_map[name], lw=lw_map[name])
    axes[1].plot(lrs, label=name, color=colors[name], ls=ls_map[name], lw=lw_map[name])

axes[0].set_xlabel("Step"); axes[0].set_ylabel("Cross-Entropy Loss (log)")
axes[0].set_title("Loss Convergence"); axes[0].legend(); axes[0].grid(True, alpha=0.3)
axes[1].set_xlabel("Step"); axes[1].set_ylabel("Learning Rate")
axes[1].set_title("LR Schedule"); axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/Users/lizixi/Desktop/reasoning-kingdom/entropy_lr_gpt_ablation.png", dpi=150)
print("saved: entropy_lr_gpt_ablation.png")
