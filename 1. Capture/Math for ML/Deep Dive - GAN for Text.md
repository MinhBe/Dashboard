---
aliases: [TextGAN, SeqGAN, Gumbel-Softmax]
created: 2026-04-29 00:00:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, gan, text-generation, sql-injection]
category: [research]
---
# Deep Dive: GAN cho Text - Vượt qua rào cản Rời rạc

## 1. Bản chất cốt lõi (Core Intuition)
Hãy tưởng tượng GAN như một họa sĩ (Generator) và một giám khảo (Discriminator).
- **Với ảnh (Continuous):** Họa sĩ vẽ một nét, giám khảo bảo "hơi đỏ quá", họa sĩ có thể chỉnh sửa sắc độ đỏ một chút xíu.
- **Với Text (Discrete):** Họa sĩ viết chữ `A`, giám khảo bảo "nên là chữ `B`". Họa sĩ không thể sửa chữ `A` "một chút xíu" để thành chữ `B` được. Một là `A`, hai là `B`, không có gì ở giữa.

**Nỗi đau giải quyết:** Toán học của Deep Learning (Backpropagation) cần sự thay đổi "nhỏ xíu" và liên tục để học. Text lại nhảy cóc (rời rạc), khiến cho Generator của GAN không biết phải sửa mình như thế nào khi bị Discriminator chê.

## 2. Cách thức vận hành (How it works)
Để GAN làm việc được với Text (hoặc SQL), chúng ta có 2 chiến thuật chính:

### Chiến thuật A: "Giả vờ" liên tục (Gumbel-Softmax)
Thay vì chọn một từ duy nhất (argmax), chúng ta sử dụng một hàm toán học đặc biệt khiến cho mô hình xuất ra một "hỗn hợp" các từ. 
Ví dụ: 90% là `SELECT`, 5% là `INSERT`, 5% là `UPDATE`. 
Vì là con số %, nên Discriminator có thể góp ý: *"Bớt SELECT đi một tí, tăng UPDATE lên một tí"*.

### Chiến thuật B: Biến GAN thành một trò chơi (Reinforcement Learning - SeqGAN)
Chúng ta coi Generator như một người chơi game. Mỗi từ nó viết ra là một "hành động". Cuối câu, Discriminator sẽ chấm điểm (Reward). 
- Điểm cao: Generator nhớ để lần sau làm thế tiếp.
- Điểm thấp: Generator thử cách khác.

## 3. Giải mã công thức (Math Decoded)

| Công thức | Ý nghĩa "tiếng người" | Tại sao quan trọng? |
| --- | --- | --- |
| **Discrete Output** | "Chọn một trong hai". | Kẻ thù của GAN truyền thống (không thể tính đạo hàm). |
| **Gumbel-Softmax** | "Cái cầu nối giữa cứng và mềm". | Cho phép dòng thông tin từ Discriminator chảy ngược về Generator dù là dữ liệu chữ. |
| **Policy Gradient ($\nabla_\theta J(\theta)$)** | "Kim chỉ nam cho hành động". | Công thức cốt lõi của RL giúp Generator biết hướng nào là "đúng đắn" để nhận thưởng. |
| **Reward (R)** | "Lời khen của Giám khảo". | Thay thế cho Loss function truyền thống trong SeqGAN. |

