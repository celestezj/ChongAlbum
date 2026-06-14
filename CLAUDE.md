# Album Build System

## 目录结构

```
one_album/
├── Chong's photo gallery.html   # 原始 HTML 页面（硬编码数据）
├── base.css                     # 样式文件
├── demo.js                      # 交互逻辑
├── TweenMax.min.js              # GSAP 动画库
├── imagesloaded.pkgd.min.js     # 图片加载检测
├── build_output/
│   ├── album.json               # 相册数据（JSON）
│   ├── build_album.py           # 构建脚本（Python）
│   ├── template.html            # HTML 模板（含占位符）
│   ├── album_schema.md          # JSON 字段完整参考
│   └── index.html               # 默认构建生成的最终页面，注意拷贝到父级目录才能有效工作
└── CLAUDE.md                    # 本文件
```

## 构建流程

JSON 数据 → Python 脚本渲染 → 替换模板占位符 → 生成完整 HTML

## 快速使用

```bash
cd build_output
python build_album.py   # 默认使用 album.json + template.html → index.html
python build_album.py -j album.json -t template.html -o ../index.html   # 指定文件
```

## album.json 结构与字段

### 顶层

```json
{
  "albums": [ /* 照片条目 */ ],
  "about": { /* 关于信息 */ }
}
```

### albums[] 条目字段

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | int | 否 | 下标+1 | 预览编号，对应 `#preview-N` |
| `img` | string | **是** | - | 图片 URL |
| `title` | string | **是** | - | 主标题 |
| `text` | string | **是** | - | 副标题 |
| `title_hover` | string | 否 | =`title` | 悬停填充文字 |
| `title_style` | array | 否 | `[]` | 标题样式：`straight` / `bottom` / `left` |
| `text_style` | array | 否 | `[]` | 文字位置：`bottom` / `topcloser` / `bottomcloser` / `right` |
| `text_rotation` | string | 否 | 无 | 文字旋转：`rotated1`(+4°) / `rotated2`(-3°) / `rotated3`(-15°) |
| `text_reverse` | bool | 否 | `false` | 反色 |
| `deco` | string | 否 | 无 | 装饰符（语义名） |
| `deco_top` | bool | 否 | `false` | 装饰符置于顶部 |
| `quote` | string | 否 | 无 | 网格中显示的短描述（`box__content`） |
| `overlay` | string | 否 | 无 | 预览弹窗中的描述（`overlay__content`） |

### deco 对照表

| 语义名 | 显示 | HTML 实体 |
|--------|------|-----------|
| `cross` | ✞ | `&#10014;` |
| `star` | ✰ | `&#10032;` |
| `four` | ➃ | `&#10115;` |
| `seven` | ➐ | `&#10108;` |
| `arrow` | ➩ | `&#10153;` |

### about 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | **是** | 按钮文字 |
| `text_style` | array | 否 | 同 `albums[].text_style` |
| `text_rotation` | string | 否 | 同 `albums[].text_rotation` |
| `text_reverse` | bool | 否 | 默认 `true` |
| `link` | string | 否 | 点击跳转 URL |
| `content` | string | **是** | 描述文字（可含 HTML） |
| `pos` | int | 否 | 插入位置（在第pos个album后面插入，默认是插入在最后） |

### 模板占位符

| 占位符 | 替换为 |
|--------|--------|
| `{{album_grid}}` | 所有相册 grid 项 + About 项 |
| `{{album_overlay}}` | 所有相册 overlay 项 |

## 注意事项

- 新增照片只需在 `albums` 数组追加对象，`id` 省略自动按顺序生成
- About 项不是数组元素，是独立的顶层 `about` 对象
- `quote` 和 `overlay` 是两个独立字段：`quote` 出现在网格卡片中，`overlay` 出现在点击预览弹窗中
- 删除照片只需从数组中移除对应条目，id 不会自动重排（除非省略 id 字段）
