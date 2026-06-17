# Reviewpack

面向 AI 辅助 Pull Request Review 的隐私优先上下面向 AI 辅助 Pull Request Review 的隐私优先上下文包生成工具。
- Risk checklist
- Reviewer checklist
- Release note hints
- Suggested review focus
- AI-ready review prompt
- AI handoff instructions
- AI context bundle
- AI input preview
- Machine-readable JSON output

示例输出目录：

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/reviewer-checklist.md
    .reviewpack/release-note-hints.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-handoff.md
    .reviewpack/ai-context.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

输出产物说明：

    docs/output-artifacts.md
    docs/artifact-contract.md

JSON 输出说明：

    docs/json-output.md
    docs/integration-json.md

Draft JSON schema：

    schemas/reviewpack-result.schema.json

示例输出文件：

    examples/output/

## AI handoff

Reviewpack 默认不会调用 AI provider。

它会生成本地文件，用户可以先检查，再决定是否分享给 AI 工具。

如果 AI assistant 可以读取当前 workspace 文件，可以说：

    Please read .reviewpack/ai-handoff.md and follow it.

如果 AI assistant 不能读取本地文件，但可以上传一个文件，上传：

    .reviewpack/ai-context.md

如果只能复制粘贴，使用：

    .reviewpack/ai-review-prompt.md

更多说明：

    docs/ai-handoff.md

## 隐私优先默认行为

对于 demo、fixture 和 local git 工作流，Reviewpack 默认在本地运行。

默认情况下，它不会把代码、diff、commit message、环境变量、仓库 secrets 或终端信息发送给任何外部 AI 服务。

GitHub 模式会访问网络，但只用于从 GitHub API 获取用户明确指定的 Pull Request metadata 和 changed file statistics。

GitHub 模式可能会把 labels、base/head branch 名称、commit count、draft status 和 changed file status 写入本地生成的 artifacts。

当前隐私相关能力包括：

- 本地 demo 模式
- 本地 fixture 模式
- 本地 git diff 模式
- GitHub PR metadata 模式
- GitHub Action artifact 模式
- 可选短 PR comment mode
- 可配置输出文件
- 可配置风险阈值
- 可配置高风险路径
- 可配置路径分类
- 不调用 AI 的 AI-ready prompt 生成
- 不调用 AI 的 AI handoff
- 不调用 AI 的 AI context bundle
- 不调用 AI 的 AI input preview
- 不调用 AI 的 release note hints
- 不调用 AI 的 reviewer checklist
- 针对 preview 文本的基础 secret-like value 脱敏
- 默认不上传 raw diff
- 默认不上传完整源代码
- 默认不包含 commit message
- 默认不评论 PR

## 文档

- 项目状态：docs/status.md
- 安装指南：docs/installation.md
- 命令指南：docs/commands.md
- 配置指南：docs/configuration.md
- 配置 schema：docs/config-schema.md
- 输出产物：docs/output-artifacts.md
- Artifact contract：docs/artifact-contract.md
- JSON 输出：docs/json-output.md
- JSON 集成指南：docs/integration-json.md
- v1.0 readiness：docs/v1-readiness.md
- 使用指南：docs/usage.md
- 隐私模型：docs/privacy.md
- 设计说明：docs/design.md
- 本地 git diff 模式：docs/local-git.md
- GitHub 支持：docs/github.md
- GitHub Action：docs/github-action.md
- AI handoff：docs/ai-handoff.md
- AI input preview：docs/ai-preview.md
- Release note hints：docs/release-note-hints.md
- Reviewer checklist：docs/reviewer-checklist.md
- 集成原则：docs/integrations.md
- Roadmap：docs/roadmap.md
- Release checklist：docs/release-checklist.md
- 示例说明：examples/README.md

## 核心思路

直接 AI Review：

    PR diff -> AI -> review comments

Reviewpack 工作流：

    PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

也就是说，Reviewpack 不试图替代 reviewer，而是先把 Review 所需的上下文准备好。

## 当前状态

Reviewpack 目前是一个已发布到 PyPI 的早期产品。

当前支持：

- PyPI 安装
- Demo 模式
- 本地 fixture 输入
- 本地 git diff 输入
- 增强的 GitHub PR metadata 输入
- GitHub Action artifact 输出
- 可选短 PR comment mode
- Markdown 和 JSON 结构化输出
- reviewpack.json draft JSON schema
- JSON integration guidance
- 可配置规则和输出
- 改进后的 Review artifacts
- Reviewer checklist
- Release note hints
- AI handoff
- AI context bundle
- 可选 AI input preview
- preview 文本中的 secret-like value 脱敏
- 默认不调用 AI

推荐首次体验流程：

    pip install reviewpack
    reviewpack demo
    reviewpack handoff

详细项目状态请查看：

    docs/status.md

## Roadmap

近期路线：

- v0.7.x：配置和 artifact contract 继续稳定化
- v0.8.x：GitHub workflow 验证
- v0.9.x：1.0 前稳定化
- v1.0.0：稳定 CLI 和 artifact contract

详细 roadmap：

    docs/roadmap.md