## 4.2. Triển khai thực tế (Practical Implementation)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class GumbelSoftmax(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, temperature=1.0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.output = nn.Linear(hidden_dim, vocab_size)
        self.temperature = temperature
        
    def forward(self, x, hidden=None):
        embedded = self.embedding(x)
        if hidden is None:
            output, hidden = self.lstm(embedded)
        else:
            output, hidden = self.lstm(embedded, hidden)
        logits = self.output(output)
        return logits, hidden
    
    def gumbel_softmax_sample(self, logits):
        gumbel_noise = -torch.log(-torch.log(torch.rand_like(logits) + 1e-20) + 1e-20)
        y = (logits + gumbel_noise) / self.temperature
        return F.softmax(y, dim=-1)
    
    def generate(self, max_len, start_token, temperature=0.5):
        self.eval()
        generated = [start_token]
        hidden = None
        for _ in range(max_len):
            x = torch.tensor([[generated[-1]]).cuda() if torch.cuda.is_available() else torch.tensor([[generated[-1]]])
            logits, hidden = self.forward(x, hidden)
            probs = self.gumbel_softmax_sample(logits)
            next_token = torch.multinomial(probs.squeeze(), 1).item()
            generated.append(next_token)
            if next_token == 0:  # EOS token
                break
        return generated


class SeqGANGenerator(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.hidden_dim = hidden_dim
        
    def forward(self, x, state=None):
        embedded = self.embedding(x)
        if state is None:
            lstm_out, new_state = self.lstm(embedded)
        else:
            lstm_out, new_state = self.lstm(embedded, state)
        return lstm_out, new_state
    
    def get_policy(self, x):
        lstm_out, _ = self.forward(x)
        logits = self.output(lstm_out)
        return F.softmax(logits, dim=-1)
    
    def get_action(self, x, temperature=0.5):
        policy = self.get_policy(x)
        if temperature > 0:
            policy = F.softmax(torch.log(policy + 1e-20) / temperature, dim=-1)
        return torch.multinomial(policy, 1)


class PolicyGradientLoss(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, log_probs, rewards):
        loss = -torch.mean(log_probs * rewards)
        return loss


def compute_reward(generated_sql, discriminator, waf_rules=None):
    reward = 0.0
    
    with torch.no_grad():
        score = discriminator(generated_sql)
        reward += score.item()
    
    if waf_rules:
        for rule in waf_rules:
            if rule.match(generated_sql):
                reward += 0.5
                
    return reward
```

**Checklist triển khai SeqGAN cho SQL Injection:**
- [ ] Chuẩn bị SQL Injection corpus (tối thiểu 1000 samples)
- [ ] Xây dựng vocabulary cho SQL tokens
- [ ] Pre-train Generator bằng MLE loss (50 epochs)
- [ ] Thiết kế Discriminator với reward function
- [ ] Fine-tune bằng policy gradient
- [ ] Đánh giá: bypass rate trên WAF test

## 5. So sánh & Đối chiếu (Comparison)

| Tiêu chí | GAN cơ bản | Gumbel-Softmax GAN | SeqGAN | Transformer+GAN |
|----------|------------|------------------|-------|-----------------|
| Xử lý discrete output | ❌ Không được | ✅ Mềm hóa | ✅ RL-based | ✅ Tự nhiên |
| Gradient flow | ❌ Đứt gãy | ✅ Liên tục | ✅ Policy gradient | ✅ Đầy đủ |
| Sinh sequence dài | ⚠️ Khó | ⚠️ Trung bình | ✅ Tốt | ✅ Rất tốt |
| Training stability | ❌ Hay sụp đổ | ⚠️ Cần tuning | ✅ Tốt | ⚠️ Tốn tài nguyên |
| Thích hợp cho SQLi | ❌ Không | ✅ | ✅ **Phù hợp nhất** | ✅ Nếu có GPU |
| Reference | Vanilla | Jang et al., 2016 | Yu et al., 2017 | - |

## 6. Kết nối & Mở rộng (Connections)
- **Kết nối trong vault**: [[Deep Dive - VAE]] → [[Deep Dive - Diffusion]] → [[Deep Dive - Transformers]]
- **Mô hình liên quan:** WGAN (để ổn định training), RelGAN (cải tiến của Gumbel-Softmax), LeakGAN (hierarchical RL)
- **Câu hỏi mở:** Liệu có thể kết hợp Transformer (như GPT) làm Generator trong khung của GAN để tận dụng cả hai sức mạnh không?
- **Next steps:** Tiến hành implement SeqGAN cho SQL Injection với corpus có sẵn

## 7. Tài liệu tham khảo
- Paper: "SeqGAN: Sequence Generative Adversarial Nets with Policy Gradient" (2016) - https://arxiv.org/abs/1609.05473
- Paper: "Categorical Reparameterization with Gumbel-Softmax" (2016) - https://arxiv.org/abs/1611.01144
- Blog: Understanding Gumbel-Softmax (Lilian Weng) - https://lilianweng.github.io/posts/2017-08-15-why-gumbel-softmax/
