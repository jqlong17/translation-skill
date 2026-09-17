# 翻译 skill

把 EPUB 书籍翻译成中文的 Codex/Cursor skill。它的目标不是“抽文本然后粗翻”，而是在尽量保持 EPUB 原始结构的前提下，产出可阅读、可校验、可继续迭代的中文 EPUB。

当前包含的 skill：

- `academic-epub-translator`：面向学术、技术、语言学、认知科学、心理学等书籍的 EPUB -> 中文 EPUB 翻译工作流。

## 适合谁用

- 想让 Codex 或 Cursor 逐章翻译 EPUB 的用户。
- 想保留原书图片、脚注、链接、目录、页码锚点和引用结构的用户。
- 想把英文或其他语言的专业书翻成中文，并希望 AI 每阶段都能自检的用户。
- 想复用一个稳定 prompt/workflow，而不是每次重新写翻译要求的 AI agent。

## 它做什么

- 读取完整 EPUB，而不是只看标题、目录或摘要。
- 解包 EPUB 到工作目录，不修改源 EPUB。
- 按章节或小节循环执行：阅读 -> 翻译 -> XML 检查 -> 继续。
- 保留原始图片文件、manifest、spine、ID、内部链接、pagebreak、脚注回链。
- 对语言学例句、公式、代码、符号、判断标记等证据材料默认保留原文。
- 用内置脚本打包和验证译稿 EPUB。
- 用 `TRANSLATION_STATE.md` 记录进度、术语和验证日志，方便中断后继续。

## 安装到 Codex

把本仓库中的 skill 目录复制或软链接到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R academic-epub-translator ~/.codex/skills/
```

也可以用软链接，方便拉取仓库更新：

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/翻译skill/academic-epub-translator ~/.codex/skills/academic-epub-translator
```

## 安装到 Cursor

如果你在 Cursor 中使用本地 skills，可以放到 Cursor 的 skills 目录，例如：

```bash
mkdir -p ~/.cursor/skills
cp -R academic-epub-translator ~/.cursor/skills/
```

不同 Cursor 版本或个人配置的 skills 目录可能不同；原则是让 agent 能读到：

```text
academic-epub-translator/SKILL.md
```

## 给 AI agent 的用法

当用户要求翻译 EPUB 时，先读完整的：

```text
academic-epub-translator/SKILL.md
```

如果是语言学、认知科学或心理语言学书籍，再读：

```text
academic-epub-translator/LINGUISTICS_REFERENCE.md
```

然后严格执行这个循环：

1. 检查或创建 `TRANSLATION_STATE.md`。
2. 解包源 EPUB 到一个新的工作目录。
3. 一次处理一个完整小节；为了提速，可合并 2-4 个相邻短小节。
4. 直接在 XHTML 中翻译正文、标题、图注、alt、脚注。
5. 保留英语例句、形式标记、公式、图像和代码式内容，除非用户明确要求翻译。
6. 每批翻译后解析 XHTML，确认 XML 没坏。
7. 每章结束，或触及大量链接/图片/脚注后，打包 EPUB 并与源书验证结构不变量。
8. 更新 `TRANSLATION_STATE.md`，再继续下一批。

重要：最终可见成品应当是一个稳定文件，例如：

```text
书名（当前译稿）.epub
```

阶段检查点应放入 `checkpoints/` 或 `archive/`，不要把很多同名阶段 EPUB 散落在用户的 Downloads 或项目根目录。

## 常用命令

检查 EPUB：

```bash
python3 academic-epub-translator/scripts/inspect_epub.py /path/to/source.epub
```

解包 EPUB：

```bash
python3 academic-epub-translator/scripts/unpack_epub.py /path/to/source.epub /path/to/workdir
```

打包 EPUB：

```bash
python3 academic-epub-translator/scripts/package_epub.py /path/to/workdir /path/to/output.epub
```

覆盖稳定的“当前译稿”输出：

```bash
python3 academic-epub-translator/scripts/package_epub.py /path/to/workdir /path/to/书名（当前译稿）.epub --replace
```

验证 EPUB，并与源 EPUB 对比结构不变量：

```bash
python3 academic-epub-translator/scripts/validate_epub.py /path/to/output.epub --source /path/to/source.epub
```

## 质量门槛

译稿交付前至少确认：

- XHTML/XML 可以解析。
- EPUB 的 `mimetype` 位置和压缩方式正确。
- manifest、spine、内部链接、fragment、ID 没有损坏。
- 图片、表格、脚注、页码锚点数量与源书一致。
- 原图文件保持不变。
- 术语表和 `TRANSLATION_STATE.md` 与实际进度一致。
- 没有把作为证据的英文例句、公式、代码或判断标记误翻。

## 获取 EPUB

请使用你有权处理的 EPUB 文件，例如：

- 自己购买并允许个人处理的电子书。
- 作者、出版社或课程公开发布的 EPUB。
- 公版书和开放授权书籍，例如 Project Gutenberg、Standard Ebooks、OpenStax、DOAB、OAPEN。
- 学校、图书馆或机构订阅中允许下载和个人研究使用的 EPUB。

不要把这个 skill 用作规避版权、DRM 或平台使用条款的工具。AI agent 在处理用户提供的 EPUB 时，应默认提醒用户确认其拥有相应使用权。

## 版权提醒

本仓库不包含任何书籍正文或译文，只提供翻译工作流和校验脚本。请只翻译你有权处理的 EPUB 文件，并遵守所在地区的版权与使用限制。

## 许可证

MIT License. 见 [LICENSE](LICENSE)。
