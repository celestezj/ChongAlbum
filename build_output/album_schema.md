# album.json 编写指南

## 顶层结构

```json
{
  "albums": [
    { /* 相册条目 */ },
    { /* 相册条目 */ }
  ],
  "about": { /* 关于信息 */ }
}
```

---

## album 条目字段

每个 `albums[]` 中的对象表示一张照片。

### 基本字段

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | int | 否 | 数组下标+1 | 预览编号，对应 `#preview-N` |
| `img` | string | **是** | - | 图片 URL |
| `title` | string | **是** | - | 主标题文字 |
| `text` | string | **是** | - | 副标题文字 |

### 可选字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title_hover` | string | =`title` | 悬停填充文字（`data-hover` 属性） |
| `title_style` | array | `[]` | 标题样式修饰，见下方说明 |
| `text_style` | array | `[]` | 副标题位置修饰，见下方说明 |
| `text_rotation` | string | 无 | 副标题旋转，见下方说明 |
| `text_reverse` | bool | `false` | 副标题反色（白底黑字变黑底白字） |
| `deco` | string | 无 | 装饰符号，见下方对照表 |
| `deco_top` | bool | `false` | 装饰符号置于顶部 |
| `quote` | string | 无 | 网格中显示的短描述文字（`box__content`） |
| `overlay` | string | 无 | 预览弹窗中的长描述文字（`overlay__content`） |

### title_style 可选值

可组合使用，如 `["straight", "bottom"]`：

| 值 | 效果 |
|------|------|
| `"straight"` | 水平书写（默认 vertical-rl） |
| `"bottom"` | 底部定位 |
| `"left"` | 左侧定位 |

### text_style 可选值

可组合使用，如 `["bottom", "right"]`：

| 值 | 效果 |
|------|------|
| `"bottom"` | 底部 |
| `"topcloser"` | 靠近顶部 |
| `"bottomcloser"` | 靠近底部 |
| `"right"` | 右对齐 |

### text_rotation 可选值

| 值 | 效果 |
|------|------|
| `"rotated1"` | 旋转 +4° |
| `"rotated2"` | 旋转 -3° |
| `"rotated3"` | 旋转 -15° |

### deco 语义化名称对照表

| 名称 | 显示 | HTML 实体 |
|------|------|-----------|
| `"cross"` | ✞ | `&#10014;` |
| `"star"`  | ✰    | `&#10032;` |
| `"four"` | ➃ | `&#10115;` |
| `"seven"` | ➐ | `&#10108;` |
| `"arrow"` | ➩ | `&#10153;` |

---

## about 字段

```json
"about": {
  "text": "About",
  "text_rotation": "rotated2",
  "text_reverse": true,
  "link": "https://www.wenchong.space",
  "content": "<strong>...</strong> description with HTML"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | **是** | 按钮文字 |
| `text_style` | array | 否 | 同 album 的 text_style |
| `text_rotation` | string | 否 | 同 album 的 text_rotation |
| `text_reverse` | bool | 否 | 同 album 的 text_reverse（About 默认 true） |
| `link` | string | 否 | 点击跳转链接，省略则不跳转 |
| `content` | string | **是** | 描述文字（可含 HTML 标签） |

---

## 完整示例

```json
{
  "albums": [
    {
      "id": 1,
      "img": "https://gitee.com/Langwenchong/figure-bed/raw/master/SKY_20210513_225400__edit_284979137428388.jpg",
      "title": "Memo",
      "text": "Valley",
      "deco": "cross",
      "quote": "\"May all the beauty in the world be at the right time.\"",
      "overlay": "\"You are like a dazzling light in a mountain stream that illuminates my whole world\""
    },
    {
      "id": 2,
      "img": "https://gitee.com/Langwenchong/figure-bed/raw/master/IMG_20210101_230456.jpg",
      "title": "Wish",
      "title_style": ["straight", "bottom"],
      "text": "Fireworks",
      "text_style": ["bottom"],
      "text_rotation": "rotated1",
      "deco": "four",
      "deco_top": true,
      "overlay": "-The fireworks were beautiful that night and I made a good wish."
    },
    {
      "id": 4,
      "img": "https://gitee.com/Langwenchong/figure-bed/raw/master/SKY_20210425_111925__edit_285943484172511.jpg",
      "title": "Dragon",
      "text": "Adventure",
      "text_style": ["bottom", "right"],
      "text_rotation": "rotated3",
      "overlay": "Even if there are many dangers ahead, you and I will go ahead"
    },
    {
      "id": 18,
      "img": "https://gitee.com/Langwenchong/figure-bed/raw/master/SKY_20210206_185723__edit_190504103262075.jpg",
      "title": "Sea",
      "text": "deep",
      "quote": "\"The soft light roams under the sea\"",
      "overlay": "The soft light roams under the sea"
    },
  ],
  "about": {
    "text": "About",
    "link": "https://example.com",
    "content": "<strong>Album</strong> description here."
  }
}
```

## 使用方式

1. 编写或编辑 `album.json`
2. 在 HTML 模板中使用 `{{album_grid}}` 和 `{{album_overlay}}` 占位符
3. 运行 `python build_album.py` 生成最终 HTML