v1.0 readiness checklist：

    docs/v1-readiness.md

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

## License

MIT

## Language

- English: README.md
- 简体中文: README.zh-CN.md

Reviewpack 帮助开源维护者和工程团队在进行人工 Review 或 AI 辅助 Review 之前，先生成结构化、可复用、可审查的 PR 上下文。

它不是另一个吵闹的 AI Review Bot。Reviewpack 更像一个 Review 前置上下文层：它会收集 PR 元信息、变更文件、测试信号、文档信号、依赖信号、风险提示、release note hints、reviewer checklist、AI handoff instructions 和建议 Review 重点，然后生成清晰的 Review Context Pack。

## 快速开始

安装 Reviewpack：

    pip install reviewpack

生成一个 demo review pack：

    reviewpack demo

Reviewpack 默认会把输出写入：

    .reviewpack/

查看 AI handoff 指引：

    reviewpack handoff

如果你的 AI assistant 可以读取当前 workspace 文件，可以对它说：

    Please read .reviewpack/ai-handoff.md and follow it.

如果 AI assistant 不能读取本地文件，但可以上传一个文件，上传：

    .reviewpack/ai-context.md

如果只能复制粘贴，使用：

    .reviewpack/ai-review-prompt.md

## 为什么需要 Reviewpack？

AI 编程工具很强，但 Review 质量高度依赖上下文。

很多直接 AI Review 的流程，是从原始 diff 开始的。这种方式容易遗漏项目级信息，例如：

- 哪些文件属于高风险区域？
- 是否更新了测试？
- 是否更新了文档？
- 是否修改了依赖？
- 这个 PR 是否过大？
- 是否影响 CI、配置或发布行为？
- 这个 PR 是否需要写入 release notes？
- 维护者应该优先关注什么？

Reviewpack 的目标是在 Review 开始之前，先把这些上下文整理好。

## 常见工作流

### 首次体验

    reviewpack demo

### 已有 GitHub Pull Request

    reviewpack github https://github.com/owner/repo/pull/123

GitHub 模式可能会收集 PR state、draft 状态、base/head branch 名称、commit 数量、labels、changed file status 和 changed file statistics。

GitHub 模式默认不会收集 raw diff 或完整源代码。

public repository 通常不需要 token。

private repository 或遇到 GitHub API rate limit 时，可能需要：

    REVIEWPACK_GITHUB_TOKEN=YOUR_TOKEN reviewpack github https://github.com/owner/repo/pull/123

### 本地开发

    reviewpack local

默认比较：

    main...HEAD

### Fixture 输入

    reviewpack from-fixture simple-pr.json

fixture 文件必须已经存在。

首次体验建议使用：

    reviewpack demo

### 命令指引

    reviewpack guide

查看 CLI 参数：

    reviewpack --help
    reviewpack github --help
    reviewpack local --help

## 配置

Reviewpack 可以通过以下文件进行配置：

    .reviewpack.yml

配置文件是可选的。

如果不存在配置文件，Reviewpack 会使用隐私优先的默认行为。

示例：

    outputs:
      ai_context: true
      ai_handoff: true
      reviewer_checklist: true
      release_note_hints: true

    risk:
      large_pr_files: 20
      large_pr_lines: 500
      high_risk_paths:
        - .github/workflows/
        - pyproject.toml

    paths:
      docs:
        - docs/
        - README.md
      tests:
        - tests/

使用自定义配置文件：

    reviewpack demo --config path/to/reviewpack.yml

更多说明：

    docs/configuration.md
    docs/config-schema.md
    examples/.reviewpack.yml

## GitHub Action

Reviewpack 可以在 GitHub Actions 中运行，并把生成的 review pack 作为 workflow artifact 上传。

示例 workflow：

    name: Reviewpack

    on:
      pull_request:

    jobs:
      reviewpack:
        runs-on: ubuntu-latest

        permissions:
          contents: read
          pull-requests: read

        steps:
          - name: Check out repository
            uses: actions/checkout@v4

          - name: Run Reviewpack
            uses: Yuanzitech/reviewpack@v0.7.0
            with:
              mode: github
              pr-url: ${{ github.event.pull_request.html_url }}
              github-token: ${{ github.token }}

默认情况下，Action 会上传一个 workflow artifact：

    reviewpack-output

workflow 完成后，可以在 GitHub Actions run 页面下载这个 artifact。

推荐优先查看：

    pr-summary.md
    reviewer-checklist.md
    risk-checklist.md
    release-note-hints.md
    ai-handoff.md
    ai-context.md

当前 GitHub Action 集成默认不会自动评论 PR，也不会调用 AI provider。

可以显式开启可选 PR comment mode：

    comment: "true"

comment mode 会发布或更新一条短的指引评论。它不会把完整 review pack 粘贴到 PR 评论里。

comment mode 需要：

    permissions:
      contents: read
      pull-requests: write

更多说明：

    docs/github-action.md

示例：

    examples/github-action.yml
    examples/github-action-local.yml
    examples/github-action-comment.yml

## Reviewpack 会生成什么？

一个 review pack 可能包括：

- PR summary
