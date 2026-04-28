---
aliases: []
created: 2026-04-28 22:37:03
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
# Nguyên nhân

## Bạn KHÔNG thực sự “generate SQL”

Bạn đang:

generate adversarial sequence

👉 giống:

- jailbreak prompt
- adversarial NLP

---

## GAN hữu ích khi:

- Bạn có discriminator = “WAF / detector”
- Generator học cách bypass

👉 Đây là:

Generator → attack  
Discriminator → defense

🔥 Đây là use-case GAN mạnh nhất trong NLP

# Định hướng
## Continuous relaxation (Gumbel-Softmax)

Biến discrete → “giả continuous”

- Softmax + noise → gần giống sampling
- Cho phép backprop xuyên qua token

👉 Key idea:

argmax (discrete)  →  softmax (continuous approximation)

📌 Dùng trong:

- RelGAN
- GSGAN
- Meta-CoTGAN

---

## (2) 🎯 Reinforcement Learning (policy gradient)

Xem generator như **policy π(a|s)**

- Token = action
- Sequence = trajectory
- Reward = discriminator score

👉 Công thức lõi:

∇θJ(θ)=Eπθ[R⋅∇θlog⁡πθ(a∣s)]\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}[R \cdot \nabla_\theta \log \pi_\theta(a|s)]∇θ​J(θ)=Eπθ​​[R⋅∇θ​logπθ​(a∣s)]

👉 Đây chính là:

- **REINFORCE**
- Backbone của **SeqGAN**

📌 Ưu:

- Không cần differentiable output

📌 Nhược:

- Variance cao
- Train chậm / unstable

---

## (3) 🧩 Latent / hybrid approach

Không sinh text trực tiếp, mà:

z → semantic space → decode → text

👉 Ví dụ:

- TextGAN → feature matching
- TextGen-GAN (2025) → GAN + RNN decoder
- Transformer-GAN → pretrain + adversarial fine-tune

📌 Đây là hướng hiện đại nhất

# evalution

KHÔNG chỉ dùng BLEU

Nên dùng:

- Perplexity → fluency
- Self-BLEU → diversity
- Attack success rate → quan trọng nhất (SQLi)