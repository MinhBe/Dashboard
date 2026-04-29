---
aliases: []
created: 2026-04-29 02:00:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [generative-ai, index, overview]
category: [research]
---

# Generative AI - Bản đồ Tri thức (Knowledge Map)

> Đây là điểm bắt đầu để điều hướng giữa các chủ đề về Generative AI trong vault này.

---

## Lộ trình học tập (Learning Path)

```
1. Nền tảng
   [[Deep Dive - Transformers]] → Hiểu cơ chế Attention, nền tảng của mọi generative model hiện đại
   
2. Các mô hình sinh
   [[Deep Dive - VAE]] → Mô hình nén & tái tạo cơ bản
   [[Deep Dive - GAN for Text]] → SeqGAN, Gumbel-Softmax cho text rời rạc
   [[Deep Dive - Diffusion]] → Mô hình khử nhiễu, diversity cao

3. So sánh & Quyết định
   [[Deep Dive - So sánh Generative Models]] → Chọn đúng mô hình cho bài toán
```

---

## Tổng quan các mô hình

| Mô hình | Điểm mạnh | Điểm yếu | Phù hợp cho |
|--------|----------|---------|-----------|
| VAE | Nhanh, ổn định, latent control | Output "mờ" | Data augmentation |
| GAN | Nhanh | Không ổn định, mode collapse | Không khuyến nghị cho text |
| SeqGAN/Gumbel | RL-based, bypass WAF | Cần reward engineering | **SQL Injection generation** |
| Diffusion | Diversity cao nhất | Chậm, text chưa ổn | Future research |
| Transformer | Syntax-aware | Cần nhiều data | Large-scale generation |

---

## Bảng quyết định (Decision Matrix)

| Bạn cần... | Mô hình nên dùng |
|-----------|-----------------|
| Baseline nhanh | VAE |
| Sinh biến thể đa dạng | SeqGAN |
| Bypass WAF | SeqGAN với RL |
| Cú pháp SQL đúng | Transformer |
| Experiment/research | Diffusion (theo dõi) |

---

## Các câu hỏi mở (Open Questions)

- [ ] Kết hợp VAE + SeqGAN có hiệu quả hơn không?
- [ ] Diffusion có thể beat SeqGAN với small dataset không?
- [ ] Transformer + GAN hybrid có khả thi không?

---

## Tài liệu nền tảng bổ trợ

- [[Deep Dive - Math Foundation for DL]] - Nền tảng toán học
- [[math-foundation-for-dl]] - Công thức cốt lõi

---

## Progress Tracker

- [x] Transformers - Core concept
- [x] VAE - Basic generative
- [x] GAN for Text - SeqGAN, Gumbel-Softmax
- [x] Diffusion - Advanced
- [x] So sánh - Decision making
- [ ] Implementation - CWGAN fix cho SQL Injection
- [ ] Testing - WAF bypass evaluation