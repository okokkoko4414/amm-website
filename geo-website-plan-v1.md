# GEO 官网整体方案 v1.0 — 官网制作项目

> 日期: 2026-05-22
> 制定人: CEO Agent
> 状态: 提案待审查
> 关联: GEO-1

---

## 0. 现状总结

**已完成的：**
- ✅ 竞品分析 (AMM-12) — 覆盖6家直接竞品 + 3家间接竞品
- ✅ 官网 MVP 已部署 — GitHub Pages (https://okokkoko4414.github.io/amm-website/)
- ✅ 2页结构: index.html (首页) + about.html (关于)
- ✅ 基础 SEO: canonical URL, structured data (Schema.org), meta description
- ✅ GEO 排名基线数据已采集
- ✅ 排名监控脚本 (geo-rank-monitor.py) 就绪
- ✅ 经营计划 v4.0 中明确了 Phase 0 官网目标

**当前 Gap：**
- ❌ 无自定义域名 (使用 GitHub Pages subpath)
- ❌ 缺少 CTA/转化路径 (pricing section 占位，无 contact form/signup)
- ❌ 无 Analytics/跟踪
- ❌ 无 case studies / social proof 区域
- ❌ 缺少 landing 页 (针对不同流量来源)
- ❌ 无 Blog/资源区块 (GEO 内容营销抓手)
- ❌ 无多语种版本 (Phase 0 可暂缓)
- ❌ 无后端服务 (联系表单等)

---

## 1. 架构方案

### 1.1 技术架构 (延续 v4.0 分离策略)

```
用户 → CDN (Cloudflare/Netlify)
                │
                ├── 静态资源: GitHub Pages (继续托管静态 HTML/CSS/JS)
                ├── 域名: amm-geo.com (自定义域名指向 CDN)
                │
                └── 后端 API(暂缓Phase 0):
                    └── 联系表单 → 可先用 Formspree/Google Form 替代
```

**Phase 0 原则：不引入后端服务，保持纯静态。** 用第三方服务弥补交互需求。

### 1.2 网站结构 (Phase 0 目标)

```
amm-geo.com/
├── index.html        → 首页 (Hero + 问题方案 + How It Works + 数据 + Pricing + CTA)
├── about.html        → 关于我们 (已存在，需增强)
├── services.html     → 服务详情 (GEO 服务说明、交付流程) [新建]
├── pricing.html      → 独立定价页 + 自助下单 [新建]
├── contact.html      → 联系/咨询表单 [新建]
├── blog/             → 博客目录 [Phase 1]
│   └── index.html    → 博客列表页 [Phase 1]
└── case-studies/     → 案例研究 [Phase 1]
    └── index.html    → 案例列表 [Phase 1]
```

### 1.3 SEO/GEO 策略

| 维度 | 当前状态 | 目标 (Phase 0) | 负责部门 |
|------|---------|---------------|---------|
| 结构化数据 | ✅ Schema.org Organization | 增加 FAQ/Service/BreadcrumbList | 企划品牌部 |
| Sitemap | ❌ 无 | XML sitemap + robots.txt | 产品研发部 |
| OG 标签 | ✅ 基础 | 完善各页面 OG/Twitter Card | 企划品牌部 |
| 关键词策略 | ❌ 未系统化 | 聚焦10个GEO关键词 | 企划品牌部 |
| AI 搜索优化 | ✅ 基线已采集 | 每周监控+内容迭代 | 企划品牌部 |
| 页面速度 | ⚠️ 未测 | Lighthouse 90+ | 产品研发部 |
| 内链结构 | ⚠️ 基础但单向 | 页面间互相链接, 面包屑导航 | 产品研发部 |

### 1.4 关键词策略 (Top 10 GEO 关键词)

基于竞品分析，建议 Phase 0 聚焦以下关键词：

| 关键词 | 搜索意图 | 难度估计 | 优先级 |
|--------|---------|---------|-------|
| generative engine optimization | 信息型 | 中-低 | 🔴 P0 |
| GEO marketing agency | 商业型 | 低 | 🔴 P0 |
| AI search optimization | 信息型 | 中 | 🟡 P1 |
| GEO SEO services | 商业型 | 低 | 🟡 P1 |
| AI content optimization for search | 信息型 | 中 | 🟡 P1 |
| ChatGPT ranking optimization | 商业型 | 中-低 | 🟢 P2 |
| Perplexity AI optimization | 商业型 | 低 | 🟢 P2 |
| Gemini search ranking | 商业型 | 低 | 🟢 P2 |
| AI visibility agency | 品牌型 | 低 | 🟢 P2 |
| optimize for AI search engines | 信息型 | 中 | 🟢 P2 |

---

## 2. 分步执行计划

### Phase 0 (M1-W2 到 M1-W4) — 网站升级

| 周次 | 任务 | 产出 | 负责部门 |
|------|------|------|---------|
| W2-1 | 自定义域名配置 (amm-geo.com) + CDN | 域名可访问 | 产品研发部 |
| W2-2 | robots.txt + sitemap.xml + 性能优化 | 技术SEO就位 | 产品研发部 |
| W2-3 | services.html 页面 (GEO服务详情) | 服务说明页上线 | 企划品牌部 |
| W2-4 | pricing.html 页面 (独立定价+CTA) | 定价转化页上线 | 企划品牌部+市场部 |
| W2-5 | contact.html (Formspree 嵌入表单) | 咨询入口就位 | 企划品牌部 |
| W3-1 | 结构化数据增强 (FAQ/Breadcrumb) | Schema.org 完善 | 企划品牌部 |
| W3-2 | 关键词内容植入 (10个页面Meta优化) | 页面SEO就位 | 企划品牌部 |
| W3-3 | 数据分析设置 (Google Analytics/Plausible) | 数据跟踪就位 | 产品研发部 |
| W4-1 | GEO 排名第二次基线采集 & 对比 | 第一次排名变化数据 | 企划品牌部 |
| W4-2 | 整体 UAT + 问题修复 | 上线 | CEO Agent |

### Phase 1 (M2+) — 内容增强

- 博客/Blog系统启动
- Case studies 页面
- 多语种版本 (日/韩/德)
- A/B 测试 landing pages

---

## 3. 验证标准

Phase 0 官网成功标准（与经营计划 v4.0 一致）：

| 指标 | 目标值 | 测量方式 | 负责人 |
|------|-------|---------|--------|
| 官网可访问性 | URL 有效 24/7 | 手动/down detector | CEO |
| 结构化数据验证 | Google Rich Results 无错误 | 测试工具 | 产品研发部 |
| GEO 排名 | 10个目标关键词在ChatGPT/Perplexity前50 | 监控脚本 | 企划品牌部 |
| 联系表单可用 | 表单提交成功可达 CEO | 手动测试 | 产品研发部 |
| 页面加载 | Lighthouse Performance ≥ 85 | Lighthouse | 产品研发部 |

---

## 4. 部门协调矩阵

| 任务模块 | 主导部门 | 协作部门 | 调度方式 |
|---------|---------|---------|---------|
| 域名+CDN+部署 | 产品研发部 | — | 直接子任务 |
| 页面内容撰写 | 企划品牌部 | 市场部(关键词) | 内容+关键词同步 |
| SEO/GEO优化 | 企划品牌部 | 产品研发部(技术) | 技术SEO+内容SEO并行 |
| 转化路径设计 | 市场部 | 企划品牌部 | 定价+CTA文案 |
| 数据分析 | 产品研发部 | 企划品牌部 | 工具部署+数据解读 |
| 竞品持续追踪 | 企划品牌部 | — | 每月更新 |

---

## 5. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 自定义域名DNS延迟 | 中 | 低 | 提前配置；先继续使用 GitHub Pages |
| 静态表单不可靠 | 低 | 中 | Formspree 有免费额度，备选 Google Form |
| SEO优化效果延迟 | 高 | 中 | 接受SEO需要时间，以排名基线测量为凭证 |
| 内容创作质量不足 | 中 | 中 | 先用结构化+模板化内容，迭代优化 |
| 部门Agent可用性 | 低 | 高 | CEO亲自承担关键路径任务 |

---

*本方案根据 竞品分析(AMM-12)、经营计划v4.0、CEO架构审查 综合制定，待审查确认后分派子任务。*
