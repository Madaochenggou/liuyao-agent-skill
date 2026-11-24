# 事前记录与复盘

以下为记录模板，不含真实用户资料。

```json
{
  "record_id": "synthetic-001-v1",
  "version": 1,
  "created_at": "填写含时区的事前时间",
  "input_status": "complete_or_partial",
  "question": "单一目标事件",
  "success_event": "可外部核验的成功标准",
  "deadline": "填写含时区的观察截止时间",
  "main_judgment": "倾向成／倾向不成／暂不能判断",
  "confidence": "低／中／高／不适用",
  "decisive_rules": ["R02"],
  "strongest_counterevidence": "最强反证",
  "timing": {"window": null, "condition": "无成立依据时不推成功应期"},
  "failure_condition": "事先写明什么结果会推翻主断",
  "outcome": null,
  "evaluation": "pending"
}
```

记录时间必须来自实际记录，不填假日期伪装事前预测。真实时间、单位和个人资料留在私人记录；公开时另建相对日期副本，不公开原始映射。

有反馈时另存 outcome 记录：原 record_id、实际事件、观测时间、证据类型、判定（命中／未命中／未知／弃权）、误差原因。日期偏差与成败偏差分开评价。倾向成而到期未出现成功事件，判未命中；倾向不成却出现成功事件，同样判未命中。资料不完整或弃权不计入命中分母，必须另外报告数量，防止只展示成功案例。

修正使用 v2 并说明新增事实、纠正的技术错误及修正时间。v2 不覆盖 v1，也不能在知道结果后记作新的事前预测。
