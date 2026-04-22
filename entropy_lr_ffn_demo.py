import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# --- tiny FFN on synthetic classification ---
def relu(x): return np.maximum(0, x)
def softmax(x): e = np.exp(x - x.max(-1, keepdims=True)); return e / e.sum(-1, keepdims=True)
def cross_entropy(p, y): return -np.log(p[np.arange(len(y)), y] + 1e-10).mean()

def ffn_forward(x, W1, b1, W2, b2):
    h = relu(x @ W1 + b1)
    return softmax(h @ W2 + b2), h

def ffn_grads(x, y, W1, b1, W2, b2):
    n = len(y)
    logits_raw = relu(x @ W1 + b1) @ W2 + b2
    p = softmax(logits_raw)
    h = relu(x @ W1 + b1)
    dp = p.copy(); dp[np.arange(n), y] -= 1; dp /= n
    dW2 = h.T @ dp; db2 = dp.sum(0)
    dh = dp @ W2.T * (h > 0)
    dW1 = x.T @ dh; db1 = dh.sum(0)
    return dW1, db1, dW2, db2, p

# data
N, D, H, C = 512, 16, 32, 8
X = np.random.randn(N, D).astype(np.float32)
y = np.random.randint(0, C, N)

def init():
    W1 = np.random.randn(D, H).astype(np.float32) * 0.1
    b1 = np.zeros(H, dtype=np.float32)
    W2 = np.random.randn(H, C).astype(np.float32) * 0.1
    b2 = np.zeros(C, dtype=np.float32)
    return W1, b1, W2, b2

def entropy_aware_alpha(p):
    H_max = np.log(C)
    H = -(p * np.log(p + 1e-10)).sum(-1).mean()
    B = min(H / H_max, 1 - 1e-6)
    return -np.log(1 - B)

steps = 200
eta_target = 0.05  # desired effective lr at step 0

# --- fixed lr (same effective rate for fair comparison) ---
W1,b1,W2,b2 = init()
loss_fixed, lr_fixed = [], []
for _ in range(steps):
    dW1,db1,dW2,db2,p = ffn_grads(X,y,W1,b1,W2,b2)
    W1-=eta_target*dW1; b1-=eta_target*db1; W2-=eta_target*dW2; b2-=eta_target*db2
    loss_fixed.append(cross_entropy(p,y))
    lr_fixed.append(eta_target)

# --- entropy-aware lr: calibrate eta0 from initial entropy ---
W1,b1,W2,b2 = init()
_,_,_,_,p0 = ffn_grads(X,y,W1,b1,W2,b2)
alpha0 = entropy_aware_alpha(p0)
eta0 = eta_target * (1 + alpha0)  # so first effective step == eta_target
loss_ent, lr_ent = [], []
for _ in range(steps):
    dW1,db1,dW2,db2,p = ffn_grads(X,y,W1,b1,W2,b2)
    alpha = entropy_aware_alpha(p)
    eta_t = eta0 / (1 + alpha)
    W1-=eta_t*dW1; b1-=eta_t*db1; W2-=eta_t*dW2; b2-=eta_t*db2
    loss_ent.append(cross_entropy(p,y))
    lr_ent.append(eta_t)

# --- cosine annealing (same eta_target base) ---
W1,b1,W2,b2 = init()
loss_cos, lr_cos = [], []
for t in range(steps):
    dW1,db1,dW2,db2,p = ffn_grads(X,y,W1,b1,W2,b2)
    eta_t = eta_target * 0.5 * (1 + np.cos(np.pi * t / steps))
    W1-=eta_t*dW1; b1-=eta_t*db1; W2-=eta_t*dW2; b2-=eta_t*db2
    loss_cos.append(cross_entropy(p,y))
    lr_cos.append(eta_t)

# --- plot ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("FFN Convergence: Entropy-Aware vs Fixed vs Cosine LR\n"
             r"($\eta_t = \eta_0\,/\,(1+\alpha(B_t))$,  $\alpha=-\log(1-B_t)$)",
             fontsize=12)

ax = axes[0]
ax.semilogy(loss_fixed, label=f"Fixed $\\eta$={eta0}", color="tab:orange", lw=1.8)
ax.semilogy(loss_cos,   label="Cosine Annealing",      color="tab:green",  lw=1.8, ls="--")
ax.semilogy(loss_ent,   label="Entropy-Aware (ADS)",   color="tab:blue",   lw=2.2)
ax.set_xlabel("Step"); ax.set_ylabel("Cross-Entropy Loss (log scale)")
ax.set_title("Loss Convergence"); ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1]
ax.plot(lr_fixed, label=f"Fixed $\\eta$={eta0}", color="tab:orange", lw=1.8)
ax.plot(lr_cos,   label="Cosine Annealing",      color="tab:green",  lw=1.8, ls="--")
ax.plot(lr_ent,   label="Entropy-Aware (ADS)",   color="tab:blue",   lw=2.2)
ax.set_xlabel("Step"); ax.set_ylabel("Learning Rate")
ax.set_title("LR Schedule"); ax.legend(); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/Users/lizixi/Desktop/reasoning-kingdom/entropy_lr_ffn_demo.png", dpi=150)
print("saved: entropy_lr_ffn_demo.png")
