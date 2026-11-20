---
title: Trie
summary: Prefiks daraxti. So'zlarni harfma-harf saqlash, prefiks bo'yicha O(L) vaqtda tezkor qidirish va avtoto'ldirish (autocomplete) tuzilmasi.
---

## Trie nima

**Trie** (inglizcha *re**trie**val* — "qidirib topish" so'zidan olingan, ko'pincha "tray" deb talaffuz qilinadi) — bu matnli ma'lumotlarni, xususan so'zlar va ularning prefikslarini saqlash uchun mo'ljallangan maxsus **daraxtsimon ma'lumotlar tuzilmasi**.

Oddiy qidiruv usullarida so'zni qidirish butun so'zni solishtirishni talab qilsa, Trie'da qidiruv harfma-harf daraxt shoxlari bo'ylab tushish orqali amalga oshiriladi.

```
       (ROOT)
       /    \
      c      d
     / \      \
    a   o      o
   /     \      \
  t*      g*     g*
(cat)   (dog)  (dog)
```
> Yuqoridagi daraxtda `cat` va `dog` so'zlari saqlangan. Yulduzcha (`*`) so'z shu tugunda tugaganini (`is_end = True`) bildiradi.

## Qanday tuzilgan

Har bir Trie tuguni (node) odatda ikkita asosiy ma'lumotni saqlaydi:
1. `children` — keyingi harflarga olib boruvchi bolalar ro'yxati (hash map / dictionary yoki 26 ta harflik massiv).
2. `is_end` — aynan shu tugunda biror so'z to'liq tugaganmi-yo'qligini ko'rsatuvchi mantiqiy qiymat (`True`/`False`).

## Amallar va murakkablik

`L` — kiritilayotgan yoki qidirilayotgan so'zning uzunligi.
`N` — lug'atdagi so'zlar soni.
`Σ` (Sigma) — alifbodagi belgilar soni (masalan, ingliz tili kichik harflari uchun 26).

| Amal | Vaqt | Xotira | Izoh |
|------|------|--------|------|
| So'z qo'shish (Insert) | O(L) | O(L) | Harfma-harf shoxlar bo'ylab tushiladi |
| So'zni qidirish (Search) | O(L) | O(1) | So'z oxiri tuguniga yetib `is_end` tekshiriladi |
| Prefiksni tekshirish (StartsWith) | O(L) | O(1) | Prefiks tuguniga yetib borilsa kifoya |
| Eng uzun umumiy prefiks (LCP) | O(S) | O(S) | Yagona shoxli zanjir bo'ylab yuriladi |
| Umumiy xotira hajmi | — | O(N · L · Σ) | Barcha tugunlar va bolalar havolalari |

## Tugun (Node) yaratish

Trie tugunining har bir dasturlash tilidagi ko'rinishi:

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # harf -> TrieNode
        self.is_end = False
```

```php
class TrieNode {
    public $children = [];
    public $isEnd = false;
}
```

```go
type TrieNode struct {
	children map[rune]*TrieNode
	isEnd    bool
}

func NewTrieNode() *TrieNode {
	return &TrieNode{children: make(map[rune]*TrieNode)}
}
```

## Insert: So'z qo'shish

Ildizdan boshlab har bir harf tekshiriladi. Agar harf mavjud bo'lmasa, yangi tugun yaratiladi. So'z tugagach, oxirgi tugunning `is_end` belgisi `True` qilinadi.

```python
def insert(root: TrieNode, word: str) -> None:
    curr = root
    for ch in word:
        if ch not in curr.children:
            curr.children[ch] = TrieNode()
        curr = curr.children[ch]
    curr.is_end = True
```

```php
function insert($root, $word) {
    $curr = $root;
    for ($i = 0; $i < strlen($word); $i++) {
        $ch = $word[$i];
        if (!isset($curr->children[$ch])) {
            $curr->children[$ch] = new TrieNode();
        }
        $curr = $curr->children[$ch];
    }
    $curr->isEnd = true;
}
```

```go
func (t *TrieNode) Insert(word string) {
	curr := t
	for _, ch := range word {
		if _, ok := curr.children[ch]; !ok {
			curr.children[ch] = NewTrieNode()
		}
		curr = curr.children[ch]
	}
	curr.isEnd = true
}
```

## Search va StartsWith (Prefiks qidirish)

So'zni to'liq qidirish (`Search`) bilan prefiks qidirish (`StartsWith`) o'rtasidagi yagona farq: `Search` da so'z oxiridagi tugun `is_end == True` bo'lishi shart, `StartsWith` da esa harflar zanjiri mavjud bo'lsa yetarli.

```python
def search(root: TrieNode, word: str) -> bool:
    curr = root
    for ch in word:
        if ch not in curr.children:
            return False
        curr = curr.children[ch]
    return curr.is_end

def starts_with(root: TrieNode, prefix: str) -> bool:
    curr = root
    for ch in prefix:
        if ch not in curr.children:
            return False
        curr = curr.children[ch]
    return True
```

```php
function search($root, $word) {
    $curr = $root;
    for ($i = 0; $i < strlen($word); $i++) {
        $ch = $word[$i];
        if (!isset($curr->children[$ch])) return false;
        $curr = $curr->children[$ch];
    }
    return $curr->isEnd;
}

function startsWith($root, $prefix) {
    $curr = $root;
    for ($i = 0; $i < strlen($prefix); $i++) {
        $ch = $prefix[$i];
        if (!isset($curr->children[$ch])) return false;
        $curr = $curr->children[$ch];
    }
    return true;
}
```

```go
func (t *TrieNode) Search(word string) bool {
	curr := t
	for _, ch := range word {
		if next, ok := curr.children[ch]; ok {
			curr = next
		} else {
			return false
		}
	}
	return curr.isEnd
}

func (t *TrieNode) StartsWith(prefix string) bool {
	curr := t
	for _, ch := range prefix {
		if next, ok := curr.children[ch]; ok {
			curr = next
		} else {
			return false
		}
	}
	return true
}
```

## Longest Common Prefix masalasida qo'llash

Trie yordamida barcha so'zlar daraxtga joylashtirilganda, umumiy prefiks **ildizdan boshlab faqat bitta bolasi bor va so'z tugamagan** tugunlar yo'lidir:

1. Ildizdan harakatni boshlaymiz.
2. Agar joriy tugunning `len(children) == 1` bo'lsa va u yerda biror so'z tugamagan bo'lsa (`not is_end`), o'sha yagona bolaga o'tamiz va harfni yig'amiz.
3. Agar bolalar soni 1 dan ko'p bo'lsa (shoxlanish yuz bersa) yoki so'z tugasa, qidiruv to'xtaydi.

## Qachon ishlatiladi

- **Avtoto'ldirish (Autocomplete):** Foydalanuvchi biror prefiks kiritganda, unga mos barcha so'zlarni bir zumda topish (qidiruv tizimlari, IDE lar).
- **Lug'at va imloni tekshirish (Spell Check):** So'zning lug'atda bor-yo'qligini juda tez $O(L)$ vaqtda tekshirish.
- **Eng uzun umumiy prefiks (Longest Common Prefix):** Bir guruh matnlarning boshlang'ich bir xil qismini topish.
- **IP routing:** Tarmoq protokollarida eng uzun prefiks mosligi (Longest Prefix Match) orqali paketlarni yo'naltirish.
