# graduate-map
Create and show a graduation destination map.

# 细节备忘

## 输入信息格式

使用一个JSON来存储信息，格式如下：
```json
{
  "list": [
    [
      "张三",
      "北京",
      "北京大学"
    ],
    [
      "李四",
      "北京",
      "清华大学"
    ]
  ],
  "location": {
    "北京": [
      39.910924,
      116.413387
    ],
    "北京大学": [
      39.998877,
      116.316833
    ],
    "清华大学": [
      40.009645,
      116.333374
    ]
  }
}
```

## `map-university`组件`data`格式
```json
{
  name: "北京理工大学",
  location: {
	lng: 116.322726,
	lat: 39.966659
  },
  list: ["flw", "fdd"]
}
```