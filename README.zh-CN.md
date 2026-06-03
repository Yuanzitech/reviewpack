# Reviewpack

面向 AI 辅助 Pull Request Review 的隐私优先上下文包生成工具。

Reviewpack 帮助开源维护者和工程团队在进行人工 Review 或 AI 辅助 Review 之前，先生成结构化、可复用、可审查的 PR 上下文。

它不是另一个吵闹的 AI Review Bot。Reviewpack 更像一个 Review 前置上下文层：它会收集 PR 元信息、变更文件、测试信号、文档信号、依赖信号、风险提示和建议 Review 重点，然后生成清晰的 Review Context Pack。

## Language

- English: README.md
- 简体中文: README.zh-CN.md

## 为什么需要 Reviewpack？

AI 编程工具很强，但 Review 质量高度依赖上下文。

很多直接 AI Review 的流程，是从原始 diff 开始的。这种方式容易遗漏项目级信息，例如：

- 哪些文件属于高风险区域？
- 是否更新了测试？
- 是否更新了文档？
- 是否修改了依赖？
- 这个 PR 是否过大？
- 是否影响 CI、配置或发布行为？
- 维护者应该优先关注什么？

Reviewpack 的目标是在 Review 开始之前，先把这些上下文整理好。

## 快速开始

本地开发安装：

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

Windows PowerShell：

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"

从示例 fixture 生成 review pack：

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

生成 review pack，并同时生成 AI 输入预览：

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

查看生成文件：

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/reviewpack.json

## 示例输出

示例 PR summary：

    examples/output/pr-summary.example.md

这个示例可以帮助你快速理解 Reviewpack 生成的结构化 Review 上下文长什么样。

## 核心思路

直接 AI Review：

    PR diff -> AI -> review comments

Reviewpack 工作流：

    PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

也就是说，Reviewpack 不试图替代 reviewer，而是先把 Review 所需的上下文准备好。

## 当前支持的输入模式

Reviewpack 当前支持：

- Fixture 输入
- 本地 git diff 输入
- GitHub Pull Request metadata 输入

示例：

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

    reviewpack local --base main --head HEAD --output .reviewpack

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

## 隐私优先默认行为

对于 fixture 和 local git 工作流，Reviewpack 默认在本地运行。

默认情况下，它不会把代码、diff、分支名、commit message、环境变量、仓库元信息或终端信息发送给任何外部 AI 服务。

GitHub 模式会访问网络，但只用于从 GitHub API 获取用户明确指定的 Pull Request metadata 和 changed file statistics。

未来如果加入 AI provider 调用，也会是可选、显式开启的功能。用户应该能够控制哪些上下文会发送给 AI provider。

当前隐私相关能力包括：

- 本地 fixture 模式
- 本地 git diff 模式
- GitHub PR metadata 模式
- 不调用 AI 的 AI-ready prompt 生成
- 不调用 AI 的 AI input preview 生成
- 针对预览文本的基础 secret-like value 脱敏
- 默认不上传 raw diff
- 默认不包含 branch name
- 默认不包含 commit message
- 尽可能保持 local-first

## Reviewpack 会生成什么？

一个 review pack 可能包括：

- PR summary
- Changed file overview
- Risk checklist
- Test impact
- Documentation impact
- Dependency impact
- CI and configuration impact
- Suggested review focus
- AI-ready review prompt
- AI input preview
- Machine-readable JSON output

示例输出目录：

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

## 当前状态

Reviewpack 目前处于早期开发阶段。

当前 milestone 支持：

- 本地 fixture 输入
- 本地 git diff 输入
- GitHub PR metadata 输入
- Markdown 和 JSON 结构化输出
- 可选 AI input preview
- preview 文本中的 secret-like value 脱敏
- 默认不调用 AI

## 文档

- 使用指南：docs/usage.md
- 隐私模型：docs/privacy.md
- 设计说明：docs/design.md
- 本地 git diff 模式：docs/local-git.md
- GitHub 支持：docs/github.md
- AI input preview：docs/ai-preview.md
- 集成原则：docs/integrations.md
- Roadmap：docs/roadmap.md
- Release checklist：docs/release-checklist.md
- 示例说明：examples/README.md

## Roadmap

高层 roadmap：

- v0.1.x：打磨核心本地工作流
- v0.2.x：改进隐私感知 AI preview 和配置能力
- v0.3.x：增强 GitHub Pull Request 工作流
- v0.4.x：增加 GitHub Actions integration 和 maintainer automation

详细 roadmap：

    docs/roadmap.md

## 这个项目为什么存在？

Reviewpack 的出发点是：AI 辅助 Review 的质量取决于它拿到的上下文。

与其让 AI 直接面对原始 diff，Reviewpack 选择先生成结构化、可复用、隐私友好的上下文。

这样维护者可以更容易：

- 理解这个 PR 改了什么
- 识别 Review 风险
- 判断是否缺测试或文档
- 在人工 Review 和 AI Review 之间复用上下文
- 控制哪些信息可以被准备给 AI

## 不做什么

Reviewpack 不打算：

- 自动 approve PR
- 自动 merge PR
- 替代人类维护者
- 在 PR 里刷大量噪音评论
- 默认上传代码
- 让 AI 成为基础功能的必要条件

## 设计原则

1. Local-first
2. Privacy-first
3. AI-optional
4. Human-readable
5. Machine-readable
6. Maintainer-controlled
7. Tool-agnostic

Reviewpack 应该可以配合人类 reviewer、Codex、Cursor、Cline、OpenCode、Claude Code、GitHub Copilot 和其他 AI coding assistants 使用。

## 贡献

欢迎贡献文档、测试、风险规则、示例和隐私相关改进。

请先阅读：

    CONTRIBUTING.md

安全相关问题请阅读：

    SECURITY.md

## License

MIT
