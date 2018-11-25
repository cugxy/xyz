# 28 题 strStr 实现
## KPM算法思路

### 最长公共前后缀长度表

- 前缀 : 如字符串 `ABCDE` 则其前缀有 ：`A` `AB` `ABC` `ABCD` .
- 后缀 : 如字符串 `ABCDE` 则其后缀有 ：`E` `DE` `CDE` `BCDE` .
- 最长公共前后缀长度 : 如对于字符串 `ABADEABA` ，则其前缀有 `A` `AB` `ABA` `ABAD` `ABADE` `ABADEA` `ABADEAB`，其后缀有 `A` `BA` `ABA` `EABA` `DEABA` `ADEABA` `BADEABA`，前缀与后缀有相同字符串 `A` `ABA`，则最长公共前后缀为 `ABA` ，长度为 3 .
- 最长公共前后缀长度表 : 如字符串 `ABCDABD`，则其前缀有 `A` `AB` `ABC` `ABCD` `ABCDA` `ABCDAB`，加上其自身组成长度为 7 的字符串数组。对于数组中的每个字符串，求其最长公共前后缀长度，并添加到结果数组中，最终的到结果为：`0, 0, 0, 0, 1, 2, 0`

### 遍历
- 移动位数 = 已匹配字符串数 - 对应的最长公共前后缀长度