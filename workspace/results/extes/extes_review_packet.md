# ExtES 分层抽样评审包

## 人工评审标准（每条快速勾选 / 备注）

对下方每一条样本，建议回答四个问题（可用 ✅ / ⚠️ / ❌ 或 1–5 分）：

1. **对话真实性**：读来是否像真实来访者（vs 模板腔、翻译腔、人设断裂）。
2. **粗标签可信度**：`binary_label`（阻抗/合作）与当前 `response` 及上文是否一致。
3. **上下文可用性**：给定 `context`，是否足以支撑后续 profile 或「需要内心过程」类建模（信息过少则 profile/COT 成本高）。
4. **任务域匹配**：是否与您关心的中文 RECAP / 临床来访者模拟设定足够接近（主观即可）。

**汇总**：若 2）大量不可信 → 优先重做粗标或清洗；若 3）大量不可用 → 暂缓 profile/COT 管线；若 4）长期偏离 → 考虑仅作英文侧扩量或单独 loss。


---

## Part A — binary.json 分层样本

分层：`binary_label` × (`metadata.scene` ∈ Top scenes 或 `__other__`)。

| # | stratum | sample_id | binary_label | scene | len(resp) | len(ctx) |
|---|---------|-----------|--------------|-------|-----------|----------|
| 1 | 合作 \| Academic Stress | `extes_10748_8` | 合作 | Academic Stress | 81 | 766 |
| 2 | 合作 \| Academic Stress | `extes_2400_4` | 合作 | Academic Stress | 124 | 929 |
| 3 | 合作 \| Academic Stress | `extes_10728_6` | 合作 | Academic Stress | 122 | 906 |
| 4 | 合作 \| Academic Stress | `extes_11061_5` | 合作 | Academic Stress | 127 | 1099 |
| 5 | 合作 \| Academic Stress | `extes_10715_5` | 合作 | Academic Stress | 141 | 1079 |
| 6 | 合作 \| Academic Stress | `extes_1874_7` | 合作 | Academic Stress | 111 | 1233 |
| 7 | 合作 \| Academic Stress | `extes_1861_5` | 合作 | Academic Stress | 191 | 1206 |
| 8 | 合作 \| Academic Stress | `extes_9066_1` | 合作 | Academic Stress | 225 | 128 |
| 9 | 合作 \| Academic Stress | `extes_2136_3` | 合作 | Academic Stress | 136 | 1253 |
| 10 | 合作 \| Academic Stress | `extes_10716_10` | 合作 | Academic Stress | 45 | 1093 |
| 11 | 合作 \| Anxiety and Panic | `extes_2220_4` | 合作 | Anxiety and Panic | 146 | 1105 |
| 12 | 合作 \| Anxiety and Panic | `extes_2221_7` | 合作 | Anxiety and Panic | 117 | 1341 |
| 13 | 合作 \| Anxiety and Panic | `extes_2498_8` | 合作 | Anxiety and Panic | 120 | 1154 |
| 14 | 合作 \| Anxiety and Panic | `extes_55_4` | 合作 | Anxiety and Panic | 50 | 847 |
| 15 | 合作 \| Anxiety and Panic | `extes_2212_4` | 合作 | Anxiety and Panic | 59 | 1101 |
| 16 | 合作 \| Anxiety and Panic | `extes_212_1` | 合作 | Anxiety and Panic | 141 | 51 |
| 17 | 合作 \| Anxiety and Panic | `extes_2222_5` | 合作 | Anxiety and Panic | 160 | 1088 |
| 18 | 合作 \| Anxiety and Panic | `extes_55_7` | 合作 | Anxiety and Panic | 43 | 794 |
| 19 | 合作 \| Anxiety and Panic | `extes_2505_3` | 合作 | Anxiety and Panic | 49 | 810 |
| 20 | 合作 \| Anxiety and Panic | `extes_9080_2` | 合作 | Anxiety and Panic | 160 | 304 |
| 21 | 合作 \| Breakups or Divorce | `extes_2223_15` | 合作 | Breakups or Divorce | 19 | 485 |
| 22 | 合作 \| Breakups or Divorce | `extes_4559_1` | 合作 | Breakups or Divorce | 172 | 290 |
| 23 | 合作 \| Breakups or Divorce | `extes_1686_6` | 合作 | Breakups or Divorce | 53 | 1037 |
| 24 | 合作 \| Breakups or Divorce | `extes_4502_7` | 合作 | Breakups or Divorce | 79 | 1889 |
| 25 | 合作 \| Breakups or Divorce | `extes_10843_8` | 合作 | Breakups or Divorce | 67 | 1059 |
| 26 | 合作 \| Breakups or Divorce | `extes_4257_7` | 合作 | Breakups or Divorce | 100 | 931 |
| 27 | 合作 \| Breakups or Divorce | `extes_892_5` | 合作 | Breakups or Divorce | 97 | 1737 |
| 28 | 合作 \| Breakups or Divorce | `extes_10144_5` | 合作 | Breakups or Divorce | 113 | 1321 |
| 29 | 合作 \| Breakups or Divorce | `extes_4536_2` | 合作 | Breakups or Divorce | 89 | 326 |
| 30 | 合作 \| Breakups or Divorce | `extes_10827_3` | 合作 | Breakups or Divorce | 115 | 931 |
| 31 | 合作 \| Communication Challenges | `extes_6370_8` | 合作 | Communication Challenges | 136 | 878 |
| 32 | 合作 \| Communication Challenges | `extes_7386_6` | 合作 | Communication Challenges | 112 | 865 |
| 33 | 合作 \| Communication Challenges | `extes_2650_4` | 合作 | Communication Challenges | 81 | 997 |
| 34 | 合作 \| Communication Challenges | `extes_3563_7` | 合作 | Communication Challenges | 72 | 1027 |
| 35 | 合作 \| Communication Challenges | `extes_4306_6` | 合作 | Communication Challenges | 173 | 1654 |
| 36 | 合作 \| Communication Challenges | `extes_2648_7` | 合作 | Communication Challenges | 114 | 1263 |
| 37 | 合作 \| Communication Challenges | `extes_7484_2` | 合作 | Communication Challenges | 274 | 679 |
| 38 | 合作 \| Communication Challenges | `extes_3708_9` | 合作 | Communication Challenges | 73 | 721 |
| 39 | 合作 \| Communication Challenges | `extes_2723_4` | 合作 | Communication Challenges | 156 | 1460 |
| 40 | 合作 \| Communication Challenges | `extes_5387_9` | 合作 | Communication Challenges | 48 | 1186 |
| 41 | 合作 \| Conflicts or Communication Problems | `extes_1540_2` | 合作 | Conflicts or Communication Problems | 227 | 599 |
| 42 | 合作 \| Conflicts or Communication Problems | `extes_9632_3` | 合作 | Conflicts or Communication Problems | 167 | 841 |
| 43 | 合作 \| Conflicts or Communication Problems | `extes_9797_1` | 合作 | Conflicts or Communication Problems | 102 | 137 |
| 44 | 合作 \| Conflicts or Communication Problems | `extes_9427_3` | 合作 | Conflicts or Communication Problems | 214 | 1020 |
| 45 | 合作 \| Conflicts or Communication Problems | `extes_3987_6` | 合作 | Conflicts or Communication Problems | 104 | 1122 |
| 46 | 合作 \| Conflicts or Communication Problems | `extes_867_8` | 合作 | Conflicts or Communication Problems | 101 | 1301 |
| 47 | 合作 \| Conflicts or Communication Problems | `extes_6746_11` | 合作 | Conflicts or Communication Problems | 74 | 1163 |
| 48 | 合作 \| Conflicts or Communication Problems | `extes_8368_6` | 合作 | Conflicts or Communication Problems | 87 | 1382 |
| 49 | 合作 \| Conflicts or Communication Problems | `extes_9529_2` | 合作 | Conflicts or Communication Problems | 189 | 488 |
| 50 | 合作 \| Conflicts or Communication Problems | `extes_5975_2` | 合作 | Conflicts or Communication Problems | 137 | 432 |
| 51 | 合作 \| Coping with the illness or death of a loved one | `extes_10871_5` | 合作 | Coping with the illness or death of a loved one | 211 | 1277 |
| 52 | 合作 \| Coping with the illness or death of a loved one | `extes_4815_9` | 合作 | Coping with the illness or death of a loved one | 116 | 1245 |
| 53 | 合作 \| Coping with the illness or death of a loved one | `extes_10363_7` | 合作 | Coping with the illness or death of a loved one | 24 | 1338 |
| 54 | 合作 \| Coping with the illness or death of a loved one | `extes_10202_6` | 合作 | Coping with the illness or death of a loved one | 130 | 1520 |
| 55 | 合作 \| Coping with the illness or death of a loved one | `extes_10044_2` | 合作 | Coping with the illness or death of a loved one | 68 | 435 |
| 56 | 合作 \| Coping with the illness or death of a loved one | `extes_2237_6` | 合作 | Coping with the illness or death of a loved one | 124 | 1038 |
| 57 | 合作 \| Coping with the illness or death of a loved one | `extes_329_5` | 合作 | Coping with the illness or death of a loved one | 197 | 1528 |
| 58 | 合作 \| Coping with the illness or death of a loved one | `extes_10031_3` | 合作 | Coping with the illness or death of a loved one | 119 | 681 |
| 59 | 合作 \| Coping with the illness or death of a loved one | `extes_1315_7` | 合作 | Coping with the illness or death of a loved one | 61 | 1036 |
| 60 | 合作 \| Coping with the illness or death of a loved one | `extes_10529_2` | 合作 | Coping with the illness or death of a loved one | 168 | 348 |
| 61 | 合作 \| Dealing with the Loss of a Pet | `extes_10390_4` | 合作 | Dealing with the Loss of a Pet | 233 | 1570 |
| 62 | 合作 \| Dealing with the Loss of a Pet | `extes_1992_4` | 合作 | Dealing with the Loss of a Pet | 55 | 681 |
| 63 | 合作 \| Dealing with the Loss of a Pet | `extes_10597_10` | 合作 | Dealing with the Loss of a Pet | 56 | 860 |
| 64 | 合作 \| Dealing with the Loss of a Pet | `extes_1114_1` | 合作 | Dealing with the Loss of a Pet | 320 | 586 |
| 65 | 合作 \| Dealing with the Loss of a Pet | `extes_5096_0` | 合作 | Dealing with the Loss of a Pet | 114 | 33 |
| 66 | 合作 \| Dealing with the Loss of a Pet | `extes_1052_9` | 合作 | Dealing with the Loss of a Pet | 61 | 1062 |
| 67 | 合作 \| Dealing with the Loss of a Pet | `extes_1405_2` | 合作 | Dealing with the Loss of a Pet | 149 | 618 |
| 68 | 合作 \| Dealing with the Loss of a Pet | `extes_9913_1` | 合作 | Dealing with the Loss of a Pet | 223 | 456 |
| 69 | 合作 \| Dealing with the Loss of a Pet | `extes_2017_8` | 合作 | Dealing with the Loss of a Pet | 137 | 1140 |
| 70 | 合作 \| Dealing with the Loss of a Pet | `extes_1417_8` | 合作 | Dealing with the Loss of a Pet | 128 | 1432 |
| 71 | 合作 \| Depression and Low Mood | `extes_2526_5` | 合作 | Depression and Low Mood | 195 | 1966 |
| 72 | 合作 \| Depression and Low Mood | `extes_11102_2` | 合作 | Depression and Low Mood | 207 | 359 |
| 73 | 合作 \| Depression and Low Mood | `extes_2419_7` | 合作 | Depression and Low Mood | 72 | 1238 |
| 74 | 合作 \| Depression and Low Mood | `extes_196_7` | 合作 | Depression and Low Mood | 81 | 1631 |
| 75 | 合作 \| Depression and Low Mood | `extes_11099_5` | 合作 | Depression and Low Mood | 136 | 1472 |
| 76 | 合作 \| Depression and Low Mood | `extes_2510_2` | 合作 | Depression and Low Mood | 164 | 382 |
| 77 | 合作 \| Depression and Low Mood | `extes_2523_8` | 合作 | Depression and Low Mood | 124 | 1485 |
| 78 | 合作 \| Depression and Low Mood | `extes_2159_3` | 合作 | Depression and Low Mood | 122 | 670 |
| 79 | 合作 \| Depression and Low Mood | `extes_1894_4` | 合作 | Depression and Low Mood | 208 | 1185 |
| 80 | 合作 \| Depression and Low Mood | `extes_197_5` | 合作 | Depression and Low Mood | 195 | 1009 |
| 81 | 合作 \| Financial Worries and Uncertainty | `extes_10655_1` | 合作 | Financial Worries and Uncertainty | 151 | 88 |
| 82 | 合作 \| Financial Worries and Uncertainty | `extes_2067_1` | 合作 | Financial Worries and Uncertainty | 166 | 81 |
| 83 | 合作 \| Financial Worries and Uncertainty | `extes_11005_4` | 合作 | Financial Worries and Uncertainty | 174 | 1523 |
| 84 | 合作 \| Financial Worries and Uncertainty | `extes_674_6` | 合作 | Financial Worries and Uncertainty | 186 | 1464 |
| 85 | 合作 \| Financial Worries and Uncertainty | `extes_9061_2` | 合作 | Financial Worries and Uncertainty | 88 | 494 |
| 86 | 合作 \| Financial Worries and Uncertainty | `extes_4895_2` | 合作 | Financial Worries and Uncertainty | 109 | 267 |
| 87 | 合作 \| Financial Worries and Uncertainty | `extes_10667_4` | 合作 | Financial Worries and Uncertainty | 176 | 1246 |
| 88 | 合作 \| Financial Worries and Uncertainty | `extes_10989_5` | 合作 | Financial Worries and Uncertainty | 135 | 1284 |
| 89 | 合作 \| Financial Worries and Uncertainty | `extes_10998_2` | 合作 | Financial Worries and Uncertainty | 109 | 383 |
| 90 | 合作 \| Financial Worries and Uncertainty | `extes_11015_1` | 合作 | Financial Worries and Uncertainty | 115 | 49 |
| 91 | 合作 \| Managing Bipolar Disorder | `extes_204_8` | 合作 | Managing Bipolar Disorder | 81 | 690 |
| 92 | 合作 \| Managing Bipolar Disorder | `extes_382_13` | 合作 | Managing Bipolar Disorder | 44 | 564 |
| 93 | 合作 \| Managing Bipolar Disorder | `extes_703_4` | 合作 | Managing Bipolar Disorder | 90 | 760 |
| 94 | 合作 \| Managing Bipolar Disorder | `extes_2457_5` | 合作 | Managing Bipolar Disorder | 113 | 1360 |
| 95 | 合作 \| Managing Bipolar Disorder | `extes_2454_5` | 合作 | Managing Bipolar Disorder | 173 | 1142 |
| 96 | 合作 \| Managing Bipolar Disorder | `extes_2467_8` | 合作 | Managing Bipolar Disorder | 102 | 1106 |
| 97 | 合作 \| Managing Bipolar Disorder | `extes_54_1` | 合作 | Managing Bipolar Disorder | 187 | 414 |
| 98 | 合作 \| Managing Bipolar Disorder | `extes_9075_2` | 合作 | Managing Bipolar Disorder | 116 | 635 |
| 99 | 合作 \| Managing Bipolar Disorder | `extes_2204_3` | 合作 | Managing Bipolar Disorder | 177 | 1189 |
| 100 | 合作 \| Managing Bipolar Disorder | `extes_2458_2` | 合作 | Managing Bipolar Disorder | 96 | 698 |
| 101 | 合作 \| Unemployment-related stress | `extes_10692_4` | 合作 | Unemployment-related stress | 151 | 1303 |
| 102 | 合作 \| Unemployment-related stress | `extes_185_3` | 合作 | Unemployment-related stress | 90 | 645 |
| 103 | 合作 \| Unemployment-related stress | `extes_2379_6` | 合作 | Unemployment-related stress | 151 | 1388 |
| 104 | 合作 \| Unemployment-related stress | `extes_185_8` | 合作 | Unemployment-related stress | 110 | 952 |
| 105 | 合作 \| Unemployment-related stress | `extes_2379_1` | 合作 | Unemployment-related stress | 178 | 119 |
| 106 | 合作 \| Unemployment-related stress | `extes_2354_2` | 合作 | Unemployment-related stress | 166 | 362 |
| 107 | 合作 \| Unemployment-related stress | `extes_10709_6` | 合作 | Unemployment-related stress | 109 | 1143 |
| 108 | 合作 \| Unemployment-related stress | `extes_10673_9` | 合作 | Unemployment-related stress | 82 | 1278 |
| 109 | 合作 \| Unemployment-related stress | `extes_37_11` | 合作 | Unemployment-related stress | 45 | 796 |
| 110 | 合作 \| Unemployment-related stress | `extes_10675_6` | 合作 | Unemployment-related stress | 119 | 1459 |
| 111 | 合作 \| Work-related Stress and Burnout | `extes_10616_5` | 合作 | Work-related Stress and Burnout | 133 | 1171 |
| 112 | 合作 \| Work-related Stress and Burnout | `extes_343_13` | 合作 | Work-related Stress and Burnout | 112 | 655 |
| 113 | 合作 \| Work-related Stress and Burnout | `extes_10454_10` | 合作 | Work-related Stress and Burnout | 36 | 1015 |
| 114 | 合作 \| Work-related Stress and Burnout | `extes_10944_2` | 合作 | Work-related Stress and Burnout | 189 | 397 |
| 115 | 合作 \| Work-related Stress and Burnout | `extes_2041_11` | 合作 | Work-related Stress and Burnout | 85 | 896 |
| 116 | 合作 \| Work-related Stress and Burnout | `extes_1777_5` | 合作 | Work-related Stress and Burnout | 103 | 1093 |
| 117 | 合作 \| Work-related Stress and Burnout | `extes_10947_9` | 合作 | Work-related Stress and Burnout | 68 | 828 |
| 118 | 合作 \| Work-related Stress and Burnout | `extes_2059_9` | 合作 | Work-related Stress and Burnout | 33 | 1001 |
| 119 | 合作 \| Work-related Stress and Burnout | `extes_10618_11` | 合作 | Work-related Stress and Burnout | 30 | 765 |
| 120 | 合作 \| Work-related Stress and Burnout | `extes_10608_2` | 合作 | Work-related Stress and Burnout | 238 | 280 |
| 121 | 合作 \| __other__ | `extes_2592_1` | 合作 | Moving to a New City or Country | 149 | 50 |
| 122 | 合作 \| __other__ | `extes_286_2` | 合作 | Surviving and Recovering from Physical or Emotional Abuse | 190 | 686 |
| 123 | 合作 \| __other__ | `extes_271_5` | 合作 | Academic Stress or Pressure | 78 | 741 |
| 124 | 合作 \| __other__ | `extes_4854_3` | 合作 | Job Promotion Stress | 153 | 396 |
| 125 | 合作 \| __other__ | `extes_110_10` | 合作 | Job Loss or Career Setbacks | 74 | 981 |
| 126 | 合作 \| __other__ | `extes_506_6` | 合作 | Parenting Challenges and Parental Guilt | 125 | 1203 |
| 127 | 合作 \| __other__ | `extes_421_8` | 合作 | Moving to a New City or Country | 72 | 1049 |
| 128 | 合作 \| __other__ | `extes_2578_7` | 合作 | Moving to a New City or Country | 117 | 1413 |
| 129 | 合作 \| __other__ | `extes_141_5` | 合作 | Addiction and Recovery | 86 | 941 |
| 130 | 合作 \| __other__ | `extes_598_5` | 合作 | Addiction and Recovery | 126 | 1005 |
| 131 | 阻抗 \| Academic Stress | `extes_10721_5` | 阻抗 | Academic Stress | 134 | 1023 |
| 132 | 阻抗 \| Academic Stress | `extes_2127_4` | 阻抗 | Academic Stress | 154 | 1118 |
| 133 | 阻抗 \| Academic Stress | `extes_2150_2` | 阻抗 | Academic Stress | 143 | 513 |
| 134 | 阻抗 \| Academic Stress | `extes_370_3` | 阻抗 | Academic Stress | 111 | 813 |
| 135 | 阻抗 \| Academic Stress | `extes_2393_3` | 阻抗 | Academic Stress | 122 | 891 |
| 136 | 阻抗 \| Academic Stress | `extes_11059_3` | 阻抗 | Academic Stress | 193 | 922 |
| 137 | 阻抗 \| Academic Stress | `extes_189_3` | 阻抗 | Academic Stress | 135 | 802 |
| 138 | 阻抗 \| Academic Stress | `extes_2385_4` | 阻抗 | Academic Stress | 142 | 1241 |
| 139 | 阻抗 \| Academic Stress | `extes_1865_3` | 阻抗 | Academic Stress | 186 | 1323 |
| 140 | 阻抗 \| Academic Stress | `extes_187_4` | 阻抗 | Academic Stress | 156 | 1131 |
| 141 | 阻抗 \| Anxiety and Panic | `extes_9080_4` | 阻抗 | Anxiety and Panic | 112 | 1035 |
| 142 | 阻抗 \| Anxiety and Panic | `extes_2211_3` | 阻抗 | Anxiety and Panic | 122 | 881 |
| 143 | 阻抗 \| Anxiety and Panic | `extes_2209_4` | 阻抗 | Anxiety and Panic | 133 | 1477 |
| 144 | 阻抗 \| Anxiety and Panic | `extes_2480_3` | 阻抗 | Anxiety and Panic | 125 | 919 |
| 145 | 阻抗 \| Anxiety and Panic | `extes_716_4` | 阻抗 | Anxiety and Panic | 87 | 929 |
| 146 | 阻抗 \| Anxiety and Panic | `extes_55_5` | 阻抗 | Anxiety and Panic | 95 | 780 |
| 147 | 阻抗 \| Anxiety and Panic | `extes_2494_4` | 阻抗 | Anxiety and Panic | 111 | 1025 |
| 148 | 阻抗 \| Anxiety and Panic | `extes_2491_6` | 阻抗 | Anxiety and Panic | 98 | 1138 |
| 149 | 阻抗 \| Anxiety and Panic | `extes_2496_2` | 阻抗 | Anxiety and Panic | 105 | 263 |
| 150 | 阻抗 \| Anxiety and Panic | `extes_2221_4` | 阻抗 | Anxiety and Panic | 167 | 1235 |
| 151 | 阻抗 \| Breakups or Divorce | `extes_1570_6` | 阻抗 | Breakups or Divorce | 99 | 1099 |
| 152 | 阻抗 \| Breakups or Divorce | `extes_9639_5` | 阻抗 | Breakups or Divorce | 97 | 1091 |
| 153 | 阻抗 \| Breakups or Divorce | `extes_11176_5` | 阻抗 | Breakups or Divorce | 67 | 842 |
| 154 | 阻抗 \| Breakups or Divorce | `extes_10509_6` | 阻抗 | Breakups or Divorce | 73 | 1036 |
| 155 | 阻抗 \| Breakups or Divorce | `extes_884_8` | 阻抗 | Breakups or Divorce | 90 | 1203 |
| 156 | 阻抗 \| Breakups or Divorce | `extes_10002_4` | 阻抗 | Breakups or Divorce | 111 | 940 |
| 157 | 阻抗 \| Breakups or Divorce | `extes_1259_4` | 阻抗 | Breakups or Divorce | 79 | 857 |
| 158 | 阻抗 \| Breakups or Divorce | `extes_9672_6` | 阻抗 | Breakups or Divorce | 74 | 1052 |
| 159 | 阻抗 \| Breakups or Divorce | `extes_896_3` | 阻抗 | Breakups or Divorce | 85 | 655 |
| 160 | 阻抗 \| Breakups or Divorce | `extes_10328_5` | 阻抗 | Breakups or Divorce | 106 | 950 |
| 161 | 阻抗 \| Communication Challenges | `extes_5840_3` | 阻抗 | Communication Challenges | 184 | 1219 |
| 162 | 阻抗 \| Communication Challenges | `extes_6800_3` | 阻抗 | Communication Challenges | 103 | 979 |
| 163 | 阻抗 \| Communication Challenges | `extes_2812_6` | 阻抗 | Communication Challenges | 71 | 846 |
| 164 | 阻抗 \| Communication Challenges | `extes_8272_3` | 阻抗 | Communication Challenges | 158 | 1277 |
| 165 | 阻抗 \| Communication Challenges | `extes_6949_3` | 阻抗 | Communication Challenges | 101 | 905 |
| 166 | 阻抗 \| Communication Challenges | `extes_3506_3` | 阻抗 | Communication Challenges | 132 | 955 |
| 167 | 阻抗 \| Communication Challenges | `extes_6055_2` | 阻抗 | Communication Challenges | 156 | 465 |
| 168 | 阻抗 \| Communication Challenges | `extes_7195_3` | 阻抗 | Communication Challenges | 143 | 1236 |
| 169 | 阻抗 \| Communication Challenges | `extes_9252_3` | 阻抗 | Communication Challenges | 102 | 858 |
| 170 | 阻抗 \| Communication Challenges | `extes_3663_3` | 阻抗 | Communication Challenges | 229 | 1147 |
| 171 | 阻抗 \| Conflicts or Communication Problems | `extes_6697_4` | 阻抗 | Conflicts or Communication Problems | 100 | 1363 |
| 172 | 阻抗 \| Conflicts or Communication Problems | `extes_4422_3` | 阻抗 | Conflicts or Communication Problems | 87 | 805 |
| 173 | 阻抗 \| Conflicts or Communication Problems | `extes_6835_3` | 阻抗 | Conflicts or Communication Problems | 90 | 851 |
| 174 | 阻抗 \| Conflicts or Communication Problems | `extes_8424_3` | 阻抗 | Conflicts or Communication Problems | 189 | 1225 |
| 175 | 阻抗 \| Conflicts or Communication Problems | `extes_6560_3` | 阻抗 | Conflicts or Communication Problems | 115 | 667 |
| 176 | 阻抗 \| Conflicts or Communication Problems | `extes_9633_4` | 阻抗 | Conflicts or Communication Problems | 137 | 1108 |
| 177 | 阻抗 \| Conflicts or Communication Problems | `extes_6197_5` | 阻抗 | Conflicts or Communication Problems | 186 | 1392 |
| 178 | 阻抗 \| Conflicts or Communication Problems | `extes_3134_4` | 阻抗 | Conflicts or Communication Problems | 107 | 1140 |
| 179 | 阻抗 \| Conflicts or Communication Problems | `extes_1664_4` | 阻抗 | Conflicts or Communication Problems | 165 | 1281 |
| 180 | 阻抗 \| Conflicts or Communication Problems | `extes_5864_4` | 阻抗 | Conflicts or Communication Problems | 151 | 1506 |
| 181 | 阻抗 \| Coping with the illness or death of a loved one | `extes_2238_6` | 阻抗 | Coping with the illness or death of a loved one | 93 | 1155 |
| 182 | 阻抗 \| Coping with the illness or death of a loved one | `extes_1337_4` | 阻抗 | Coping with the illness or death of a loved one | 97 | 1127 |
| 183 | 阻抗 \| Coping with the illness or death of a loved one | `extes_1374_4` | 阻抗 | Coping with the illness or death of a loved one | 83 | 1129 |
| 184 | 阻抗 \| Coping with the illness or death of a loved one | `extes_9884_2` | 阻抗 | Coping with the illness or death of a loved one | 123 | 569 |
| 185 | 阻抗 \| Coping with the illness or death of a loved one | `extes_1041_5` | 阻抗 | Coping with the illness or death of a loved one | 119 | 1232 |
| 186 | 阻抗 \| Coping with the illness or death of a loved one | `extes_2235_6` | 阻抗 | Coping with the illness or death of a loved one | 83 | 835 |
| 187 | 阻抗 \| Coping with the illness or death of a loved one | `extes_1322_3` | 阻抗 | Coping with the illness or death of a loved one | 125 | 783 |
| 188 | 阻抗 \| Coping with the illness or death of a loved one | `extes_4976_5` | 阻抗 | Coping with the illness or death of a loved one | 71 | 1175 |
| 189 | 阻抗 \| Coping with the illness or death of a loved one | `extes_10379_5` | 阻抗 | Coping with the illness or death of a loved one | 89 | 1057 |
| 190 | 阻抗 \| Coping with the illness or death of a loved one | `extes_2231_5` | 阻抗 | Coping with the illness or death of a loved one | 90 | 916 |
| 191 | 阻抗 \| Dealing with the Loss of a Pet | `extes_2022_5` | 阻抗 | Dealing with the Loss of a Pet | 81 | 706 |
| 192 | 阻抗 \| Dealing with the Loss of a Pet | `extes_10936_3` | 阻抗 | Dealing with the Loss of a Pet | 67 | 1005 |
| 193 | 阻抗 \| Dealing with the Loss of a Pet | `extes_1406_5` | 阻抗 | Dealing with the Loss of a Pet | 171 | 1337 |
| 194 | 阻抗 \| Dealing with the Loss of a Pet | `extes_20_4` | 阻抗 | Dealing with the Loss of a Pet | 66 | 723 |
| 195 | 阻抗 \| Dealing with the Loss of a Pet | `extes_2262_4` | 阻抗 | Dealing with the Loss of a Pet | 63 | 1040 |
| 196 | 阻抗 \| Dealing with the Loss of a Pet | `extes_169_6` | 阻抗 | Dealing with the Loss of a Pet | 64 | 1077 |
| 197 | 阻抗 \| Dealing with the Loss of a Pet | `extes_10215_5` | 阻抗 | Dealing with the Loss of a Pet | 97 | 1369 |
| 198 | 阻抗 \| Dealing with the Loss of a Pet | `extes_10589_6` | 阻抗 | Dealing with the Loss of a Pet | 65 | 825 |
| 199 | 阻抗 \| Dealing with the Loss of a Pet | `extes_1384_2` | 阻抗 | Dealing with the Loss of a Pet | 103 | 632 |
| 200 | 阻抗 \| Dealing with the Loss of a Pet | `extes_1416_3` | 阻抗 | Dealing with the Loss of a Pet | 103 | 948 |
| 201 | 阻抗 \| Depression and Low Mood | `extes_2519_8` | 阻抗 | Depression and Low Mood | 73 | 961 |
| 202 | 阻抗 \| Depression and Low Mood | `extes_10758_4` | 阻抗 | Depression and Low Mood | 160 | 1384 |
| 203 | 阻抗 \| Depression and Low Mood | `extes_9085_4` | 阻抗 | Depression and Low Mood | 185 | 996 |
| 204 | 阻抗 \| Depression and Low Mood | `extes_213_8` | 阻抗 | Depression and Low Mood | 142 | 1271 |
| 205 | 阻抗 \| Depression and Low Mood | `extes_64_5` | 阻抗 | Depression and Low Mood | 63 | 992 |
| 206 | 阻抗 \| Depression and Low Mood | `extes_200_6` | 阻抗 | Depression and Low Mood | 121 | 1187 |
| 207 | 阻抗 \| Depression and Low Mood | `extes_214_3` | 阻抗 | Depression and Low Mood | 73 | 640 |
| 208 | 阻抗 \| Depression and Low Mood | `extes_218_5` | 阻抗 | Depression and Low Mood | 106 | 1516 |
| 209 | 阻抗 \| Depression and Low Mood | `extes_2431_3` | 阻抗 | Depression and Low Mood | 150 | 1007 |
| 210 | 阻抗 \| Depression and Low Mood | `extes_2533_3` | 阻抗 | Depression and Low Mood | 75 | 759 |
| 211 | 阻抗 \| Financial Worries and Uncertainty | `extes_10985_4` | 阻抗 | Financial Worries and Uncertainty | 191 | 1397 |
| 212 | 阻抗 \| Financial Worries and Uncertainty | `extes_11003_2` | 阻抗 | Financial Worries and Uncertainty | 139 | 888 |
| 213 | 阻抗 \| Financial Worries and Uncertainty | `extes_10670_4` | 阻抗 | Financial Worries and Uncertainty | 147 | 1436 |
| 214 | 阻抗 \| Financial Worries and Uncertainty | `extes_2349_2` | 阻抗 | Financial Worries and Uncertainty | 92 | 962 |
| 215 | 阻抗 \| Financial Worries and Uncertainty | `extes_1820_3` | 阻抗 | Financial Worries and Uncertainty | 128 | 874 |
| 216 | 阻抗 \| Financial Worries and Uncertainty | `extes_1815_2` | 阻抗 | Financial Worries and Uncertainty | 165 | 1058 |
| 217 | 阻抗 \| Financial Worries and Uncertainty | `extes_351_3` | 阻抗 | Financial Worries and Uncertainty | 166 | 889 |
| 218 | 阻抗 \| Financial Worries and Uncertainty | `extes_671_5` | 阻抗 | Financial Worries and Uncertainty | 111 | 1093 |
| 219 | 阻抗 \| Financial Worries and Uncertainty | `extes_10993_5` | 阻抗 | Financial Worries and Uncertainty | 145 | 1235 |
| 220 | 阻抗 \| Financial Worries and Uncertainty | `extes_2336_6` | 阻抗 | Financial Worries and Uncertainty | 123 | 1813 |
| 221 | 阻抗 \| Managing Bipolar Disorder | `extes_9076_4` | 阻抗 | Managing Bipolar Disorder | 61 | 788 |
| 222 | 阻抗 \| Managing Bipolar Disorder | `extes_2191_9` | 阻抗 | Managing Bipolar Disorder | 165 | 1023 |
| 223 | 阻抗 \| Managing Bipolar Disorder | `extes_2479_7` | 阻抗 | Managing Bipolar Disorder | 101 | 929 |
| 224 | 阻抗 \| Managing Bipolar Disorder | `extes_384_3` | 阻抗 | Managing Bipolar Disorder | 74 | 823 |
| 225 | 阻抗 \| Managing Bipolar Disorder | `extes_2179_4` | 阻抗 | Managing Bipolar Disorder | 117 | 1260 |
| 226 | 阻抗 \| Managing Bipolar Disorder | `extes_387_5` | 阻抗 | Managing Bipolar Disorder | 93 | 888 |
| 227 | 阻抗 \| Managing Bipolar Disorder | `extes_2455_4` | 阻抗 | Managing Bipolar Disorder | 120 | 1105 |
| 228 | 阻抗 \| Managing Bipolar Disorder | `extes_2473_6` | 阻抗 | Managing Bipolar Disorder | 199 | 1181 |
| 229 | 阻抗 \| Managing Bipolar Disorder | `extes_2207_3` | 阻抗 | Managing Bipolar Disorder | 132 | 1043 |
| 230 | 阻抗 \| Managing Bipolar Disorder | `extes_2196_2` | 阻抗 | Managing Bipolar Disorder | 49 | 727 |
| 231 | 阻抗 \| Unemployment-related stress | `extes_681_3` | 阻抗 | Unemployment-related stress | 195 | 1019 |
| 232 | 阻抗 \| Unemployment-related stress | `extes_4907_4` | 阻抗 | Unemployment-related stress | 81 | 965 |
| 233 | 阻抗 \| Unemployment-related stress | `extes_2114_4` | 阻抗 | Unemployment-related stress | 151 | 1533 |
| 234 | 阻抗 \| Unemployment-related stress | `extes_4901_5` | 阻抗 | Unemployment-related stress | 100 | 1108 |
| 235 | 阻抗 \| Unemployment-related stress | `extes_4905_3` | 阻抗 | Unemployment-related stress | 146 | 741 |
| 236 | 阻抗 \| Unemployment-related stress | `extes_4912_5` | 阻抗 | Unemployment-related stress | 110 | 1037 |
| 237 | 阻抗 \| Unemployment-related stress | `extes_4902_5` | 阻抗 | Unemployment-related stress | 99 | 1170 |
| 238 | 阻抗 \| Unemployment-related stress | `extes_1832_3` | 阻抗 | Unemployment-related stress | 68 | 888 |
| 239 | 阻抗 \| Unemployment-related stress | `extes_10697_4` | 阻抗 | Unemployment-related stress | 133 | 1165 |
| 240 | 阻抗 \| Unemployment-related stress | `extes_2378_4` | 阻抗 | Unemployment-related stress | 104 | 919 |
| 241 | 阻抗 \| Work-related Stress and Burnout | `extes_10608_3` | 阻抗 | Work-related Stress and Burnout | 101 | 758 |
| 242 | 阻抗 \| Work-related Stress and Burnout | `extes_343_5` | 阻抗 | Work-related Stress and Burnout | 89 | 721 |
| 243 | 阻抗 \| Work-related Stress and Burnout | `extes_663_4` | 阻抗 | Work-related Stress and Burnout | 117 | 948 |
| 244 | 阻抗 \| Work-related Stress and Burnout | `extes_10636_3` | 阻抗 | Work-related Stress and Burnout | 178 | 1198 |
| 245 | 阻抗 \| Work-related Stress and Burnout | `extes_10638_4` | 阻抗 | Work-related Stress and Burnout | 125 | 1275 |
| 246 | 阻抗 \| Work-related Stress and Burnout | `extes_10973_7` | 阻抗 | Work-related Stress and Burnout | 164 | 1361 |
| 247 | 阻抗 \| Work-related Stress and Burnout | `extes_10949_6` | 阻抗 | Work-related Stress and Burnout | 103 | 1081 |
| 248 | 阻抗 \| Work-related Stress and Burnout | `extes_10626_5` | 阻抗 | Work-related Stress and Burnout | 130 | 1095 |
| 249 | 阻抗 \| Work-related Stress and Burnout | `extes_10954_4` | 阻抗 | Work-related Stress and Burnout | 134 | 1045 |
| 250 | 阻抗 \| Work-related Stress and Burnout | `extes_10953_6` | 阻抗 | Work-related Stress and Burnout | 150 | 1165 |
| 251 | 阻抗 \| __other__ | `extes_610_3` | 阻抗 | Support for Loved Ones or Friends | 100 | 772 |
| 252 | 阻抗 \| __other__ | `extes_227_4` | 阻抗 | Adjusting to a New Job or Role | 49 | 746 |
| 253 | 阻抗 \| __other__ | `extes_83_5` | 阻抗 | Parenthood and Parenting Challenges | 92 | 625 |
| 254 | 阻抗 \| __other__ | `extes_100_3` | 阻抗 | Cultural Identity and Belonging | 83 | 604 |
| 255 | 阻抗 \| __other__ | `extes_4886_3` | 阻抗 | Relationship Struggles and Communication Issues | 126 | 974 |
| 256 | 阻抗 \| __other__ | `extes_446_3` | 阻抗 | Low Self-Esteem or Lack of Confidence | 95 | 575 |
| 257 | 阻抗 \| __other__ | `extes_100_4` | 阻抗 | Cultural Identity and Belonging | 77 | 777 |
| 258 | 阻抗 \| __other__ | `extes_9131_4` | 阻抗 | Parenting Challenges and Parental Guilt | 126 | 1267 |
| 259 | 阻抗 \| __other__ | `extes_247_2` | 阻抗 | Parenthood and Parenting Challenges | 133 | 439 |
| 260 | 阻抗 \| __other__ | `extes_89_3` | 阻抗 | Lack of Confidence in Public Speaking | 104 | 843 |

### Part A 全文（逐条）

### A-1. `extes_10748_8` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with multiple projects and upcoming exams
- **binary_label**：合作

**context**

```text
来访者：Thank you, it means a lot when someone understands what I'm going through.
咨询师：Have you considered talking to your professors about your workload? They may be able to provide some guidance or offer extensions for projects.
来访者：I haven't really thought about talking to them. I always try to handle things on my own, but maybe seeking their advice could be helpful.
咨询师：It's understandable to want to handle things independently, but reaching out for support can make a huge difference. You're not alone in this.
来访者：You're right. I should try reaching out to them and explain my situation.
咨询师：That's a great step forward! While you're dealing with all these responsibilities, make sure to take breaks and practice self-care. It's essential to recharge yourself.
```

**response（来访当前句）**

```text
Yes, I tend to forget about self-care. I'll definitely make more time for myself.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-2. `extes_2400_4` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：I'm experiencing academic stress due to a heavy workload and upcoming exams.
- **binary_label**：合作

**context**

```text
来访者：It just feels like there's so much to do and not enough time to do it all. I'm constantly stressed and anxious about not being able to keep up with all the assignments and studying.
咨询师：It sounds like you're facing a lot of pressure and it's causing you significant stress. It's completely normal to feel overwhelmed in such a situation.
来访者：Thank you for understanding. It's just really hard to stay motivated and focused with so much going on.
咨询师：I completely understand. It can be really challenging to stay motivated and focused when you have so many academic obligations. Remember, though, that you're not alone in this and it's okay to ask for support.
来访者：You're right. It does help to know that I'm not alone. Sometimes it's just hard to manage everything on my own.
咨询师：Absolutely! It's important to remember that seeking support is a sign of strength, not weakness. I'm here to listen and support you through this.
```

**response（来访当前句）**

```text
Thank you, that means a lot. Do you have any suggestions on how I can better manage my workload and reduce my stress levels?
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-3. `extes_10728_6` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Having trouble staying motivated during online classes
- **binary_label**：合作

**context**

```text
来访者：Definitely. And I find it especially hard to stay focused when there are so many distractions around me. I end up procrastinating a lot.
咨询师：Procrastination can be a common struggle, especially when there are so many distractions at home. Don't be too hard on yourself, though. It's completely understandable given the circumstances.
来访者：Yeah, I guess you're right. I just wish I could find a way to stay motivated and on track like I used to be.
咨询师：I believe in you, and I know you have the ability to regain that motivation. Maybe you could try creating a study schedule or finding a dedicated workspace to help recreate that sense of structure.
来访者：That's a good idea. I'll give it a try and see if having a routine helps me stay focused.
咨询师：That's great to hear! Establishing a routine can make a big difference. Remember to be patient with yourself as you adapt to this new learning environment.
```

**response（来访当前句）**

```text
Thanks for the encouragement. It means a lot to have someone understand what I'm going through and offer practical advice.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-4. `extes_11061_5` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with a heavy course load and struggling to balance academics and personal life
- **binary_label**：合作

**context**

```text
来访者：It feels like no matter how much I study, it's never enough. And I see my friends having more free time, and it makes me doubt my abilities. I just feel so stressed and burnt out.
咨询师：I can totally understand why you would feel that way. It's tough to compare yourself to others and feel like you're falling behind. Remember, everyone's experiences are different, and it's important to focus on your own journey.
来访者：You're right. I need to stop comparing myself to others. But it's hard when I'm constantly surrounded by people who seem to be doing so well.
咨询师：It can be challenging to see others excel while you may be facing difficulties. But it's important to remember that each person has their own struggles, and what matters most is your own progress and growth.
来访者：I need to find a way to manage my time better. It always feels like I'm running out of time and that adds to my stress.
咨询师：Managing time effectively can really help reduce stress. Have you tried creating a schedule or to-do list to prioritize tasks and allocate specific time slots for studying and personal activities?
```

**response（来访当前句）**

```text
I haven't really tried that before. I usually just try to study whenever I have spare time, but it's not really working for me.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-5. `extes_10715_5` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with studying for exams and struggling to manage time effectively
- **binary_label**：合作

**context**

```text
来访者：Yeah, it feels like I have to sacrifice everything else in my life just to study. I don't have time for my hobbies, friends, or even taking care of myself properly.
咨询师：It's tough when studying takes up so much of your time and it feels like you have to give up other important aspects of your life. It's important to find a balance.
来访者：I've tried making a study schedule, but it's difficult to stick to it. I get distracted easily and end up procrastinating. It's frustrating.
咨询师：Creating a study schedule is a great idea, but it can be challenging to stick to it. Have you considered breaking down your tasks into smaller, more manageable chunks? That way, it's easier to focus and less overwhelming.
来访者：That's a good suggestion. I'll try breaking down my studying into smaller tasks. But I still struggle with staying motivated and avoiding distractions.
咨询师：I can understand how staying motivated and avoiding distractions can be difficult. Remember, it's important to take breaks and reward yourself for small achievements. It can help you stay motivated and focused.
```

**response（来访当前句）**

```text
You're right, taking breaks and rewarding myself could make studying more enjoyable. I just need to figure out ways to manage my time better.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-6. `extes_1874_7` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with upcoming exams and struggling to concentrate
- **binary_label**：合作

**context**

```text
来访者：Yes, exactly. I'm worried that I won't be able to cover all the material in time and I'll end up failing the exams.
咨询师：Those feelings of worry and self-doubt are common when facing a time crunch with exams. It's important to remember that many students have experienced similar concerns, and you're not alone in this.
来访者：I guess so. It's just hard to stay positive when I feel so overwhelmed. Do you have any suggestions for managing this stress?
咨询师：Absolutely! One suggestion is to break down your study material into smaller, manageable chunks. Set specific goals for each study session, and reward yourself after accomplishing them. It can also be helpful to find a quiet and comfortable study space free from distractions. And don't forget to take breaks and engage in activities that help you relax, like going for a walk or practicing deep breathing exercises.
来访者：Thanks for the suggestions. I'll give them a try. It's just good to know that there are strategies I can use to manage my stress.
咨询师：You're welcome! Remember, you have the ability to manage your stress and overcome these challenges. Don't be too hard on yourself, and if you ever need someone to talk to or have further questions, feel free to reach out.
```

**response（来访当前句）**

```text
I really appreciate your support. It means a lot to have someone to talk to about all of this. Thank you again.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-7. `extes_1861_5` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Struggling to balance work and study commitments
- **binary_label**：合作

**context**

```text
来访者：Thank you, I appreciate your understanding. I just wish there was more time in the day to get everything done and still have time for myself and my friends.
咨询师：I hear you. Time management can be a real struggle, especially when your plate is so full. Have you tried creating a schedule or setting aside specific times for studying and relaxation?
来访者：Yes, I've tried that, but it feels like there's always something that comes up or unexpected tasks that take up my time. It's frustrating and leaves me feeling overwhelmed.
咨询师：That must be incredibly frustrating, constantly having your schedule disrupted. It's understandable to feel overwhelmed when unexpected tasks interfere with your plans. It's important to be flexible and prioritize self-care when needed.
来访者：You're right, I need to be more flexible and kind to myself. It's just hard to let go and not feel guilty when I'm not constantly working.
咨询师：I completely understand. It's common to struggle with finding balance and feeling guilty for taking breaks. However, it's important to remember that rest and self-care are integral to maintaining a healthy and productive lifestyle. You deserve to recharge and take care of your well-being.
```

**response（来访当前句）**

```text
Thank you for saying that. I often forget that taking care of myself is just as important as meeting deadlines and completing tasks. It feels like such a relief to hear someone validate that.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-8. `extes_9066_1` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Struggling to balance work and studies
- **binary_label**：合作

**context**

```text
来访者：Hey, I really need to talk about something that's been bothering me recently.
咨询师：Sure, I'm here to listen. What's going on?
```

**response（来访当前句）**

```text
So, I've been feeling overwhelmed lately with the amount of work and studying I have to do. It's becoming really difficult to find a balance between my job and my studies, and it's starting to take a toll on my mental health.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-9. `extes_2136_3` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：I'm feeling overwhelmed with my studies. Online learning has been difficult for me, and I'm struggling to manage my workload and stay motivated.
- **binary_label**：合作

**context**

```text
来访者：Hey, I've been really stressed out with my studies lately. Online learning has been a struggle for me, and it feels like I can't keep up with the workload. I'm feeling really overwhelmed.
咨询师：I can totally understand how you're feeling. Online learning can be challenging, and it's tough to stay motivated when you have so many assignments to juggle. Can you tell me more about what you're going through specifically?
来访者：Yeah, it's been really hard to concentrate and stay organized with everything. There are so many distractions at home, and I find myself getting easily distracted. Plus, it's tough to manage my time effectively with all the different deadlines.
咨询师：Are you finding it difficult to find a quiet study space at home? And are you also struggling to prioritize your tasks and manage your time efficiently?
来访者：Exactly! Finding a quiet space at home where I can focus has been a real challenge, especially with my family around. And time management is a constant struggle. I always end up procrastinating and feeling even more stressed.
咨询师：It sounds like you're dealing with a lot of challenges right now. It's completely understandable to feel overwhelmed and have trouble staying focused and managing your time in this situation.
```

**response（来访当前句）**

```text
Thank you for understanding. It's just frustrating because I really want to do well, but it feels like everything is working against me.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-10. `extes_10716_10` — 合作 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed by upcoming exams and struggling to manage time effectively
- **binary_label**：合作

**context**

```text
来访者：I've heard of the Pomodoro Technique before, but I haven't given it a try. I'll definitely try implementing it and creating a distraction-free study space. Thanks for the suggestions!
咨询师：You're welcome! I'm glad the suggestions resonated with you. Remember, by implementing these techniques and being kind to yourself, you can overcome this hurdle and excel in your exams. Stay positive!
来访者：Thank you for your support. It really means a lot to me. I'll keep pushing forward and focus on my own growth. It feels better knowing that I have someone to talk to about these things.
咨询师：I'm always here to listen and support you whenever you need. You're not alone in this journey. Keep up the great work and don't hesitate to reach out if you ever need someone to chat with or share your progress.
来访者：Thank you, that means a lot to me. I'll make sure to take care of myself and reach out if I need someone to talk to. Thanks again for being there for me.
咨询师：Of course! Take care of yourself and remember that you're capable of overcoming these challenges. I believe in you. Goodbye for now.
```

**response（来访当前句）**

```text
Thank you for everything. Take care, goodbye!
```

**raw_output（若有，节选）**

```text
合作

# 以上是本题的输入
```

---

### A-11. `extes_2220_4` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been experiencing anxiety and panic attacks recently due to social situations. It has been affecting my ability to attend events and gatherings, and I'm not sure how to cope with it.
- **binary_label**：合作

**context**

```text
来访者：Lately, I've been dealing with a lot of anxiety and panic attacks when I'm in social situations. It's been causing me to avoid events and gatherings, and I'm starting to feel isolated.
咨询师：I'm sorry to hear that you're going through this. Anxiety and panic attacks can be really challenging, especially in social situations. It must be tough to feel isolated because of it. You're not alone.
来访者：Thank you for understanding. It just feels overwhelming, and I don't know how to control my anxiety when I'm around people.
咨询师：I can understand why you would feel overwhelmed and troubled by your anxiety in social settings. It's completely valid to feel that way. It's important to remember that managing anxiety takes time and practice. Have you tried any techniques to cope with it?
来访者：I've tried deep breathing exercises and they help a bit, but I still struggle to calm down completely.
咨询师：It's good to hear that deep breathing exercises offer some relief. Can you tell me more about the situations that trigger your anxiety? Is it specific types of events or being around a large number of people?
```

**response（来访当前句）**

```text
I think it's more about being in large crowds or unfamiliar social situations. I worry about what people think of me and if I'll embarrass myself.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-12. `extes_2221_7` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been experiencing anxiety and panic attacks recently due to the pressure of starting a new job. It has been affecting my daily life, sleep quality, and ability to focus, and I'm not sure how to cope with it.
- **binary_label**：合作

**context**

```text
来访者：I'm afraid that if I talk about my anxiety and panic attacks, they won't see me as capable and it might affect my career prospects. So, I've been keeping it to myself.
咨询师：It's completely understandable that you feel hesitant to open up about your anxiety and panic attacks at work. However, it's important to remember that seeking support doesn't make you any less capable. It takes courage to ask for help, and your well-being should be a priority. Have you considered exploring resources like counseling services or employee assistance programs at your workplace?
来访者：I haven't thought about that. I didn't realize there might be resources available. I'll look into it. But in the meantime, I need help with managing my anxiety and panic attacks when they happen.
咨询师：Of course! Let's focus on coping with your anxiety and panic attacks in the moment. Have you tried any relaxation techniques or mindfulness exercises?
来访者：I've heard of deep breathing exercises, but I'm not sure if they actually work.
咨询师：Deep breathing exercises can be quite effective for managing anxiety and panic attacks. While they might not work for everyone, it's worth giving them a try. Additionally, you can explore other relaxation techniques like progressive muscle relaxation or guided meditation. It's about finding what resonates with you personally.
```

**response（来访当前句）**

```text
That makes sense. Are there any specific deep breathing exercises or guided meditation resources you would recommend?
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-13. `extes_2498_8` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I've been feeling overwhelmed by constant worry and experiencing frequent panic attacks. It's affecting my ability to focus on my work and enjoy everyday activities. I'm struggling to find ways to cope with these intense feelings of anxiety.
- **binary_label**：合作

**context**

```text
来访者：That's a good idea. I've been keeping it to myself because I didn't want to burden others, but maybe they can actually help me feel more secure.
咨询师：You definitely deserve support and understanding. Opening up to your loved ones about what you're going through can create a stronger support network for you. Remember, you don't have to face this alone.
来访者：You're right. I need to stop isolating myself. Thank you for reminding me of that.
咨询师：Of course! I sincerely believe that with the right support and coping strategies, you can manage your anxiety and panic attacks more effectively. Seeking help from a mental health professional like a therapist or counselor can provide additional tools and guidance.
来访者：I've been considering therapy but was hesitant. Hearing your encouragement makes me feel more confident about it.
咨询师：Therapy can be a valuable resource for developing coping mechanisms and strategies tailored to your needs. Talking to a professional who specializes in anxiety disorders can help you gain new insights and find techniques that work best for you. It's an empowering step towards taking control of your mental well-being.
```

**response（来访当前句）**

```text
You're right. I shouldn't let fear hold me back. I'm going to start looking for a therapist. Thank you for your support.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-14. `extes_55_4` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I'm feeling really anxious about returning to work after being on medical leave for anxiety. I'm worried about how my coworkers will perceive me and if I'll be able to handle the stress.
- **binary_label**：合作

**context**

```text
来访者：I've been struggling with anxiety, and I'm feeling really anxious about going back to work after being on medical leave.
咨询师：I can understand why returning to work might be causing anxiety. It's natural to worry about how your coworkers will perceive you and if you'll be able to handle the stress.
来访者：Exactly! It's been really hard for me to get back on track.
咨询师：I can relate to what you're going through. I've experienced anxiety myself, so I understand how challenging it can be to overcome and resume your regular routine.
来访者：It feels overwhelming, and I'm scared of having a panic attack at work.
咨询师：Remember, anxiety tends to amplify our worries and make them seem more intense than they actually are. It might help to remind yourself that you've coped with similar situations before, and you have the skills to manage your anxiety.
```

**response（来访当前句）**

```text
You're right. I have overcome anxiety in the past.
```

**raw_output（若有，节选）**

```text
合作

# 以上是本题的输入
```

---

### A-15. `extes_2212_4` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I've been experiencing intense anxiety and panic attacks whenever I have to drive. Even the thought of getting behind the wheel makes me feel overwhelmed and terrified. It's affecting my ability to go places and live my daily life.
- **binary_label**：合作

**context**

```text
来访者：I'm really struggling with anxiety and panic attacks related to driving. It's gotten so bad that I feel paralyzed by fear whenever I have to get in a car.
咨询师：I'm sorry to hear that. It must be incredibly distressing for you. Driving anxiety is a common challenge that many people face. Your worries and fears are valid.
来访者：Yes, it's like a constant battle inside my head. I worry about losing control of the vehicle and getting into an accident. Even short trips have become a nightmare.
咨询师：I can understand how distressing and intrusive those thoughts must be. Being afraid of losing control is a common fear, especially when it comes to driving. Your concerns are valid, and I want to help you overcome this fear.
来访者：Thank you for understanding. I just wish I could overcome this anxiety and drive without feeling overwhelmed.
咨询师：Overcoming driving anxiety takes time and practice, but it is possible. Have you tried any relaxation techniques, such as deep breathing exercises or progressive muscle relaxation? These methods can help calm your mind and body before getting behind the wheel.
```

**response（来访当前句）**

```text
I've never tried those techniques before. How do they work?
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-16. `extes_212_1` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been feeling extremely anxious lately due to the constant pressure at work and it's starting to affect my emotional well-being. I'm overwhelmed and finding it hard to cope with the stress.
- **binary_label**：合作

**context**

```text
来访者：Hi there
咨询师：Hello! How can I assist you today?
```

**response（来访当前句）**

```text
I've been feeling really anxious and stressed out lately. The workload at my job has been overwhelming and it's affecting my emotional state.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-17. `extes_2222_5` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been experiencing anxiety and panic attacks recently due to the stress of preparing for an important job interview. It has been affecting my sleep, appetite, and overall well-being, and I'm not sure how to manage it.
- **binary_label**：合作

**context**

```text
来访者：Thank you, I really appreciate that. I just feel like I can't control my anxiety and it's taking a toll on me.
咨询师：It's totally normal to feel that way when anxiety sets in. It's important to acknowledge that your emotions are valid. Understanding and recognizing your anxiety is already a huge step forward. Have you had previous experiences with anxiety before job interviews?
来访者：Yeah, I've always felt anxious before important events, but for some reason, it's getting worse this time. The fear of failure is just paralyzing.
咨询师：I can understand how the fear of failure can intensify your anxiety. It's a common feeling that many people experience. Just remember that it's okay to feel nervous, but try not to let it overpower you. You've achieved so much to get to this point.
来访者：I guess you're right. I've worked really hard for this opportunity, and I shouldn't let my anxiety diminish my confidence.
咨询师：Absolutely! You've got this! Acknowledging your accomplishments and strengths can help boost your confidence. Is there anything specific that triggers your panic attacks?
```

**response（来访当前句）**

```text
The thought of being evaluated and questioned during the interview makes me feel extremely anxious. I also worry about saying the wrong things and being judged.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-18. `extes_55_7` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I'm feeling really anxious about returning to work after being on medical leave for anxiety. I'm worried about how my coworkers will perceive me and if I'll be able to handle the stress.
- **binary_label**：合作

**context**

```text
来访者：You're right. I have overcome anxiety in the past.
咨询师：That's wonderful to hear! You've already shown resilience and strength in dealing with anxiety before. You can definitely draw on that experience to manage your return to work.
来访者：I guess I'm also worried about what my coworkers will think of me after being on medical leave.
咨询师：It's completely understandable to have these concerns. Remember, taking medical leave to address your anxiety is a courageous step, and it shows your commitment to taking care of your well-being. Most supportive coworkers will understand this.
来访者：I hope they do. I don't want them to view me differently.
咨询师：It sounds like you're concerned about maintaining positive relationships with your coworkers while also managing your anxiety. Is that accurate?
```

**response（来访当前句）**

```text
Yes, exactly! I want to be seen as capable.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的回应
```

---

### A-19. `extes_2505_3` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Lately, I've been feeling extremely anxious and panicky because I have an upcoming presentation at work. I'm afraid of embarrassing myself and it's causing me a lot of stress. I don't know how to cope with this overwhelming anxiety.
- **binary_label**：合作

**context**

```text
来访者：Hey, I could really use someone to talk to right now.
咨询师：Hi there, I'm here for you. What's been bothering you?
来访者：I've been feeling so anxious and panicky lately because I have this important presentation at work. I'm so worried about messing it up and it's making me so stressed.
咨询师：I can understand how stressful it must be for you. Presentations can be nerve-wracking, especially when we put pressure on ourselves to perform perfectly. But remember, making mistakes is a part of the learning process, and it's okay to not be perfect.
来访者：I know, but I just can't seem to calm down. The anxiety is affecting my sleep and overall well-being.
咨询师：I can empathize with what you're going through. Anxiety can really take a toll on our mental and physical health. It's essential to find ways to manage it.
```

**response（来访当前句）**

```text
Any suggestions on how I can manage this anxiety?
```

**raw_output（若有，节选）**

```text
合作

# 输出
合作

# 输出
```

---

### A-20. `extes_9080_2` — 合作 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Recently, I've been experiencing panic attacks at work. Every time I have to give a presentation or speak in front of a group, I start feeling extremely anxious and my heart races. It's affecting my performance and causing me a lot of stress and worry.
- **binary_label**：合作

**context**

```text
来访者：Hi, I need some advice.
咨询师：Hello, I'm here to help. What's been going on?
来访者：I've been having panic attacks at work whenever I have to give presentations.
咨询师：I'm really sorry to hear that, it sounds like a really challenging situation. Can you tell me more about what triggers these panic attacks?
```

**response（来访当前句）**

```text
It usually happens when I have to speak in front of a group. As soon as I start talking, I feel this overwhelming sense of anxiety and my heart starts pounding.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-21. `extes_2223_15` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being in a serious relationship for five years, my partner and I have decided to end our relationship. I'm feeling heartbroken and unsure of how to start over.
- **binary_label**：合作

**context**

```text
来访者：Thank you for the support. I'll try my best to move forward and find happiness.
咨询师：That's the spirit! Take care of yourself, surround yourself with positivity, and remember there is a bright future waiting ahead. Reach out anytime you need someone to talk to.
来访者：I will. Thank you again for everything.
咨询师：Don't mention it! I'm here for you. Take care and stay strong.
来访者：Goodbye for now.
咨询师：Goodbye! Remember, you're stronger than you think, and brighter days are on the way.
```

**response（来访当前句）**

```text
Thank you. Goodbye!
```

**raw_output（若有，节选）**

```text
合作

# 以上是合作的回应
```

---

### A-22. `extes_4559_1` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：My close friend and I recently ended our friendship due to a misunderstanding. I'm feeling hurt and confused about how to move forward without them in my life.
- **binary_label**：合作

**context**

```text
来访者：Hey, I'm going through a tough time. My best friend and I recently had a falling out, and it's left me feeling really hurt and lost.
咨询师：I'm here for you. It sounds like ending your friendship has been really challenging for you. Can you tell me more about how you're feeling right now?
```

**response（来访当前句）**

```text
I feel hurt and betrayed by my friend's actions. We used to confide in each other and support one another, but now I feel like I've lost an important connection in my life.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-23. `extes_1686_6` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being in a long-distance relationship for three years, my partner and I have decided to break up. It's been emotionally challenging for me, and I'm struggling with feelings of sadness and loneliness.
- **binary_label**：合作

**context**

```text
来访者：Thank you. It's just hard to imagine my life without them
咨询师：I can imagine that must be really difficult. It's okay to grieve the loss and take some time to heal. Are there any support systems or activities that have helped you through tough times in the past?
来访者：My friends have always been there for me, but it's still hard to overcome this feeling of emptiness
咨询师：I understand. Even with support, it can still be tough to overcome the feeling of emptiness. Remember, healing takes time. During this period, it might be helpful to engage in self-care activities that bring you comfort and joy. What are some activities that usually help you feel better?
来访者：I find solace in painting and listening to music
咨询师：That's great! Painting and listening to music can be therapeutic and help release emotions. Continue nurturing your creative side and use these activities as a form of self-expression. They can also provide a temporary escape from the pain you're feeling. Do you have any other hobbies or interests you could explore?
```

**response（来访当前句）**

```text
I used to enjoy hiking and haven't done it in a while
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-24. `extes_4502_7` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：I recently went through a difficult divorce with my spouse of ten years. It's been hard for me to adjust to the changes in my life and I'm feeling overwhelmed.
- **binary_label**：合作

**context**

```text
来访者：That's a good suggestion. I hadn't really considered therapy, but I think it could help. Right now, I just feel so alone and isolated.
咨询师：I'm glad you're open to the idea of therapy. It can be incredibly helpful in providing you with the guidance and support you need. Remember that you're not alone in this, even if it feels that way right now. Surrounding yourself with understanding and empathetic people, seeking professional help if necessary, and taking care of yourself are all important steps in the healing process. Is there anything you enjoy doing that brings you a sense of comfort or joy?
来访者：I used to love hiking and being in nature, but I haven't done it in a long time. Maybe spending time outdoors would help me find some peace.
咨询师：That's a wonderful idea! Spending time in nature can be incredibly therapeutic. It offers a chance to disconnect from the stresses of everyday life and reconnect with yourself. Make time to go hiking or simply take a walk in a nearby park. Surrounding yourself with the beauty of nature can bring you a sense of peace and help you find clarity during this difficult time. Is there a particular hiking trail or park you've been wanting to explore?
来访者：There's a national park not too far away that I've always wanted to visit. I think I'll plan a trip there and embark on a hiking adventure.
咨询师：That sounds like a fantastic plan! Planning a trip to the national park will give you something to look forward to and a chance to immerse yourself in nature. Take the time to research the best trails and prepare for the trip. You might also want to invite a supportive friend or family member to join you if they're available and willing. Remember, this journey is not just about hiking. It's about rediscovering yourself and finding moments of happiness along the way. If you have any questions or need suggestions, feel free to ask me!
```

**response（来访当前句）**

```text
Thank you, I really appreciate your support and guidance. It means a lot to me.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-25. `extes_10843_8` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：My long-term partner and I have recently ended our relationship. We were living together, and now I'm finding it difficult to adjust to being on my own.
- **binary_label**：合作

**context**

```text
来访者：I'm not sure how to move forward from here. Everything feels uncertain.
咨询师：I hear you. Can you share more about the specific uncertainties you're facing? Maybe we can explore some possibilities together.
来访者：I'm worried about being alone and starting over. The idea of rebuilding my life from scratch feels overwhelming.
咨询师：It's normal to feel overwhelmed by the thought of starting over. But remember, you're not alone. Reach out to your support system, whether it's friends, family, or even a therapist. They will be there to help you navigate this transition and offer guidance.
来访者：You're right. I should lean on my loved ones for support. I'm also afraid of being hurt again in the future.
咨询师：It's completely understandable to have fears about future relationships. However, it's important to remember that each relationship is unique, and the past doesn't define what will happen in the future. Take this time to focus on healing and personal growth, and when you're ready, you'll be able to approach new relationships with a clearer perspective.
```

**response（来访当前句）**

```text
Thank you for your support and advice. It really means a lot to me.
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-26. `extes_4257_7` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being together for three years, my partner and I have decided to end our relationship due to constant arguments and growing apart. I'm feeling devastated and lost, not knowing how to move on.
- **binary_label**：合作

**context**

```text
来访者：I hope you're right. How do I even begin to move on from this?
咨询师：Instead of thinking about it as 'moving on,' think of it as giving yourself the time and space to heal from the pain and rediscover your own identity. Start by focusing on self-care and doing things that make you happy. Surround yourself with supportive friends and family who can provide a listening ear and offer a shoulder to lean on.
来访者：That sounds challenging but necessary. I'll give it a try.
咨询师：Absolutely, it won't be easy, but remember that you're not alone in this journey. Many people have gone through similar experiences and come out stronger. Take it one day at a time, be patient with yourself, and allow the healing process to unfold naturally.
来访者：Thank you for your support. I'll take your advice to heart.
咨询师：You're welcome! Self-care is crucial during this time. What are some activities or hobbies that bring you joy or help you relax?
```

**response（来访当前句）**

```text
I used to love painting, and I find solace in nature. Maybe I should focus more on those activities.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-27. `extes_892_5` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being in a 10-year marriage, my husband and I have decided to get a divorce. I'm feeling overwhelmed and scared about starting over on my own.
- **binary_label**：合作

**context**

```text
来访者：I just can't believe this is happening. We've been together for so long, and now I have to face everything on my own. What if I can't handle it?
咨询师：It's completely understandable that you're feeling overwhelmed by the thought of starting anew. It's a significant change, and it's natural to worry about handling everything alone. Remember, though, that you're stronger than you think. You've made it through difficult times before, and you can do it again. I'm here to support you every step of the way. Would you like to explore practical ways we can help ease your transition?
来访者：Thank you for being there. I'm not sure where to start. How can I even begin rebuilding my life and finding happiness again?
咨询师：Resilience is an incredible quality you possess, and it's important to give yourself credit for that. Starting over takes time, but it also provides an opportunity for personal growth and rediscovering your passions. One step at a time, focus on self-care, reconnecting with old hobbies or interests, and building a support system of friends and loved ones. Remember, this is a fresh start, and you have the chance to create a life that brings you fulfillment and happiness.
来访者：I guess you're right. It's just hard to envision a bright future right now. I can't help but feel a sense of loss.
咨询师：Feeling a sense of loss and uncertainty is completely normal during times like these. It's okay to grieve the end of your marriage and the life you had imagined. Take your time to process your emotions, as healing takes time. Surround yourself with supportive people who can provide the comfort and understanding you need. Remember, you're not alone in this. We're in this together, and I'll be here every step of the way.
```

**response（来访当前句）**

```text
Thank you for your support. It means a lot to have someone to talk to during this difficult time.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-28. `extes_10144_5` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being in a long-distance relationship for three years, my girlfriend and I recently decided to end things because the distance became too challenging to bear. I'm feeling heartbroken and unsure about how to move forward.
- **binary_label**：合作

**context**

```text
来访者：I'm struggling to accept that it's over. I keep replaying all the memories and thinking about what could have been. I just wish things had turned out differently.
咨询师：It's completely normal to grieve the loss of a relationship and to have thoughts about what could have been. It's important to allow yourself to process these emotions. Have you considered seeking support from friends or a therapist to help you through this difficult time?
来访者：I haven't thought about it, but maybe talking to someone would help. Do you have any suggestions?
咨询师：Absolutely. First, confide in your closest friends or family members. They can provide a listening ear and support during this challenging time. Additionally, you can consider seeking professional help and talking to a therapist who specializes in relationships and heartbreak. They can provide guidance and strategies for coping with the pain.
来访者：I'll reach out to my friends and consider talking to a therapist. I never realized how important it is to take care of my mental health during a breakup. Thank you for suggesting it.
咨询师：You're welcome. Taking care of your mental health is crucial, especially during difficult times. Remember to be kind to yourself and prioritize self-care. Is there anything else you'd like to talk about or any other concerns you have?
```

**response（来访当前句）**

```text
Another thing that's been bothering me is the fear of being alone and starting over. It's overwhelming and scary.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-29. `extes_4536_2` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：Lately, I've been struggling with a recent divorce. My spouse and I decided to separate after 10 years of marriage. I feel overwhelmed and unsure of how to move forward.
- **binary_label**：合作

**context**

```text
来访者：Hey, I've been going through a really tough time lately
咨询师：Hi there. I'm here to listen. What's been happening?
来访者：My spouse and I recently got divorced after 10 years together
咨询师：I'm really sorry to hear that. Going through a divorce can be extremely challenging and emotionally draining. How are you feeling about it?
```

**response（来访当前句）**

```text
I feel devastated and lost. This relationship meant the world to me and now it's all over
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-30. `extes_10827_3` — 合作 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being together for three years, my partner and I have recently broken up because of our constant arguments and inability to meet each other's needs. I am feeling heartbroken and unsure of how to move on.
- **binary_label**：合作

**context**

```text
来访者：Hey, I just went through a tough breakup. It's been really hard for me to accept that it's over.
咨询师：I'm sorry to hear that you're going through this. Can you tell me more about what happened in your relationship?
来访者：We had been arguing too much and couldn't find common ground. It felt like we were constantly pulling in different directions. It became exhausting for both of us.
咨询师：That sounds incredibly challenging. It takes a toll when two people in a relationship can't seem to find a way to meet each other's needs. How are you feeling about the breakup?
来访者：I'm heartbroken because I still love my ex, but at the same time, I know it's for the best. It's hard to let go of our dreams together.
咨询师：It's completely normal to feel heartbroken after a breakup, especially when you still love the person. Letting go of shared dreams can be incredibly difficult. Have you been finding any ways to cope with these emotions?
```

**response（来访当前句）**

```text
I've been spending a lot of time with friends and distracting myself with work. It helps to have support around me.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的行为是
```

---

### A-31. `extes_6370_8` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling disconnected from my family lately and it's causing a lot of strain in our relationship. I want to find a way to reconnect and communicate better.
- **binary_label**：合作

**context**

```text
来访者：You're right. I shouldn't be afraid to speak up and express myself. I'll give it a try.
咨询师：That's a great approach! By opening up the lines of communication, there's a chance for understanding and growth within your family. Just remember to be patient and listen actively.
来访者：I'll do my best. Hopefully, we can find a way to reconnect and understand each other better.
咨询师：Maybe you can suggest setting aside dedicated time each week to have family meetings or activities where everyone can share their thoughts and feelings in a safe space.
来访者：That's a wonderful idea. I think creating a designated time for open communication will help us reconnect. I'll propose it to my family.
咨询师：Another perspective you can consider is seeking professional help like family therapy. A neutral third party can facilitate conversations and provide guidance in rebuilding connections.
```

**response（来访当前句）**

```text
I hadn't thought about that. It might be helpful to have a professional mediate our discussions. I'll discuss it with my family as well.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-32. `extes_7386_6` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been struggling to communicate effectively with my partner about our future plans. We have different ideas and goals, and it's causing a lot of tension in our relationship. I'm afraid we won't be able to find a compromise.
- **binary_label**：合作

**context**

```text
来访者：Yes, it's been weighing on me a lot. I worry that we won't be able to reach an agreement and it will put a strain on our relationship.
咨询师：It's completely normal to feel that way. Having differing opinions on significant life choices can feel overwhelming and put a strain on any relationship.
来访者：I just wish there was a way for us to find a middle ground or understand each other better.
咨询师：Your desire to find a compromise and understand each other better is a positive step toward resolving this challenge. It shows your commitment to the relationship.
来访者：Thank you for saying that. It's reassuring to know that it's not unreasonable for me to hope for a resolution.
咨询师：Absolutely! Every relationship faces challenges, and finding common ground can take time. It might help to take a step back and recognize that this is a normal part of growth together.
```

**response（来访当前句）**

```text
That's a good point. We've been together for a while, so it's natural to encounter some obstacles along the way.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-33. `extes_2650_4` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling really stressed out at work lately and it's affecting my performance and overall well-being.
- **binary_label**：合作

**context**

```text
来访者：I'm not doing so great. I've been feeling really stressed out and it's been affecting my work and personal life.
咨询师：I'm sorry to hear that. It can be incredibly challenging when stress starts to take a toll on different aspects of our lives. Can you tell me more about what's been happening at work?
来访者：I've been assigned a lot of new responsibilities and the deadlines are piling up. It feels overwhelming and I'm constantly worried about not meeting expectations.
咨询师：That sounds very overwhelming indeed. It's completely normal to feel stressed in such demanding situations. Have you tried talking to your supervisor or colleagues about your workload concerns?
来访者：I haven't yet. I'm afraid of appearing weak or incompetent if I express my struggles.
咨询师：I understand your concerns, but keeping these worries to yourself will only add to the stress. Perhaps you can consider scheduling a meeting with your supervisor to openly discuss your workload and see if any adjustments can be made.
```

**response（来访当前句）**

```text
You're right. I shouldn't let my fears hold me back from seeking support at work.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-34. `extes_3563_7` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling disconnected from my partner lately, and we have been struggling to communicate effectively. It's been causing a lot of tension and frustration in our relationship.
- **binary_label**：合作

**context**

```text
来访者：That's a good idea. We usually end up interrupting or criticizing each other, which only makes things worse. I'll suggest having dedicated conversations where we both can express ourselves without judgment.
咨询师：That's a great step to take! Remember, it's not about blaming each other but working together to find solutions. By creating a safe and non-judgmental space, both of you can feel heard and understood.
来访者：I will keep that in mind. It's just hard not to feel frustrated with the situation at times.
咨询师：Feeling frustrated in this situation is completely understandable. It's important to acknowledge your emotions. Remember to be patient with yourselves and allow each other time to process and grow in your communication journey.
来访者：Thank you for understanding. I really appreciate the advice and support.
咨询师：You're welcome! Facing challenges in relationships can be tough, but by actively working on your communication, both of you can strengthen your bond. I believe in your ability to navigate through this.
```

**response（来访当前句）**

```text
Thank you so much for your kind words and encouragement. It means a lot.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-35. `extes_4306_6` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently moved to a new city and I'm struggling to make new friends. It's been hard to find people with similar interests and connect with them.
- **binary_label**：合作

**context**

```text
来访者：You're right, maybe I'm just being too hard on myself. I'll try to be more patient and open to new opportunities.
咨询师：That's a great mindset to have! Being open to new opportunities and staying positive will definitely increase your chances of meeting like-minded people. Remember, it's not a reflection of your worth or likability. You're deserving of meaningful friendships, and with time and effort, you'll find them. Is there anything specific you've tried doing to meet new people?
来访者：I've tried attending some social events and joining hobby groups, but I guess I haven't been consistent. Maybe I should make more of an effort to regularly participate in activities.
咨询师：That sounds like a great plan! Consistency is key when it comes to meeting new people. By regularly participating in activities that align with your interests, you'll have better chances of meeting individuals who share similar passions. It might also be helpful to connect with local social groups or organizations through online platforms. This way, you can stay updated on events and activities happening in your area.
来访者：I haven't really explored online platforms for connecting with people. Do you have any recommendations?
咨询师：Certainly! There are several online platforms that can help you connect with people who share similar interests. Some popular options include Meetup, Bumble BFF, or local Facebook groups related to your hobbies or community. These platforms often have various events and community gatherings, providing an opportunity to meet new people. Additionally, you can search for forums or online communities that focus on your specific interests.
```

**response（来访当前句）**

```text
Wow, I didn't realize there were so many options available. I'll definitely give those platforms a try and explore the online communities too. Thank you for the suggestions!
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-36. `extes_2648_7` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been having trouble expressing my emotions to my partner and it's causing misunderstandings in our relationship.
- **binary_label**：合作

**context**

```text
来访者：I've mentioned it in passing, but I don't think I've made it clear just how much it affects me.
咨询师：It can be challenging to express our emotions, especially when we fear how the other person may react. Your feelings are valid and it's important for your partner to be aware of the impact their dismissiveness has on you. Perhaps having a more direct and focused conversation about this could help.
来访者：You're right. I should have a deeper conversation with them. I just worry that they won't understand.
咨询师：It's natural to have concerns about how your partner may react, but withholding your feelings won't help create a healthier line of communication. In a supportive relationship, it's important to create a safe space for both of you to express your emotions without fear of criticism. Honest communication is key.
来访者：I guess you're right. I need to be open and let my partner know how significant this is for me. It's scary, but it's necessary for our relationship to grow.
咨询师：Absolutely! Taking that step towards open and honest communication can pave the way for a stronger and more understanding relationship. Remember, both of you want what's best for each other, and by expressing your emotions openly, you're fostering growth and understanding.
```

**response（来访当前句）**

```text
Thank you for your support. I've gained some courage to initiate this conversation. I really appreciate your help.
```

**raw_output（若有，节选）**

```text
合作

# 以上是本题的输入
```

---

### A-37. `extes_7484_2` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling really anxious lately because I have an important presentation at work, and I'm struggling with public speaking.
- **binary_label**：合作

**context**

```text
来访者：Hey, can we talk for a moment?
咨询师：Of course! I'm here to listen. What's on your mind?
来访者：I've been feeling incredibly anxious lately. I have to give an important presentation at work, and I'm really struggling with public speaking. I get so nervous that my mind goes blank, and I stumble over my words.
咨询师：I can understand how nerve-wracking it can be to give a presentation, especially when you struggle with public speaking. It's completely normal to feel anxious and experience difficulties while speaking in front of others. You're not alone in facing these challenges. Can you tell me more about the importance of this presentation and the specific concerns you have?
```

**response（来访当前句）**

```text
Sure, this presentation is a vital opportunity for me to showcase my work to upper management. If I mess it up, it could have a significant impact on my career. I'm worried about stumbling over my words, forgetting important points, and letting my nerves get the best of me.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-38. `extes_3708_9` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently moved to a new city and I'm struggling to make new friends. I feel lonely and it's affecting my overall well-being.
- **binary_label**：合作

**context**

```text
来访者：Thank you for the encouragement. It means a lot.
咨询师：You're welcome. Remember, many people have faced similar challenges when moving to a new place. It's a normal part of adjusting to a new environment.
来访者：That's reassuring to hear. I'm glad to know I'm not alone in this.
咨询师：In the meantime, it's important to prioritize self-care. What are some activities or hobbies that bring you joy and help you relax?
来访者：I enjoy going for walks in the park and practicing yoga. Those activities help me clear my mind and destress.
咨询师：That's wonderful! Spending time in nature and engaging in mindful activities like yoga can have a positive impact on your overall well-being. Make sure to set aside time for them regularly.
```

**response（来访当前句）**

```text
You're right. I'll make self-care a priority. Thank you for the reminder.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-39. `extes_2723_4` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：Lately, I've been having constant arguments with my partner, and it's been really difficult to communicate effectively. I feel like we're always on different pages, and it's causing a lot of emotional distress.
- **binary_label**：合作

**context**

```text
来访者：I've been having a lot of arguments with my partner lately, and it's really taking a toll on me. We just can't seem to communicate properly.
咨询师：I'm sorry to hear that. Being in constant arguments with a partner can be really tough and emotionally draining. It's completely normal to feel distressed when there's a breakdown in communication. Can you share more about what specifically leads to these arguments?
来访者：It feels like we're always on different pages, and we misinterpret each other's intentions. I try to express my feelings, but it often ends up in a heated argument and we both get defensive.
咨询师：Misinterpretations and differences in perspectives can definitely hinder effective communication and escalate conflicts. It sounds like both of you might be struggling with expressing your feelings in a way that allows for understanding rather than defensiveness. Have you considered seeking clarification during these conversations?
来访者：Not always. In the heat of the moment, it becomes difficult to step back and try to seek clarification. We get caught up in our own emotions and the argument continues to escalate.
咨询师：I can understand how emotions can quickly take over during a disagreement, making it challenging to maintain clarity in the conversation. It's important to remember that taking a step back and seeking clarification can help break this cycle of escalation. I know it's easier said than done, but it's worth giving it a try.
```

**response（来访当前句）**

```text
You're right. I need to try harder to pause and ask for clarification instead of reacting immediately. Maybe that will help us understand each other better.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-40. `extes_5387_9` — 合作 | Communication Challenges

- **scene**：Communication Challenges
- **description**：A user is struggling to communicate with their teenage daughter and feels like they're constantly misunderstood.
- **binary_label**：合作

**context**

```text
来访者：I'll keep that in mind. I hope things improve soon. Thanks for your advice.
咨询师：You're welcome! It's fantastic that you're willing to try new approaches and not giving up. Building a strong parent-child relationship takes time and effort, but I believe in your ability to create a nurturing and communicative environment. Keep the lines of communication open, and remember that progress often happens incrementally. Feel free to reach out anytime if you'd like further guidance or support.
来访者：Thank you so much for your support. It means a lot to have someone to talk to about this.
咨询师：I'm here for you. Parenting can be challenging, and it's crucial to have support and a listening ear. Remember, you're not alone in this journey, and there are resources and professionals who can also offer guidance and support. Take care, and remember to prioritize self-care as well.
来访者：I really appreciate that. Thank you for your encouragement. Take care!
咨询师：You're very welcome! It was my pleasure to assist you. Take care of yourself and your family. Remember, small steps towards better communication can lead to significant positive changes in your relationship. Have a wonderful day!
```

**response（来访当前句）**

```text
You too! Thank you once again. Have a great day!
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-41. `extes_1540_2` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I have been having a lot of misunderstandings and arguments with my sister lately, and it's really affecting our relationship. I don't know how to resolve these conflicts and regain our connection.
- **binary_label**：合作

**context**

```text
来访者：Hey, do you have a moment? I need someone to talk to about something that's been bothering me.
咨询师：Of course! I'm here to listen. What's been going on with you and your sister?
来访者：My relationship with my sister has been really strained recently. We seem to constantly misunderstand each other and it's causing a lot of tension between us. I'm worried that we're drifting apart and I don't want that to happen.
咨询师：It sounds like you're feeling disconnected from your sister due to these misunderstandings. Can you give me an example of a recent argument or misunderstanding you've had with her?
```

**response（来访当前句）**

```text
Well, there was a situation where I thought she was ignoring me during a family gathering. I confronted her about it, and she got defensive and accused me of overreacting. It hurt me deeply and now we barely talk to each other.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-42. `extes_9632_3` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my boss always interrupts me during meetings and dismisses my ideas and contributions.
- **binary_label**：合作

**context**

```text
来访者：Hey, I really need to talk about something that's been bothering me at work.
咨询师：Of course, I'm here to listen. What's been going on?
来访者：During team meetings, my boss constantly interrupts me and undermines my ideas. It makes me feel belittled and like my contributions don't matter.
咨询师：I want to make sure I understand the situation clearly. Can you tell me more about how your boss interrupts you and dismisses your ideas?
来访者：Whenever I try to share my thoughts or present a suggestion, my boss cuts me off, dismisses my ideas, and redirects the conversation without giving me a chance to fully explain myself. It's demoralizing.
咨询师：That sounds incredibly frustrating and disheartening. It's important for your boss to create a supportive environment where everyone's input is valued and respected. How has this been affecting you?
```

**response（来访当前句）**

```text
It's been quite discouraging. I feel hesitant to speak up during meetings now and less confident in my own abilities. It also makes me feel undervalued as an employee.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-43. `extes_9797_1` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my partner and I have been arguing a lot recently and it's causing strain in our relationship.
- **binary_label**：合作

**context**

```text
来访者：Hey, I wanted to talk to you about something that's been on my mind lately.
咨询师：Of course! I'm here to listen. What's been happening?
```

**response（来访当前句）**

```text
Well, my partner and I have been arguing a lot recently, and it's starting to affect our relationship.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-44. `extes_9427_3` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling upset because my best friend and I had a disagreement that caused a strain in our relationship.
- **binary_label**：合作

**context**

```text
来访者：Hey, can we talk about something that's been bothering me lately?
咨询师：Of course! I'm here to listen. What's been bothering you?
来访者：My best friend and I had a disagreement, and it's really been putting a strain on our friendship. I'm feeling upset and don't know how to resolve it.
咨询师：I can understand how difficult that must be for you. Disagreements with close friends can be challenging, especially when it affects the relationship. Can you tell me more about what happened?
来访者：We were discussing a topic we both feel strongly about, and it quickly escalated into an argument. We ended up saying hurtful things to each other, and now we've been distant and not talking like we used to. I miss our close bond and want to find a way to repair it.
咨询师：I can completely understand your feelings. It's tough when disagreements turn into hurtful words and strain a friendship. It's clear that you value your close bond with your best friend. Have you attempted to communicate and address the issue since the argument?
```

**response（来访当前句）**

```text
I've tried reaching out, but they seem reluctant to talk about it. It's frustrating because I don't want to lose the friendship over a disagreement, but I also don't want to force them to talk if they're not ready.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-45. `extes_3987_6` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my best friend and I keep having misunderstandings and it's causing tension in our friendship. Lately, we've been arguing a lot over different opinions and it's starting to strain our relationship. It feels like we can't communicate effectively and it's causing a lot of stress and confusion.
- **binary_label**：合作

**context**

```text
来访者：We have tried, but it feels like we're talking past each other. It's frustrating and we end up getting defensive.
咨询师：It can be difficult to have productive conversations when emotions run high. How about creating a safe space where both of you can express yourselves openly without fear of judgment or criticism?
来访者：That's a good idea. We need to learn to listen to each other without feeling attacked. But staying calm in the heat of the moment is hard.
咨询师：You're absolutely right. Keeping calm during arguments can be challenging, especially when emotions are intense. One technique that might help is taking a short break during arguments to cool off and approach the conversation with a clearer perspective.
来访者：That's worth trying. I'll suggest it to my friend. I really hope we can improve our communication and find common ground.
咨询师：That's a positive approach. Along with taking breaks and practicing active listening, perhaps you could both make a list of alternative destinations that offer both relaxation and adventure. Exploring new options might help you find a compromise that satisfies both of you.
```

**response（来访当前句）**

```text
I hadn't thought of that. It sounds like a good idea. Thank you for your advice and for listening to me.
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-46. `extes_867_8` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my roommate keeps leaving dirty dishes in the sink.
- **binary_label**：合作

**context**

```text
来访者：I'll try to have a more serious conversation with them. But what if they get defensive or don't understand why I'm upset?
咨询师：It's possible that your roommate may not initially respond positively, but it's important to express your feelings and set boundaries. By addressing the issue, you're standing up for yourself and promoting a healthier living environment. If they don't understand or get defensive, consider involving a neutral mediator, such as a trusted friend or your landlord, to help facilitate the conversation.
来访者：That's a good idea. I will try talking to them again and involve someone else if needed. Thanks for your advice.
咨询师：You're welcome! It takes courage to address these types of situations, and I believe in your ability to handle it. Remember, your living situation should be a positive and respectful experience. Don't hesitate to seek support from others if you need it.
来访者：I appreciate your support and guidance. It's good to have someone to talk to about this. I hope things improve.
咨询师：Absolutely, it's important to have someone to talk to. Many people have faced similar situations with their roommates and understand the frustration it can bring. Remember to take care of yourself during this process, and don't hesitate to reach out whenever you need support.
```

**response（来访当前句）**

```text
Thank you. I will keep that in mind. Hopefully, we can resolve this issue and restore our friendship.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-47. `extes_6746_11` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my co-worker keeps taking credit for my work, and it's causing tension in the workplace.
- **binary_label**：合作

**context**

```text
来访者：I think I'll start by clarifying my role and contributions in the projects we've worked on together. I want to make it clear that I expect credit where it's due and that I won't tolerate any more misrepresentation.
咨询师：That sounds like a constructive approach. Additionally, when discussing your concerns with your co-worker, you might also consider mentioning the importance of establishing a positive collaborative environment, where everyone's contributions are valued and recognized.
来访者：That's a good point. I want to emphasize the significance of working together as a team and acknowledging each other's efforts. Thank you for the suggestion.
咨询师：You're welcome! While addressing this issue, don't forget to take care of yourself too. Engage in activities outside of work that bring you joy and help you relax, whether it's spending time with loved ones or pursuing hobbies you enjoy.
来访者：I will definitely prioritize self-care during this process. Thanks for the reminder.
咨询师：You're welcome! If you need any further support or guidance, feel free to reach out. Good luck with your conversation, and I hope things improve in your working relationship.
```

**response（来访当前句）**

```text
Thank you so much for your help and encouragement. I really appreciate it.
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-48. `extes_8368_6` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my best friend and I had a misunderstanding, and now we're not talking to each other. Our friendship means a lot to me, and I want to find a way to resolve the conflict and improve our communication.
- **binary_label**：合作

**context**

```text
来访者：I've tried reaching out a couple of times, but my best friend seems unwilling to talk or listen. It's frustrating because I really want to find a resolution.
咨询师：It's tough when one person is unreceptive to engaging in a conversation, especially when you're eager for resolution. Keep in mind that resolving conflicts takes time and patience. During this period, focus on taking care of yourself and expressing that you're open to discussing things whenever your best friend is ready.
来访者：I understand that it takes time, but it's hard to be patient and not take it personally. I just want us to resolve this and be close again.
咨询师：Feeling impatient and wanting resolution is completely understandable. Many friendships go through periods where communication breaks down, but that doesn't mean there's no hope. Trust that your best friend also values the friendship and wants to find a resolution. In the meantime, focus on self-care and self-expression.
来访者：You're right. I shouldn't lose hope. I'll try to be patient and take care of myself while waiting for my best friend to be ready. Thank you for listening and providing guidance.
咨询师：You're welcome! Remember, friendships require effort and time to work through conflicts. Don't be too hard on yourself, and continue being open to solving the issue together. If you ever need someone to talk to, I'm always here for you.
```

**response（来访当前句）**

```text
Thank you so much for your support. Having someone to talk to really means a lot to me.
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-49. `extes_9529_2` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling upset because my best friend is always canceling plans last minute, and it's causing a strain on our friendship.
- **binary_label**：合作

**context**

```text
来访者：Hey, can I talk to you about something that's been bothering me?
咨询师：Of course! I'm here to listen. What's been bothering you?
来访者：Well, I've been having some issues with my best friend. They keep canceling plans at the last minute, and it's really starting to strain our friendship.
咨询师：I can understand why that would be upsetting. It's tough when someone consistently cancels plans, especially when it's your best friend. Can you tell me more about how this has been affecting you?
```

**response（来访当前句）**

```text
It's been making me feel unimportant and undervalued. I put effort into planning our hangouts, and it hurts when they always cancel. I'm starting to question the strength of our friendship.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-50. `extes_5975_2` — 合作 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated and upset because my best friend and I had a big argument about our future plans and now we're not speaking to each other.
- **binary_label**：合作

**context**

```text
来访者：Hey, are you there?
咨询师：Yes, I'm here. Sorry for the delay. What's going on? It seems like something is bothering you.
来访者：It's about my best friend. We had a huge argument about our future plans and now it feels like our friendship is falling apart. I'm really devastated.
咨询师：I understand how difficult it can be to have a falling out with a close friend. It's completely normal to feel upset and devastated in this situation.
```

**response（来访当前句）**

```text
Yeah, it's just frustrating because we've always supported each other's dreams. But now it feels like we're not on the same page anymore.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-51. `extes_10871_5` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My cousin's father recently passed away from a prolonged illness, and she is struggling to cope with the loss. She feels guilty for not being able to spend more time with him during his final days and is overwhelmed by grief.
- **binary_label**：合作

**context**

```text
来访者：She's been feeling so guilty about not being able to spend more time with her dad, especially during his final days. She's overwhelmed with grief and it's affecting her daily life.
咨询师：It's completely normal for her to feel guilty and overwhelmed right now. Losing a loved one is never easy, and it's common to grapple with regrets and a range of conflicting emotions. How has she been expressing her grief so far?
来访者：She's been crying a lot and isolating herself from others. She hasn't really talked about it much.
咨询师：It's understandable that she's finding it hard to express her emotions openly. Grief can be a deeply personal journey, and everyone processes it differently. Have you tried talking to her about how she's feeling or offered any support?
来访者：I've tried to let her know that I'm here for her, but she hasn't opened up much. She feels like she should be able to handle it on her own.
咨询师：It's not uncommon for people to hesitate seeking support during such difficult times. However, reminding her that she doesn't have to go through this alone could help. Grief counselors or support groups can provide her with a nurturing environment to share her feelings and find appropriate ways to cope. Encouraging her to consider these options might be beneficial.
```

**response（来访当前句）**

```text
That's a good point. I'll keep reminding her that she doesn't have to face this alone. I'll suggest the idea of seeking professional help and attending a support group. Thank you for your advice. It means a lot.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-52. `extes_4815_9` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away from a long battle with cancer, and I'm struggling to process my emotions. I feel overwhelmed and lost, and I'm not sure how to cope with the grief.
- **binary_label**：合作

**context**

```text
来访者：That's a beautiful idea. I think it could give me a sense of connection and a way to keep my uncle's memory alive.
咨询师：Absolutely. Another perspective to consider is joining a grief support group or seeking counseling. It could provide a safe space to share your experiences, gain insights from others who have also experienced loss, and learn healthy ways to cope with your grief.
来访者：I've never thought about that before, but it sounds like it could be helpful. Being in a supportive environment where others understand what I'm going through could make a difference.
咨询师：Taking care of yourself is crucial during this time. It might be helpful to engage in activities that bring you comfort and solace, such as journaling, going for walks in nature, or listening to calming music. These self-care practices can support your emotional well-being.
来访者：I'll try incorporating those activities into my routine. It's essential to prioritize self-care, especially during times when I'm feeling low.
咨询师：Remember, everyone grieves at their own pace, and there's no right or wrong way to go through this process. It can be helpful to remind yourself that it's a normal part of life, and as time goes on, the pain and sadness may gradually lessen.
```

**response（来访当前句）**

```text
I'll keep that in mind. It's comforting to know that what I'm experiencing is a normal part of the grieving process.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-53. `extes_10363_7` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My sister's husband recently passed away, and she is struggling to navigate her emotions and responsibilities as a single parent.
- **binary_label**：合作

**context**

```text
来访者：She's been going through waves of sadness and often breaks down crying. I've encouraged her to seek counseling, but she feels like she should be able to handle it on her own.
咨询师：It's common for people to think that they should be able to handle their emotions on their own, but there's no shame in seeking professional help. Grief counseling can provide her with valuable tools, support, and a safe space to process her emotions. You might want to continue encouraging her to consider it as an option.
来访者：You're right. I'll talk to her again and emphasize the benefits of professional support. I just want her to find some peace.
咨询师：That's a great approach. Your support for your sister is truly valuable, and she will undoubtedly appreciate your persistent encouragement. Remember to also take care of yourself during this emotionally challenging time. If there's anything else you'd like to discuss or any other way I can assist you, please let me know.
来访者：Thank you for being here to listen and offer guidance. It means a lot to me. For now, I just needed someone to talk to, and you've provided that support.
咨询师：I'm glad I could be here for you. Just remember, you're never alone in this journey of supporting your sister. Feel free to reach out whenever you need someone to talk to. I'll always be here to listen. Take care!
```

**response（来访当前句）**

```text
Thanks again. Take care!
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-54. `extes_10202_6` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：I recently lost my grandmother to COVID-19. It has been extremely challenging for me to navigate this loss while also dealing with the isolation and fear caused by the pandemic. I'm struggling to find ways to cope with my grief and move forward.
- **binary_label**：合作

**context**

```text
来访者：I would love to share some memories. My grandmother was such an amazing cook. She would spend hours in the kitchen, teaching me her secret family recipes. I miss the smell of her food and the warmth of her presence.
咨询师：It's beautiful that you have those memories of your grandmother's cooking. It shows the bond you shared and the love she had for you. Holding onto those memories and continuing her traditions can be a meaningful way to honor her. How are you managing your grief during these challenging times?
来访者：It's been tough. I've been feeling quite isolated due to the pandemic restrictions, which makes it harder to find support. I'm trying to reach out to friends through virtual calls, but it's not the same as having someone physically present.
咨询师：I completely understand the challenges of finding support during these times. Virtual connections are a great way to stay connected, but it can indeed be challenging to replicate the feeling of physical presence. Have you considered joining online support groups or seeking professional counseling? They might offer a more structured and supportive environment.
来访者：I haven't really considered it, but it seems like a good idea. Maybe talking to others who have experienced similar losses can help me feel less alone.
咨询师：Absolutely. Online support groups can provide a safe space to connect with others who understand your experience and share advice for coping with grief. It's a wonderful way to find community and support during this difficult time.
```

**response（来访当前句）**

```text
I'll definitely look into that. Thank you for the suggestion. Do you have any other tips for coping with grief and moving forward?
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-55. `extes_10044_2` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away after battling a long-term illness. I'm struggling with grief and finding it hard to come to terms with the loss. I feel overwhelmed and unsure of how to navigate my emotions during this difficult time.
- **binary_label**：合作

**context**

```text
来访者：Hey, do you have a minute? I could really use someone to talk to right now.
咨询师：Of course, I'm here for you. What's been going on?
来访者：I recently lost my uncle, and it's been really tough. I can't stop thinking about him, and I feel so overwhelmed with grief.
咨询师：I'm so sorry for your loss. Losing a loved one is deeply painful, and it's okay to feel overwhelmed with grief. Allow yourself to experience and express your emotions.
```

**response（来访当前句）**

```text
Thank you. I just wish I could find a way to cope with this sadness.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-56. `extes_2237_6` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My cousin recently lost her mother to a long battle with an illness. She's struggling to cope with the loss and is finding it hard to navigate her daily life without her.
- **binary_label**：合作

**context**

```text
来访者：She's feeling lost and empty. She's constantly crying and feels like a part of her is missing. It's affecting her ability to concentrate and she's having trouble finding motivation to do anything.
咨询师：That sounds really tough. It's completely understandable for her to feel that way after losing someone so important in her life. It's okay for her to take time to grieve and process her emotions.
来访者：I wish I could do more to help her. I hate seeing her like this.
咨询师：You're such a caring person, and your support means a lot to her. Sometimes just being there to listen and offer comfort can be the most valuable thing you can do. She'll appreciate your presence.
来访者：I hope so, but I feel like I don't know what to say or do. I've never been through this before.
咨询师：It's completely normal to feel uncertain in this situation. Maybe you could ask her how she would like to be supported or if there's anything specific she needs during this difficult time. Your willingness to listen and provide a safe space is already a big help.
```

**response（来访当前句）**

```text
That's a good idea. I'll reach out to her and let her know that I'm here for her, no matter what. Thanks for the suggestion.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-57. `extes_329_5` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My best friend recently lost her mother and she's finding it really hard to cope with the grief. She feels lost and overwhelmed by the emotions. I want to support her through this difficult time.
- **binary_label**：合作

**context**

```text
来访者：I'm doing my best to be there for her, but sometimes I'm not sure if I'm saying or doing the right things. I just want to support her through this, you know?
咨询师：Absolutely, it's understandable to feel unsure about how to best support someone who is grieving. It's important to remember that just being there for her and allowing her to express her feelings can make a significant difference. Have you had a chance to listen to her and let her share her thoughts and emotions?
来访者：Yes, I've been trying to provide a listening ear and let her know that I'm here for her. I've also been encouraging her to talk about her mom and share happy memories. It's just hard to see her in so much pain.
咨询师：It really is heartbreaking to witness someone you care about going through such a challenging time. Your support and encouragement mean a lot to her, even if it might not feel like it at times. Is there anything she specifically mentioned that is causing her additional distress?
来访者：She's mentioned feeling guilty about things she didn't say or do before her mom passed. She wishes she could have spent more time with her and expressed her love more often. It's eating her up inside.
咨询师：Guilt is a common emotion that arises during the grieving process, and it's important to validate her feelings. Let her know that it's normal to have those thoughts and feelings, but also reassure her that she was a loving and supportive presence in her mom's life. Encourage her to focus on the positive memories and the love they shared.
```

**response（来访当前句）**

```text
That's a good point. I'll make sure to remind her of all the wonderful moments she shared with her mom. I guess reminding her of the love they had for each other could help ease some of that guilt.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-58. `extes_10031_3` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away, and I am struggling to cope with the loss. I feel overwhelmed and don't know how to navigate my emotions.
- **binary_label**：合作

**context**

```text
来访者：Hi there.
咨询师：Hello, how are you doing today?
来访者：Honestly, not great. My uncle passed away recently, and I'm having a really hard time.
咨询师：I'm sorry to hear that. It sounds like you're going through a challenging time. How have you been coping so far?
来访者：I've been feeling very overwhelmed and don't know how to process my emotions. I cry a lot and sometimes don't want to talk to anyone.
咨询师：It's completely normal to feel overwhelmed and find it difficult to express your emotions when dealing with the loss of a loved one. Grieving is a complex process, and everyone copes differently. Is there anything specific that you find comforting or that helps you feel supported?
```

**response（来访当前句）**

```text
I find solace in looking at old photographs and writing in a journal. But there are times when I just want to be alone.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-59. `extes_1315_7` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away from a sudden heart attack, and I'm struggling to cope with the loss. He was like a second father to me, and I feel lost without his guidance and support.
- **binary_label**：合作

**context**

```text
来访者：I like the idea of honoring his memory. I have so many memories with him that I want to cherish.
咨询师：That's a beautiful sentiment. Cherishing the memories you shared with him is a wonderful way to pay tribute to his life. It's important to allow yourself to grieve and remember him in your own way.
来访者：I just feel so overwhelmed by all the emotions. It's like a rollercoaster of sadness, anger, and even guilt for not spending more time with him.
咨询师：It's completely normal to experience a wide range of emotions while grieving. Remember that there is no right or wrong way to feel. It's important to be gentle with yourself and allow yourself to process these emotions.
来访者：Thank you for reminding me that it's okay to feel this way. Sometimes, I worry that I'm not grieving 'correctly'.
咨询师：You're doing a great job by acknowledging and expressing your emotions. There is no 'correct' way to grieve, and it's important to honor your unique journey through this process. Your feelings are valid, and you're doing the best you can.
```

**response（来访当前句）**

```text
I just feel so alone without him. He was always there for me.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-60. `extes_10529_2` — 合作 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My cousin recently passed away due to a sudden illness, and I'm struggling to come to terms with the loss. I feel a profound sense of sadness and emptiness, and I don't know how to begin healing.
- **binary_label**：合作

**context**

```text
来访者：Hi there.
咨询师：Hello, how are you?
来访者：To be honest, I'm not doing well. My cousin just passed away unexpectedly and it's been really hard for me. I don't know how to cope with this loss.
咨询师：I'm so sorry to hear about your loss. Losing a loved one can be incredibly difficult, especially when it happens suddenly. How are you feeling right now?
```

**response（来访当前句）**

```text
I feel overwhelmed with sadness and emptiness. It's like a part of me is missing now that my cousin is gone. I don't know where to begin healing or how to move forward.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的回应
```

---

### A-61. `extes_10390_4` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long illness and I'm struggling with the grief.
- **binary_label**：合作

**context**

```text
来访者：Thank you. It just feels so empty and quiet at home without her. I keep expecting her to come running to the door when I get back, but she's not there anymore.
咨询师：I can imagine how much you miss her comforting presence. The bond between a dog and their owner can be incredibly strong, and it's natural to feel the emptiness when that connection is suddenly gone. The routines you had with her must have left a lasting impact on your daily life as well.
来访者：Yes, it's like she was a constant source of love and joy in my life. Now, everything feels different and I'm not sure how to adjust.
咨询师：Adjusting to life without her will take time and it's okay to feel unsure about it. One way you can honor her memory is by focusing on the love and joy she brought into your life. Maybe you can create a special space with her favorite toys or photographs, as a way to still keep her presence in your home.
来访者：That's actually a wonderful idea. I have some beautiful pictures of her and setting up a little memorial space would be a lovely way to remember her. It might also help bring some comfort during this difficult adjustment.
咨询师：I'm glad you find the idea helpful. Creating a memorial space with her pictures and toys will not only honor her memory, but it can also bring you a sense of connection and comfort. Remember, these grieving processes take time, but gradually, you'll be able to cherish the happy memories and find solace in knowing that you gave her a loving home. If there's anything else I can do to support you, please don't hesitate to let me know.
```

**response（来访当前句）**

```text
Thank you for saying that. I appreciate your support and understanding. It helps to have someone who gets how much losing a pet can hurt. I'll definitely consider the memorial space idea, it sounds like exactly what I need right now.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-62. `extes_1992_4` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：I recently lost my dog due to old age and it's been really tough for me.
- **binary_label**：合作

**context**

```text
来访者：It truly is. He was like a family member to me.
咨询师：Losing a pet who's been a part of your family can feel like losing a close friend. I remember when my childhood dog passed away, and the void it left in our home was really hard to fill.
来访者：Yes, the house feels so empty without him.
咨询师：It's completely normal to feel that way. Your dog brought so much joy and companionship to your life, and adjusting to his absence will take time.
来访者：I keep questioning if I did enough to make his last days comfortable.
咨询师：It's common to feel guilty and question ourselves when our pets pass away. But please remember that you gave him a loving home and provided him with a happy life.
```

**response（来访当前句）**

```text
He deserves the best. I just miss him lying by my side.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的行为表现
```

---

### A-63. `extes_10597_10` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long battle with illness
- **binary_label**：合作

**context**

```text
来访者：You're right, I did give him a good life. I need to hold on to the happy memories we shared.
咨询师：Absolutely! Cherish the moments of joy and happiness you had together. Those memories will always be a part of you, and they will help you heal with time.
来访者：Thank you for your support. It means a lot to me.
咨询师：I'm here to support you through this tough time. Remember, healing takes time, and it's okay to take it one day at a time. If you ever need someone to talk to or just to listen, I'm here for you.
来访者：Thank you so much. It really helps knowing I have someone to turn to.
咨询师：Of course! When you're ready, consider engaging in self-care activities that have brought you comfort in the past. Taking walks, writing in a journal, or maybe even creating a photo album to honor your dog's memory could bring you some solace during this difficult period.
```

**response（来访当前句）**

```text
I will definitely consider those suggestions. Thank you.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-64. `extes_1114_1` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog recently passed away and I'm having a hard time coping with the loss. He was my best friend for 12 years and I feel a profound sense of emptiness without him by my side.
- **binary_label**：合作

**context**

```text
咨询师：Hi there, how are you doing today?
来访者：Not so great. My dog passed away recently and I'm really struggling to cope with it. He meant the world to me and now there's just this void. It's so hard.
咨询师：I'm really sorry to hear about the loss of your beloved dog. Losing a pet can be incredibly difficult and painful. Dogs hold such a special place in our hearts, and it's clear that your dog was an important part of your life. It's completely natural to feel a deep sense of emptiness and sadness without your furry friend. Can you tell me more about your dog and the bond you shared?
```

**response（来访当前句）**

```text
Thank you for understanding. My dog was the sweetest and most loving companion I could have asked for. We spent countless hours playing fetch in the park and he always knew how to cheer me up when I was feeling down. He was there for me through thick and thin, and now that he's gone, everything just feels so different.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-65. `extes_5096_0` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long battle with illness
- **binary_label**：合作

**context**

```text
咨询师：Hey, how are you doing today?
```

**response（来访当前句）**

```text
I've been feeling really down. My dog passed away yesterday after a long battle with illness, and I'm heartbroken.
```

**raw_output（若有，节选）**

```text
合作

## 心理咨询对话：
###
```

---

### A-66. `extes_1052_9` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away suddenly
- **binary_label**：合作

**context**

```text
来访者：I will definitely consider reaching out to others who have gone through a similar experience. It might help to hear their perspectives.
咨询师：That's a great idea. Many pet owners go through this process of grief, and by connecting with others who have experienced a similar loss, you may find solace and understanding. We all handle loss differently, but sharing stories and memories can often bring a sense of healing.
来访者：I will try to find that healing. Thank you for being there for me through this difficult time.
咨询师：Of course, I'm here to provide support whenever you need it. Remember to take care of yourself during this time of healing. Engaging in self-care activities that bring you comfort and calmness can be beneficial as you navigate through your grief.
来访者：I'll do my best to take care of myself. Thanks again for listening and understanding.
咨询师：You're very welcome! Never hesitate to reach out if you need someone to talk to or if you're seeking additional support. Wishing you strength and peace as you remember your beloved dog. Take care!
```

**response（来访当前句）**

```text
Thank you so much. Your kind words mean a lot. Take care too!
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-67. `extes_1405_2` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away
- **binary_label**：合作

**context**

```text
咨询师：Hi, how are you doing today?
来访者：I'm feeling really down. My dog passed away last week and I miss him so much. He was my best friend.
咨询师：I'm so sorry for your loss. Losing a pet can be incredibly tough, especially when they were such an important part of your life. How long did you have your dog?
来访者：Thank you for understanding. I had him for 12 amazing years, and I'm really struggling without him by my side.
咨询师：It's completely normal to feel empty and lost when you lose a beloved pet who's been with you for such a long time. They become a part of our daily routines, and their absence can be hard to bear.
```

**response（来访当前句）**

```text
That's exactly how I feel. I keep expecting him to come wagging his tail when I come home, but he's not there. It's so hard to accept that he's gone.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-68. `extes_9913_1` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long battle with illness
- **binary_label**：合作

**context**

```text
咨询师：Hey there! How are you doing today?
来访者：I'm feeling really down. My dog passed away last night after a long battle with illness. I can't stop thinking about her and I miss her so much.
咨询师：Oh, that's heart-wrenching to hear. Losing a loyal companion like a dog can be incredibly difficult, especially after watching them fight an illness. It's completely normal to feel overwhelmed with grief and miss their presence. How are you coping with this loss?
```

**response（来访当前句）**

```text
I feel devastated. She was more than just a pet; she was a part of my family. I haven't been able to sleep and I constantly see glimpses of her around the house. I can't help but blame myself for not being able to save her.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
阻抗
阻
```

---

### A-69. `extes_2017_8` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away suddenly
- **binary_label**：合作

**context**

```text
来访者：Thank you. Honestly, just having someone to talk to and listen to me helps a lot. It's comforting to know that my feelings are valid, and others have experienced this kind of loss too.
咨询师：You're not alone, and your grief is completely valid. Remember, it takes time to heal from such a loss, so be patient with yourself. You're doing great by expressing your emotions and seeking support.
来访者：I appreciate your kind words. It's hard to imagine a life without Max, but I'll always cherish the memories and love he brought into my life.
咨询师：Of course, and as time goes on, those memories will bring a smile to your face instead of tears. Whenever you feel ready, there are also different ways to honor Max's memory. Maybe writing a journal or creating a photo album dedicated to him could be therapeutic.
来访者：That's a wonderful idea. I'll definitely consider those options. Thank you for your genuine kindness and compassion. It means the world to me.
咨询师：You're more than welcome. Take as much time as you need to heal, and know that Max will always remain in your heart. Sending you virtual hugs and support during this difficult time.
```

**response（来访当前句）**

```text
Thank you so much. It's comforting to know that there are people like you who understand the bond between a pet and their owner. Goodbye.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-70. `extes_1417_8` — 合作 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：I recently lost my beloved dog
- **binary_label**：合作

**context**

```text
来访者：Thank you, that means a lot to hear. I just can't shake off these feelings of guilt.
咨询师：Guilt is a natural part of the grieving process, and it can take time to work through it. Remember that your love for Max was unquestionable, and sometimes, things happen that are beyond our control. It's important to let go of blame and focus on the happy memories you created together. Is there something else you'd like to ask or share?
来访者：I've been thinking about how to honor Max's memory. Do you have any suggestions on how I could do that?
咨询师：Honoring Max's memory is a wonderful way to keep his legacy alive. Some people create a memorial, perhaps through planting a tree in his honor or making a donation to an animal shelter. Others choose to create a photo album filled with all the special moments they shared with their pet. The important thing is to do something that feels meaningful to you. Is there a particular suggestion that resonates with you?
来访者：I really like the idea of creating a photo album. I have so many pictures of Max, and it would be a beautiful way to remember all the joy he brought into my life.
咨询师：That's a wonderful idea! A photo album will allow you to flip through the pages and see all the happy moments you shared with Max. It will be a treasure of memories that you can hold onto forever. Max will always be a part of your life, and this album will be a beautiful tribute to his time with you.
```

**response（来访当前句）**

```text
Thank you, your words mean a lot to me. It's helpful to have someone who understands and supports me during this difficult time.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-71. `extes_2526_5` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately. I lost my job a few months ago, and I'm struggling to find another one. It's making me feel worthless and hopeless.
- **binary_label**：合作

**context**

```text
来访者：I've been applying to numerous job postings every day, but I haven't received many responses. It's disheartening because I put so much effort into each application. I also feel discouraged when I see other people getting hired before me. It feels like I'm just not good enough.
咨询师：It sounds like you've been putting a lot of effort into your job search, and it's disheartening not to receive many responses. Rejection and seeing others succeed can definitely take a toll on your self-esteem. Have you considered seeking feedback on your applications or reaching out to professional networks for support?
来访者：I haven't really sought feedback because I'm scared of hearing more negative things. It takes a toll on my confidence. And I don't have a strong professional network to rely on. It feels like I'm doing this alone.
咨询师：I understand your fear of receiving negative feedback and feeling like you're going through this alone. It's completely normal to feel that way. Remember, though, that feedback can be valuable for improvement. There might be areas you can work on that could increase your chances of securing a job. And don't discount the power of reaching out to others. Are there any online job communities or support groups you could join to connect with professionals in your field?
来访者：I haven't really looked into that, but it's worth considering. Maybe hearing from others who are going through similar experiences would help me feel less alone.
咨询师：Absolutely! Joining online communities or support groups can provide a sense of belonging and valuable insights from people who can relate to what you're going through. Remember, job searching can be a challenging process, but it's important not to lose hope. Opportunities can arise unexpectedly, and you have valuable skills to offer. Is there any particular industry or sector you're interested in? Exploring different avenues or considering temporary work can also open up new possibilities.
```

**response（来访当前句）**

```text
I've primarily been looking for jobs in marketing, but I could consider branching out or exploring temporary work. It's just hard to stay positive sometimes. I appreciate your support and advice.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-72. `extes_11102_2` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：Lately, I've been feeling extremely exhausted and unmotivated. I wake up every day with a heavy heart, and it's affecting my ability to work and enjoy life. I feel like I'm stuck in a constant state of sadness.
- **binary_label**：合作

**context**

```text
来访者：Hey
咨询师：Hi! How are you feeling today?
来访者：Honestly, not great. I've been feeling so drained and empty. It's becoming increasingly difficult to find any joy or motivation in my daily life.
咨询师：I understand how overwhelming it can be to feel drained and empty. Your emotions are valid, and I'm here to listen. Can you talk more about what's been happening?
```

**response（来访当前句）**

```text
I've been struggling with persistently negative thoughts about myself and my abilities. It feels like every day is a constant battle, and I can't seem to break free from this cycle of sadness and self-doubt.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-73. `extes_2419_7` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：Lately, I've been feeling really down and struggling to find motivation to do anything. I recently went through a breakup and it has been really tough for me. I'm having a hard time moving on and letting go of the past.
- **binary_label**：合作

**context**

```text
来访者：You're right, maybe I should give it a try. But it's difficult to stop focusing on the negative and start thinking more positively.
咨询师：I understand. Negative thoughts can become overwhelming, especially during a breakup. One way to challenge those negative thoughts is by consciously focusing on the positives in your life. Are there any things or activities that bring you joy or make you feel good, even on the smallest scale?
来访者：Well, I do enjoy going for walks in nature. It gives me a sense of peace and helps clear my mind.
咨询师：That's wonderful! Going for walks in nature can be incredibly therapeutic. It's a chance to connect with yourself and find some peace amidst the chaos. I encourage you to dedicate some time each day for this activity, if possible, to prioritize your well-being. Is there anything else you enjoy doing or would like to try?
来访者：I used to love playing the guitar, but I haven't picked it up in a while. Maybe I should start practicing again.
咨询师：Absolutely! Playing the guitar can be such a joyful and creative outlet. It's a wonderful way to channel your emotions and find solace. I highly encourage you to start practicing again and see how it positively impacts your mood. Let me know how it goes!
```

**response（来访当前句）**

```text
Thank you for listening and offering your support. It means a lot to me.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-74. `extes_196_7` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately. My job has been really stressful and I'm not enjoying it anymore. It's causing me to question my career choices and feel hopeless.
- **binary_label**：合作

**context**

```text
来访者：I haven't thought about that, but it could be helpful to get a different perspective on my career options and how I'm feeling. I'll look into it.
咨询师：That sounds like a good plan. Remember, seeking help isn't a sign of weakness, but rather a proactive step towards taking care of yourself. It's important to explore different options and find what truly aligns with your passion and values. Is there anything else that's been weighing on your mind lately?
来访者：Actually, I've been finding it hard to find motivation for anything outside of work too. I used to have hobbies that brought me joy, but now I just feel empty and unmotivated to do anything.
咨询师：I completely understand how it feels to lose motivation for things you used to enjoy. It can be really disheartening. It might be helpful to start small and engage in activities that used to bring you joy, even if it feels difficult at first. Finding balance and rediscovering your interests can support your overall well-being. Have you tried doing any small activities to see if they bring back any spark?
来访者：I haven't really tried, to be honest. It's been hard to find that motivation, but maybe I should take your advice and give it a shot. Taking small steps might lead to feeling better overall.
咨询师：Absolutely. Remember, progress often happens gradually. Starting with even just a few minutes a day dedicated to an activity you used to enjoy can make a difference. It's important to be patient with yourself throughout this process. If you're open to it, I can suggest a few hobbies that have brought joy to others in similar situations. Would you like some ideas?
```

**response（来访当前句）**

```text
Sure, that would be great. Some suggestions might help to spark some inspiration.
```

**raw_output（若有，节选）**

```text
合作

# 提示
合作行为包括积
```

---

### A-75. `extes_11099_5` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately. My long-term relationship just ended and I'm struggling to cope with the loss.
- **binary_label**：合作

**context**

```text
来访者：We'd been together for seven years and it was a shock when my partner told me they wanted to break up. It feels like my whole world has been turned upside down and I don't know how to move on from this.
咨询师：I can only imagine how devastating and disorienting this must be for you. Ending a long-term relationship can leave us feeling lost and unsure of what comes next. It's completely valid to feel a mixture of grief, sadness, anger, or confusion. Have you been able to talk to anyone about it?
来访者：I've been talking to some friends, but it feels like they just keep saying I'll find someone better or that time will heal everything. I know they mean well, but it's not making me feel any better.
咨询师：I can understand how frustrating it must be to hear those generic responses when you're in so much pain. It sounds like you need more than just those empty reassurances. Can you share what you've been finding most challenging?
来访者：One of the hardest parts is trying to adjust to not having my partner as my go-to person anymore. They were my best friend and the one I relied on for support. Now I feel like I have an emptiness that I don't know how to fill.
咨询师：That must feel incredibly lonely and disheartening. Losing not just your partner but also your closest confidant can leave a significant void in your life. Have you considered seeking additional support, such as therapy or support groups focused on coping with breakups and adjusting to life afterwards?
```

**response（来访当前句）**

```text
I haven't really thought about it, but maybe that's something I should consider. I just don't know where to start or if it'll even help.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-76. `extes_2510_2` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately because of the ongoing pandemic. I've lost my job and I'm struggling to find motivation and purpose in my daily life. It feels like everything is falling apart and I don't know how to pick myself up.
- **binary_label**：合作

**context**

```text
来访者：Hey
咨询师：Hi there! How are you doing today?
来访者：To be honest, I've been feeling really down and lost. The ongoing pandemic has caused me to lose my job, and now I'm struggling to find purpose in my life.
咨询师：I can understand how challenging it must be to face all those sudden changes. Losing a job can be overwhelming and it's normal to feel lost and uncertain about the future.
```

**response（来访当前句）**

```text
Yeah, it's been really tough. I used to have a routine and a sense of purpose with my job, and now I feel like I'm just floating through life without any direction.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-77. `extes_2523_8` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：Lately, I've been feeling really down and unmotivated. I've lost interest in things I used to enjoy and it's starting to affect my overall mood and well-being. The constant feeling of sadness is really overwhelming and I'm not sure how to deal with it.
- **binary_label**：合作

**context**

```text
来访者：Thank you for your kind words. It really means a lot to me. Sometimes, it feels like no one understands or cares, so it's comforting to know that there are people like you who genuinely want to help.
咨询师：You're not alone in this, and your feelings are valid. Many people struggle with depression and low mood, and seeking support is an important step towards healing. Remember to be kind to yourself during this challenging time and reach out whenever you need someone to talk to.
来访者：Thank you for reminding me of that. I'll do my best to take care of myself and reach out when I need someone to lean on. It's a long journey, but I'm hopeful that I'll find my way back to happiness.
咨询师：That's great to hear! Taking care of yourself is crucial, especially when facing depression and low mood. Is there anything specific you find comforting or enjoy doing? It could be something as simple as listening to music or reading a book. Incorporating small self-care practices into your day can make a big difference.
来访者：I find comfort in listening to music and journaling. It helps me express my emotions and escape from the negative thoughts for a while. I'll try to make more time for these activities and prioritize my well-being.
咨询师：That's a wonderful idea! Music and journaling can be incredibly therapeutic. Remember to be gentle with yourself and celebrate even the small victories along the way. You're doing an amazing job in taking steps towards finding your happiness again.
```

**response（来访当前句）**

```text
Thank you so much for your support and encouragement. It really means a lot to me. I feel a bit better after talking to you.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-78. `extes_2159_3` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I'm a college student going through a phase of low mood, struggling with feelings of sadness and lack of motivation.
- **binary_label**：合作

**context**

```text
来访者：Hey
咨询师：Hi there! How are you feeling today?
来访者：Hey, I'm not doing so great. Lately, I've been feeling really down and everything feels like a chore.
咨询师：I understand how tough it can be when tasks that used to bring you joy now feel like a burden. Can you share what might be contributing to these feelings?
来访者：I think part of it is the pressure of college and trying to keep up with all my responsibilities. It's overwhelming and I feel like I can't catch a break.
咨询师：College can definitely be challenging, and managing all the responsibilities can sometimes feel daunting. Are you finding it difficult to balance your academic workload with your personal life?
```

**response（来访当前句）**

```text
Yes, exactly! I spend so much time studying and working on assignments that I hardly have any time for myself or to relax.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-79. `extes_1894_4` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I'm a university student going through a phase of low mood, struggling with feelings of sadness and hopelessness.
- **binary_label**：合作

**context**

```text
来访者：Hi, I'm not feeling too great. I've been feeling really down lately, and it's hard to find any motivation for my studies.
咨询师：I understand how tough it can be when everything feels overwhelming, and finding motivation seems impossible. Can you tell me what might be contributing to these feelings?
来访者：I've been struggling with keeping up with my assignments and the pressure of maintaining good grades. It feels like I'm constantly falling behind, and I can't shake this overwhelming sadness.
咨询师：I can imagine how challenging it must be to manage the workload and expectations of university while dealing with a heavy-hearted feeling. Have you reached out to your friends or a counselor for support?
来访者：I haven't really talked to anyone about it. I feel like I don't want to burden my friends or family with my problems. And it's difficult to find the right words to explain how I'm feeling.
咨询师：I completely understand your concern about burdening others, but remember, good friends and family members are there to support you during tough times. You can have an open conversation with them about what you're going through and how they can support you through this tough phase.
```

**response（来访当前句）**

```text
You're right, I shouldn't keep it all inside. I'll try to open up to my close friends. But sometimes, it just feels impossible to see any light at the end of the tunnel. It's hard to find hope for the future.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-80. `extes_197_5` — 合作 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately because I failed an important exam.
- **binary_label**：合作

**context**

```text
来访者：I failed this really important exam, and I had put so much effort into studying for it. I feel like a failure.
咨询师：I can understand how frustrating and disheartening it must be to fail after putting in all that effort. It's completely normal to feel this way. Remember that one exam doesn't define your worth, and you have many other strengths.
来访者：I know, but it's hard not to feel disappointed in myself. I really wanted to do well.
咨询师：It's completely understandable to feel disappointed. Give yourself some time to process these emotions, but try not to be too hard on yourself. Remember that setbacks are a part of life, and it's important to learn from them and keep moving forward.
来访者：I guess you're right. I just need to figure out how to bounce back from this.
咨询师：Exactly! It's great that you're already thinking about how to move forward. Have you thought about seeking additional support or resources, like talking to your professor about your performance or seeking tutoring for the subject?
```

**response（来访当前句）**

```text
I haven't thought about talking to my professor or getting tutoring, but it's definitely worth considering. Maybe they can offer some guidance or help me improve my understanding of the material.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-81. `extes_10655_1` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently had to take a pay cut at work due to company-wide financial struggles. I'm feeling stressed and worried about how to manage my expenses.
- **binary_label**：合作

**context**

```text
来访者：Hey, how's it going?
咨询师：Hi there! I'm doing well, thanks for asking. How about you?
```

**response（来访当前句）**

```text
I've been better, to be honest. I recently had to take a pay cut at work and I'm feeling really overwhelmed trying to figure out how to make ends meet.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-82. `extes_2067_1` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I want to start a business, but I'm struggling with financial worries and uncertainty. I have a great idea, but I'm not sure if it will be successful, and I don't have enough money to invest in it.
- **binary_label**：合作

**context**

```text
来访者：Hey, how's it going?
咨询师：Hey there! I'm doing well, thank you. How about you?
```

**response（来访当前句）**

```text
To be honest, I'm feeling a bit stressed. I have this great business idea, but I don't have enough money to invest in it. Plus, I'm not sure if it will be successful.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-83. `extes_11005_4` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I'm struggling to pay my rent. I've been feeling really stressed and overwhelmed. The landlord is demanding the rent by the end of the week, but I don't have the funds. I'm not sure how to handle this situation and I'm afraid of being evicted.
- **binary_label**：合作

**context**

```text
来访者：Thank you, I really appreciate that. It feels good to know that someone understands what I'm going through. I'm just worried about being evicted if I can't pay the rent.
咨询师：I completely understand your concerns. The fear of being evicted is definitely valid in this situation. However, it's important to know that eviction processes vary depending on local laws and regulations. There may be resources available to help you navigate through this difficult time. Stay positive and let's explore some potential solutions.
来访者：It's just really tough right now. I've been looking for jobs, but nothing has come up yet. I feel so helpless.
咨询师：I understand how discouraging it can feel when job hunting is challenging. However, it's essential to remind yourself that you have valuable skills and experiences to offer. The right opportunity will come along. While you continue to search, let's explore some potential options to help you with your rent.
来访者：That would be great. I'm open to any suggestions. I just need to find a way to pay my rent by the end of the week.
咨询师：One option you can consider is reaching out to your landlord and explaining the situation. Some landlords may be open to negotiating a temporary rent reduction or a payment plan. It's worth a try to see if they can offer any flexibility. Additionally, you can search for local assistance programs that provide financial aid for individuals facing difficulties like yours. These programs may have resources to help you through this challenging time.
```

**response（来访当前句）**

```text
I guess it's worth a shot to talk to my landlord. I'll try and see if they are willing to work something out. As for assistance programs, I'm not sure where to start looking.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-84. `extes_674_6` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I'm struggling to make ends meet. I'm feeling anxious and overwhelmed about my financial situation and I don't know how to handle it.
- **binary_label**：合作

**context**

```text
来访者：I haven't really tried any stress-relief activities, but I'm definitely willing to give it a shot. Do you have any recommendations?
咨询师：Absolutely! Here are a few stress-relief activities you can try: deep breathing exercises, taking short walks outside, practicing meditation or mindfulness, or engaging in hobbies you enjoy. These activities can help you relax and clear your mind.
来访者：Those sound like great suggestions. I'll definitely give them a try. I just hope I can find some stability soon. It's been really hard to deal with the uncertainty of not having a job.
咨询师：I completely understand how challenging the uncertainty can be. It's normal to feel that way when you're dealing with a situation like this. Many people go through economic hardships, and although it feels tough right now, it's important to remember that things can and will get better.
来访者：Thank you for reminding me of that. It's nice to have someone to talk to and receive some reassurance. Is there anything else you can suggest to help me during this difficult time?
咨询师：One option you could explore is reaching out to local resources or organizations that provide assistance for individuals facing financial difficulties. They may be able to offer guidance, support, or even job opportunities. Additionally, consider creating a budget to help manage your finances more effectively. It can give you a clearer picture of your financial situation and help you plan for the future.
```

**response（来访当前句）**

```text
Those are really helpful suggestions. I'll definitely look into local resources and start budgeting. It feels good to have a plan in place. Thank you so much for your support and advice.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-85. `extes_9061_2` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：Due to unexpected medical expenses, I am struggling to pay bills and provide for my family. I feel overwhelmed and unsure about how to handle the situation.
- **binary_label**：合作

**context**

```text
来访者：Hey there, how are you doing today?
咨询师：Hi! I'm here to listen and support you. What's been going on?
来访者：I've been feeling really stressed lately. Some unexpected medical bills came up, and now I'm struggling to make ends meet. It feels like I can't provide for my family like I want to.
咨询师：I can understand how difficult that must be for you. Financial worries can certainly be overwhelming. It's normal to feel stressed in such situations. You're doing your best to support your family.
```

**response（来访当前句）**

```text
Thank you, I appreciate your understanding. I just wish I had a better plan or solution.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-86. `extes_4895_2` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently got laid off from my job and I'm struggling to pay my monthly bills. On top of that, I have no idea when I'll find a new job.
- **binary_label**：合作

**context**

```text
来访者：Hey, how's it going?
咨询师：Hi there! How are you today?
来访者：To be honest, not great. I lost my job a few weeks ago and it's been really tough.
咨询师：I'm really sorry to hear that. Losing a job can be incredibly stressful and challenging. How have you been holding up?
```

**response（来访当前句）**

```text
It's been really rough. I feel so overwhelmed with financial worries and not knowing when I'll find a new job
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-87. `extes_10667_4` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently had unexpected medical expenses and I'm struggling to keep up with my bills. I feel overwhelmed and stressed about my financial situation.
- **binary_label**：合作

**context**

```text
来访者：Honestly, I'm not doing so well. I've been really stressed out about my finances ever since I had those unexpected medical expenses. It's been really tough to pay my bills on time and I'm not sure what to do.
咨询师：I can understand why you would feel stressed in this situation. It must be overwhelming to deal with unexpected expenses and the pressure to meet your financial obligations. I'm here to listen and support you.
来访者：Thank you, I appreciate that. It's just been really hard to stay positive when I feel like I'm drowning in bills.
咨询师：I hear you, and I want you to know that your feelings are completely valid. It's understandable to feel overwhelmed and uncertain when facing financial difficulties. Is there anything specific that's causing you the most stress?
来访者：One of the biggest concerns is that I won't be able to afford my rent next month. I'm worried about getting evicted if I can't come up with the money.
咨询师：That sounds incredibly stressful. It's completely normal to worry about having a roof over your head. Have you considered reaching out to organizations or community resources that may be able to provide assistance or guidance? They could potentially help you find solutions or connect you with local programs.
```

**response（来访当前句）**

```text
I haven't really thought about that, but it's definitely worth looking into. I just want to make sure I have a place to live and not be constantly worried about being homeless.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-88. `extes_10989_5` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I'm struggling to pay my bills. I'm feeling overwhelmed and unsure about the future.
- **binary_label**：合作

**context**

```text
来访者：I've been applying to jobs like crazy, but haven't had any luck so far. It feels like I'm stuck in this never-ending cycle of rejections and it's really demoralizing.
咨询师：It's really disheartening to face rejection time after time. But don't lose hope. Have you considered reaching out to any professional networks or attending job fairs in your area?
来访者：I haven't thought about tapping into professional networks or attending job fairs. I guess I've been so focused on online applications that I haven't explored other options.
咨询师：Expanding your network can open up more opportunities and sometimes leads to a job referral. It's worth giving it a shot. Additionally, updating your resume and cover letter to tailor them to specific job postings might increase your chances of being noticed by employers.
来访者：That's a good idea. I'll definitely look into attending job fairs and reaching out to professional networks. And I'll review my resume and cover letter to make sure they're compelling. Thanks for the suggestions!
咨询师：You're taking proactive steps to improve your job search, and that's commendable. It's important to acknowledge how challenging this whole process can be, but remember that with each application, you're one step closer to finding the right opportunity.
```

**response（来访当前句）**

```text
I appreciate your support. It really means a lot to me. It's just hard to stay positive when I've been dealing with so many rejections.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-89. `extes_10998_2` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently had unexpected medical expenses and now I'm struggling to pay my bills. I feel stressed and overwhelmed about my financial situation.
- **binary_label**：合作

**context**

```text
来访者：Hey, how's it going?
咨询师：Hello! I'm doing well, thanks for asking. What about you? How are you doing today?
来访者：I've had better days, honestly. I'm dealing with some financial stress right now and it's really getting to me.
咨询师：I'm really sorry to hear that. Dealing with financial stress can be incredibly tough, and it's completely normal to feel overwhelmed in that situation.
```

**response（来访当前句）**

```text
Thank you, I appreciate your understanding. It just feels like this never-ending cycle of bills and expenses.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-90. `extes_11015_1` — 合作 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently had unexpected medical expenses and I'm feeling overwhelmed with financial worries. I'm struggling to pay my bills and it's causing a lot of stress in my life.
- **binary_label**：合作

**context**

```text
来访者：Hey there
咨询师：Hello! How are you doing today?
```

**response（来访当前句）**

```text
Not so great, to be honest. I've been dealing with some unexpected medical expenses and it's been really stressful.
```

**raw_output（若有，节选）**

```text
合作

## 心理咨询对话：
###
```

---

### A-91. `extes_204_8` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：My best friend has recently been diagnosed with bipolar disorder, and it's been really challenging for me to help them through it. They have been experiencing extreme mood swings and I'm worried about how it's affecting their daily life and relationships. I need some guidance on how to provide emotional support.
- **binary_label**：合作

**context**

```text
来访者：I've tried telling them that, but they still keep their distance.
咨询师：It must be hard for you to see your friend pushing you away when all you want is to be there for them.
来访者：Exactly. I just want to make sure they're okay, but it feels like they're shutting me out.
咨询师：Your concern for your friend's well-being shows how much you truly care about them. That's commendable.
来访者：Thank you, but I'm starting to question if I'm doing more harm than good.
咨询师：It might be helpful to communicate your concerns honestly with your friend and let them know that you're feeling unsure about how to best support them. Open communication can foster a deeper understanding between the two of you.
```

**response（来访当前句）**

```text
I think you're right. I'll try to have an open and honest conversation with them.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-92. `extes_382_13` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've recently been diagnosed with Bipolar Disorder and I'm struggling to come to terms with it. It's affecting my relationships with loved ones and I feel overwhelmed.
- **binary_label**：合作

**context**

```text
来访者：I haven't been prioritizing my self-care lately. I'll make an effort to incorporate those things into my life.
咨询师：That's a great step forward! Remember to be patient and kind to yourself. It's a process, and you're doing amazing.
来访者：Thank you for the reminder. I will try my best and take things one day at a time.
咨询师：That's a wonderful mindset to have. Don't hesitate to reach out if you need anything else. I'm here for you.
来访者：Thank you, I really appreciate that.
咨询师：You're welcome! Stay strong and keep advocating for your well-being. You've got this.
```

**response（来访当前句）**

```text
I'll do my best. Thank you for your support.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-93. `extes_703_4` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：My best friend has been recently diagnosed with bipolar disorder and is struggling to accept and understand their condition. They feel overwhelmed and isolated as they navigate this new reality. They are unsure how their friendships and relationships will be affected by this diagnosis.
- **binary_label**：合作

**context**

```text
来访者：Yes, that's exactly how I feel. I want to be there for them, but I'm worried I might say or do the wrong thing.
咨询师：Have you tried asking your friend about their specific needs and preferences?
来访者：I haven't yet. I didn't want to bring it up and make them feel uncomfortable.
咨询师：It's completely understandable that you want to be sensitive to their feelings. You're doing your best to approach this situation with care.
来访者：Thank you, I really appreciate that. What do you suggest I do next?
咨询师：I think an open and honest conversation with your friend could be valuable. Express your willingness to support them and let them know that you want to learn more about bipolar disorder to have a better understanding. This can help strengthen your friendship.
```

**response（来访当前句）**

```text
That's a good idea. I want them to know that I'm here for them and that they're not alone.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-94. `extes_2457_5` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have recently been diagnosed with bipolar disorder and I'm struggling to navigate my professional life while managing my symptoms. The constant mood swings and lack of focus are making it difficult for me to perform well at work and maintain healthy relationships with my colleagues. I'm feeling overwhelmed and unsure of how to handle the challenges.
- **binary_label**：合作

**context**

```text
来访者：I'm hesitant to share my condition with them. I'm afraid they might react negatively or treat me differently.
咨询师：It's completely understandable to have concerns about disclosure. It's unfortunate that stigma still exists around mental health conditions. However, disclosing your condition to someone you trust, like an understanding supervisor or HR, may provide you with the support and accommodations you need to succeed at work. Do you have a close friend or family member you can confide in about this?
来访者：Yes, my sister has always been supportive. She also has some knowledge about bipolar disorder as she has a friend who was diagnosed. I've been talking to her about it.
咨询师：That's great to hear that you have someone close to you who understands bipolar disorder. How has talking to your sister been helpful in navigating your work challenges?
来访者：She's been giving me advice on how to communicate my needs at work and has encouraged me to seek professional help. It feels good to have someone on my side.
咨询师：Having a supportive sister who can provide guidance and encouragement can make a significant difference in your journey. Remember that self-advocacy is important, and seeking professional help, like therapy or medication management, can also contribute to improving your well-being and productivity. Is there anything else on your mind?
```

**response（来访当前句）**

```text
Not at the moment. Thank you for your support and guidance. It means a lot to have someone listen and understand.
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-95. `extes_2454_5` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've recently been diagnosed with bipolar disorder, and I'm struggling to come to terms with it. It's been difficult for me to manage my emotions and maintain stability in my daily life. I often feel overwhelmed and unsure of how to navigate this new reality.
- **binary_label**：合作

**context**

```text
来访者：I've already noticed some strain in my friendships. It's hard for them to understand why I act the way I do.
咨询师：It must be tough when those close to you struggle to comprehend the complexities of bipolar disorder. Your feelings and experiences are valid, even if others may have a difficult time understanding them. Have you considered discussing your diagnosis with your friends, so they can gain more insight into your unique situation?
来访者：I haven't talked to them about it yet. I'm afraid they'll distance themselves from me or treat me differently.
咨询师：It's completely normal to feel apprehensive about sharing your diagnosis, particularly due to fears of rejection or judgment. It's important to remember that true friends will support you through thick and thin, and understanding bipolar disorder might bring you closer by fostering empathy and dialogue.
来访者：You're right. I just need the courage to open up and have those conversations. I also worry about the impact on my career.
咨询师：It sounds like you're concerned about how to navigate your career alongside managing bipolar disorder. Can you tell me more about your worries?
```

**response（来访当前句）**

```text
I fear that disclosing my condition to my employer might lead to discrimination or limitations in my professional growth. I don't want to be seen as unreliable or incapable.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
阻抗
合作
```

---

### A-96. `extes_2467_8` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have recently been diagnosed with bipolar disorder and I'm struggling to manage my symptoms. I often experience extreme mood swings and it's affecting my relationships and daily life. My romantic partner doesn't understand my condition and is finding it hard to deal with my mood swings, causing tension and distance in our relationship.
- **binary_label**：合作

**context**

```text
来访者：That's a good idea. I'll look into finding some resources that can help my partner understand bipolar disorder better.
咨询师：In addition, have you considered couples therapy? A trained therapist can provide a safe space for both you and your partner to express yourselves and work on improving communication and understanding.
来访者：I haven't thought about couples therapy, but it might be a good option. I'll talk to my partner and see if they're open to the idea.
咨询师：Absolutely. Seeking professional guidance through couples therapy can be an opportunity to strengthen your relationship, enhance empathy, and improve your communication skills. Remember, progress takes time and effort.
来访者：You're right. I need to be patient and hopeful that we can overcome this together.
咨询师：You're not alone in facing these challenges in relationships. Many individuals with bipolar disorder experience difficulties in explaining their condition to their partners. Connecting with support groups or online communities might provide you with guidance and insights from others who have been through similar experiences.
```

**response（来访当前句）**

```text
I never considered joining a support group. It might be beneficial to hear from others who can relate.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-97. `extes_54_1` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've been feeling really overwhelmed lately. My partner doesn't understand my bipolar disorder, and it's causing a lot of strain in our relationship. I'm not sure how to communicate with them and get the support I need.
- **binary_label**：合作

**context**

```text
来访者：I've been feeling really overwhelmed lately. My partner doesn't understand my bipolar disorder, and it's causing a lot of strain in our relationship. I'm not sure how to communicate with them and get the support I need.
咨询师：It sounds like you're going through a tough time with your partner not being fully understanding of your bipolar disorder. Would you like to tell me more about how this is affecting you?
```

**response（来访当前句）**

```text
It's really frustrating because they dismiss my mood swings and emotional changes as me just being difficult. I constantly feel invalidated and it's taking a toll on my mental well-being.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-98. `extes_9075_2` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I recently found out that my teenage daughter has been diagnosed with bipolar disorder. It has been really challenging for me as a single parent to understand and support her through this. I often find myself feeling overwhelmed and unsure of what to do. I need some emotional support and guidance.
- **binary_label**：合作

**context**

```text
来访者：I don't know how to deal with my daughter's bipolar disorder. It's been really tough for me as a single parent.
咨询师：It sounds like you're going through a difficult time trying to support your daughter with her bipolar disorder. Can you tell me more about your concerns and frustrations?
来访者：I'm worried about how to handle her mood swings. They can be really intense and unpredictable. I feel like I'm constantly walking on eggshells around her.
咨询师：I can understand how that can be challenging and exhausting. It must be hard to experience such intense mood swings from your daughter, especially when you're the primary caregiver.
```

**response（来访当前句）**

```text
Yes, it's mentally and emotionally draining. I'm questioning whether I'm doing enough or if I'm failing her somehow.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-99. `extes_2204_3` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：My best friend has recently been diagnosed with bipolar disorder and they are finding it difficult to manage their symptoms. They are feeling overwhelmed and unsure of how to cope.
- **binary_label**：合作

**context**

```text
来访者：Hey, I'm really worried about my best friend. They've been recently diagnosed with bipolar disorder and it seems like they're going through a tough time.
咨询师：I can understand how concerned you must be. It can be challenging to witness someone you care about navigating the complexities of bipolar disorder. Can you tell me more about what they're experiencing?
来访者：It's been really tough for them. They experience extreme shifts in their moods and it's affecting their daily life. Sometimes they struggle to maintain stability and it's emotionally draining for both of us.
咨询师：It sounds like your best friend's mood swings are taking a significant toll on them and on your relationship. It's important to acknowledge the challenges and emotions they are facing.
来访者：Exactly. It hurts to see them going through such extreme emotions. I want to provide support, but I often feel helpless because I don't know what to do.
咨询师：It's commendable that you care so deeply and want to provide support. Remember that just being there to listen and Offer support is incredibly important. Sometimes, understanding and empathy can go a long way in helping your best friend feel heard and supported.
```

**response（来访当前句）**

```text
I've been researching about bipolar disorder to try and learn more, but it's quite complex. Sometimes it feels overwhelming to figure out how to help them manage their symptoms.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-100. `extes_2458_2` — 合作 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have been struggling with mood swings and finding it hard to maintain a healthy relationship with my partner. The constant changes in my mood are affecting our interactions and causing a lot of strain in the relationship. I need some guidance on how to cope with this situation and improve our connection.
- **binary_label**：合作

**context**

```text
来访者：I've been feeling really frustrated and overwhelmed lately because my mood swings are constantly causing conflicts in my relationship with my partner.
咨询师：It sounds like you've been dealing with a lot of frustration and overwhelm due to the impact of your mood swings on your relationship. It must be challenging for both you and your partner.
来访者：Yes, it's very challenging. I often have intense mood swings, and it's hard for my partner to understand and handle them.
咨询师：It's completely valid to feel that way. Bipolar disorder can present unique challenges, especially in relationships. Your partner may not fully understand what you're going through, but that doesn't mean they don't care.
```

**response（来访当前句）**

```text
I'm worried that my mood swings will push my partner away or become too much for them to handle.
```

**raw_output（若有，节选）**

```text
合作
阻抗
合作
阻抗
```

---

### A-101. `extes_10692_4` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and discouraged after being unemployed for several months.
- **binary_label**：合作

**context**

```text
来访者：I'm okay, but I've been feeling really down lately. It's been months since I lost my job, and I still haven't found another one. It's getting really difficult to stay positive.
咨询师：I can only imagine how frustrating and demoralizing it must be to be unemployed for such a long time. It's completely natural to feel down and overwhelmed in this situation. Can you tell me a little more about your job search experience?
来访者：Thanks for understanding. It's been incredibly difficult. I've been sending out multiple applications every day, but there's been very little response. I've had a couple of interviews, but they didn't go well.
咨询师：I can understand how disheartening that must be, putting in so much effort and not seeing the desired results. It's tough when you go through multiple rejections and setbacks. Have you considered connecting with any professional contacts for potential leads or recommendations?
来访者：Yes, I've been reaching out to former colleagues and friends, but so far, no luck. It feels like I'm hitting dead ends.
咨询师：I can hear your frustration. Sometimes it feels like there are no opportunities available, but don't lose hope. Can I ask if there's a particular industry or job role you're passionate about? Exploring different possibilities might help expand your search.
```

**response（来访当前句）**

```text
I was really enjoying my work in graphic design, but I'm open to exploring other options too. At this point, I just need something that pays the bills.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-102. `extes_185_3` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed with job searching
- **binary_label**：合作

**context**

```text
来访者：Hi there
咨询师：Hello! How are you doing today?
来访者：I'm feeling a bit stressed out actually. I've been searching for a job for months now and it seems like there are no opportunities available.
咨询师：I understand how frustrating and disheartening it can be when it feels like there are no job prospects. Would you like to talk a little more about your situation?
来访者：Yes, it's just been really tough. I've been sending out resumes and attending interviews, but nothing seems to be working out.
咨询师：It sounds like you've been putting a lot of effort into your job search. How does it make you feel when you don't see the results you're hoping for?
```

**response（来访当前句）**

```text
It's really discouraging. I start to doubt my skills and worry that I'll never find a job.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的行为是
```

---

### A-103. `extes_2379_6` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling demotivated and lost due to a lack of job prospects after completing a degree in a competitive field.
- **binary_label**：合作

**context**

```text
来访者：Yes, exactly! I'm starting to doubt if I made the right choices in my education and career path.
咨询师：I can empathize with your situation. It's natural to question your decisions when things don't go as planned. However, I want to assure you that this is just a temporary phase, and there are always opportunities waiting for you. Have you considered exploring different industries or expanding your skillset to increase your chances?
来访者：I haven't really thought about that. I've been so fixated on finding a job in my specific field that I haven't considered other options.
咨询师：It's great that you have a specific field in mind, but sometimes it takes a bit of flexibility to get your foot in the door. Have you considered looking for related roles or internships to gain experience? Additionally, acquiring new skills or certifications can make you stand out from the competition. Does that sound like something you might be open to exploring?
来访者：You're right, maybe widening my search parameters and gaining additional skills could open up more possibilities for me. I should be more open to different opportunities.
咨询师：That's a positive mindset! Being open to different possibilities often leads to unexpected opportunities. It takes courage to step outside your comfort zone, but I believe in your abilities. How do you feel about creating a plan to explore new career avenues?
```

**response（来访当前句）**

```text
I think that's a good idea. I'll start researching related roles and consider gaining new skill sets. Hopefully, this will help me find some direction.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-104. `extes_185_8` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed with job searching
- **binary_label**：合作

**context**

```text
来访者：Well, I did have one interview where they mentioned that I had great communication skills. It felt good to hear that, even if I didn't get the job.
咨询师：That's fantastic! It's a clear indication that your skills are valuable and acknowledged by employers. How can you leverage these skills and build on them in your future search?
来访者：I think I can highlight my communication skills more in my resume and cover letter. Maybe that will help me stand out to potential employers.
咨询师：That's a great plan! It shows that you're resilient and willing to adapt your approach. Remember, setbacks are a normal part of the job search process. It's all about staying positive and finding ways to improve your chances.
来访者：I'll keep that in mind. Thank you for your support and encouragement.
咨询师：You're welcome! It's important to have someone to talk to during this challenging time. Is there anything else you'd like to discuss or any other concerns you have?
```

**response（来访当前句）**

```text
Actually, I'd love to know some stress management techniques that could help me navigate through this process.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-105. `extes_2379_1` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling demotivated and lost due to a lack of job prospects after completing a degree in a competitive field.
- **binary_label**：合作

**context**

```text
来访者：Hey, how are you doing?
咨询师：Hey there! I'm doing well, thank you. How about you? What's been going on in your life?
```

**response（来访当前句）**

```text
Well, honestly, I've been feeling pretty down lately. I just graduated with a degree in a competitive field, but I can't seem to find any job prospects. It's really discouraging.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-106. `extes_2354_2` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and frustrated after multiple job rejections
- **binary_label**：合作

**context**

```text
来访者：Hey
咨询师：Hello, how are you doing today?
来访者：Hi, I'm feeling really down. I've been applying for jobs for a while now, but I keep getting rejected. It's really frustrating.
咨询师：I understand how you're feeling. Repeated rejections can be incredibly disheartening, especially when you're putting in so much effort. Tell me more about your job search experience.
```

**response（来访当前句）**

```text
It just feels like I'm not making any progress. I spend hours customizing my applications, and it's so demoralizing to receive rejection emails or no response at all.
```

**raw_output（若有，节选）**

```text
合作

# 输入
## 阻抗：
```

---

### A-107. `extes_10709_6` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed by the lack of job opportunities
- **binary_label**：合作

**context**

```text
来访者：I haven't really explored other industries yet. I guess I'm just afraid to step out of my comfort zone.
咨询师：Stepping out of your comfort zone might seem intimidating, but it could also lead to exciting new possibilities. Trying out different industries or acquiring new skills can enhance your chances of finding the right job. It can also give you a chance to discover a new passion. What do you think?
来访者：You're right, I shouldn't limit myself. I'm going to start looking into other industries and see what options are out there.
咨询师：That's a positive step forward! Remember, it's perfectly normal to feel uncertain or hesitant, but don't let that hold you back. Is there anything specific you'd like assistance with in exploring new industries?
来访者：I'm not sure where to start. Do you have any suggestions?
咨询师：A great starting point would be to research industries that interest you and match your skills. You could read industry publications, join online communities, or even reach out to professionals in those fields to gain insights and advice. Gathering information can help you in making informed decisions. How does that sound?
```

**response（来访当前句）**

```text
Reading industry publications and joining online communities sounds helpful. I'll definitely give that a try.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-108. `extes_10673_9` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and demotivated after being laid off
- **binary_label**：合作

**context**

```text
来访者：I'm feeling a bit more hopeful and motivated after talking about it. It helps to have someone to bounce ideas off of. Thank you for being there for me.
咨询师：You're welcome! Providing support and listening is what I'm here for. Remember, you're resilient and capable of overcoming challenges. Is there anything else on your mind or any other aspect of your situation that you'd like to discuss?
来访者：Actually, there is one more thing. I've been finding it hard to stay focused and productive throughout the day. Do you have any tips to boost motivation?
咨询师：Absolutely! Maintaining a routine, setting realistic goals, and creating a dedicated workspace can help cultivate focus. Also, remember to take breaks, engage in activities you enjoy, and connect with a support system. How does that sound?
来访者：Those are some great suggestions. I'll definitely work on incorporating those practices into my daily routine. Thanks for the advice!
咨询师：You're very welcome! Prioritizing self-care and incorporating these practices can make a significant difference. Remember, take things one step at a time and be kind to yourself in the process. Keep me updated on your progress, and feel free to reach out at any time if you need further support. Wishing you all the best in your journey!
```

**response（来访当前句）**

```text
Thank you so much. Your support means a lot to me. Take care and talk to you soon!
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-109. `extes_37_11` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling discouraged after multiple job rejections
- **binary_label**：合作

**context**

```text
来访者：You're right. I've been neglecting self-care lately. I'll make sure to schedule some 'me time' too.
咨询师：That's fantastic! Taking care of yourself will help maintain your overall well-being, which in turn can positively impact your job search. You're doing great, hang in there.
来访者：Thank you so much for your support. I really needed someone to talk to.
咨询师：You're welcome! I'm here for you whenever you need someone to talk to. We'll get through this together. Is there anything else you'd like to discuss?
来访者：No, that's all for now. Thanks again. This conversation has lifted my spirits a bit.
咨询师：I'm glad I could help. Remember, you're resilient and capable. Wishing you all the best in your job search. Please take care and don't hesitate to reach out if you need support in the future.
```

**response（来访当前句）**

```text
Thank you. Take care too, and see you around!
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-110. `extes_10675_6` — 合作 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and anxious after being laid off due to company downsizing
- **binary_label**：合作

**context**

```text
来访者：I've just started updating my resume, but it feels overwhelming. There are so many factors to consider, and I'm afraid my skills aren't good enough to compete in the job market.
咨询师：Updating your resume is a great first step, and congratulations on taking that initiative! It's common to have doubts about your skills, but remember that you have unique experiences that make you valuable. You have so much to offer, and I believe in your abilities. Would you like some suggestions for improving your resume and job search?
来访者：That would be really helpful! I want to make sure I stand out to potential employers. What do you suggest?
咨询师：One suggestion is to tailor your resume for each job application by highlighting relevant skills and experiences. Showing enthusiasm and passion for the field you're applying to can also make a positive impression. Additionally, consider reaching out to your network for job leads and recommendations. What do you think about these suggestions?
来访者：Those sound like great ideas! I'll definitely start customizing my resume and reach out to my contacts. It gives me some direction and hope that there are things I can do to improve my chances.
咨询师：That's wonderful to hear! Taking proactive steps can give you a sense of control amidst the uncertainty. Remember, opportunities are out there, and with determination and effort, you can find a new job that aligns with your skills and interests. How are you feeling now?
```

**response（来访当前句）**

```text
I'm feeling a bit more optimistic now. It helps to talk it out and receive practical advice. I appreciate your support.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-111. `extes_10616_5` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling very stressed and overwhelmed at work lately. I have a lot of deadlines to meet and I'm struggling to manage my time effectively. It's starting to take a toll on me mentally and physically.
- **binary_label**：合作

**context**

```text
来访者：There's just so much on my plate right now. I have multiple projects with strict deadlines, and it feels like I can't keep up. I'm constantly worried about meeting all the expectations.
咨询师：That sounds incredibly challenging. It's understandable to feel overwhelmed with such a heavy workload and high expectations. How have you been managing the stress that comes with it?
来访者：Honestly, I've been struggling. I find myself thinking about work even during my free time. It's hard to disconnect and relax.
咨询师：I can relate to that. It can be really tough to separate work from personal life, especially when work demands are so high. Have you tried any activities outside of work that help you unwind?
来访者：I used to enjoy painting, but I haven't had the time or energy for it lately. I feel guilty if I'm not constantly working.
咨询师：It's so common to feel guilty or like you're neglecting work when you try to take time for yourself. But it's important to remember that self-care is crucial for maintaining your well-being and productivity in the long run. Making time for activities you enjoy, even for a short while, can have a positive impact on your mental health.
```

**response（来访当前句）**

```text
You're right. I need to prioritize self-care and find a balance between work and personal life. Any suggestions on how I can do that?
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-112. `extes_343_13` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been experiencing work-related stress and burnout lately. It's been overwhelming and I don't know how to cope with it.
- **binary_label**：合作

**context**

```text
来访者：I appreciate your belief in me. With your assistance, I feel more optimistic about managing my work-related stress.
咨询师：I'm glad to hear that. Remember, this stressful period won't last forever. There will be brighter days ahead.
来访者：Thank you once again for your kindness. I'll put your advice into action and stay positive.
咨询师：You're welcome! Take things one step at a time and be gentle with yourself. I'm here to support you along the way. You've got this!
来访者：I really appreciate your support. It means a lot to me to have someone to talk to.
咨询师：I'm here for you whenever you need someone to talk to. Remember, you're not alone in this journey.
```

**response（来访当前句）**

```text
Thank you. It's comforting to know that someone understands and cares. I'll reach out if I need further support.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-113. `extes_10454_10` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed with my workload at work and it's affecting my mental health. I need some support and advice on how to manage this.
- **binary_label**：合作

**context**

```text
来访者：I'll try my best to incorporate those into my routine. It just feels like I'm constantly on the go. Any suggestions on how to detach from work mentally?
咨询师：To mentally detach from work, you can establish a routine that helps you transition out of work mode. It could be something as simple as going for a walk, practicing mindfulness or engaging in a hobby you enjoy. Journaling your thoughts and feelings can also be helpful.
来访者：I never thought of journaling before. I'll give it a try. Hopefully, it will give me some peace of mind.
咨询师：That's a great approach! Remember, small steps can make a big difference. Give yourself credit for taking action and seeking support. You're on the right track toward finding balance.
来访者：Thank you so much for your kindness and support. I feel a little better after talking this through.
咨询师：You're welcome! I'm here for you anytime you need to talk or if you need further guidance. You're doing great, and I believe in your ability to navigate through these challenges.
```

**response（来访当前句）**

```text
Thanks again, I truly appreciate it.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-114. `extes_10944_2` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling extremely stressed and burnt out at work. The constant pressure and long hours are taking a toll on my mental and physical well-being. It seems like I can never catch a break, and I feel overwhelmed by the increasing workload and demands.
- **binary_label**：合作

**context**

```text
来访者：Hi there, I could really use someone to talk to right now.
咨询师：Of course, I'm here to listen. What's been happening?
来访者：Lately, work has been incredibly stressful. The workload has been piling up, and I'm struggling to keep up. It feels like there's no end to it.
咨询师：That sounds tough. It must be exhausting to have such a heavy workload without any relief. How have you been coping with it?
```

**response（来访当前句）**

```text
Honestly, it's been really challenging. I feel like I'm constantly running on empty and there's never enough time to recharge. I've been neglecting my own well-being just to meet deadlines.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作的回应
```

---

### A-115. `extes_2041_11` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been experiencing work-related stress and burnout lately. I have been assigned multiple difficult projects with tight deadlines, and it's becoming overwhelming. Additionally, I have had disagreements with my colleagues, which further adds to my stress and burnout.
- **binary_label**：合作

**context**

```text
来访者：Finding a work-life balance seems challenging, but I'll try incorporating breaks and stress management activities. It's time to prioritize my well-being.
咨询师：That's an excellent mindset to have. Remember, self-care and prioritizing your well-being are essential for managing work-related stress and burnout. You deserve to feel balanced and supported.
来访者：Thank you for being so understanding and providing guidance. It really means a lot to me.
咨询师：You're welcome! I'm here for you, and I want to support you through this challenging period. Remember, you're capable of overcoming these difficulties, and I believe in you.
来访者：I appreciate your belief in me. With your assistance, I feel more optimistic about managing my work-related stress.
咨询师：I'm glad to hear that! Keep in mind that this phase won't last forever, and you have the strength to overcome it. There are brighter days ahead!
```

**response（来访当前句）**

```text
Thank you once again for your kindness. I'll implement your advice and stay positive.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-116. `extes_1777_5` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been working long hours and have been feeling extremely stressed and overwhelmed at my job as a project manager. The constant pressure and deadlines are taking a toll on my mental health.
- **binary_label**：合作

**context**

```text
来访者：I work as a project manager, and the constant pressure and deadlines are overwhelming me. It feels like I never have a moment to breathe.
咨询师：That sounds really tough. Managing projects can be highly demanding, especially when juggling multiple deadlines. How long have you been dealing with this level of stress?
来访者：I've been in this position for about a year now, and it's getting harder to handle. I feel like I'm on the verge of burning out.
咨询师：It's completely understandable that you feel exhausted and on edge. A year of continuous stress can have that effect. Have you discussed your concerns with your colleagues or supervisor?
来访者：Not really. I'm afraid opening up about the stress will make me seem incapable or unreliable.
咨询师：I understand your worries, but it's important to remember that you're not alone in experiencing the challenges of your role. Opening up about your stress may actually help your colleagues and supervisor understand your situation better. You do excellent work, and it's okay to seek support. Is there someone you trust at work that you could talk to?
```

**response（来访当前句）**

```text
Now that you mention it, I do have a coworker who seems to be supportive. Maybe I'll reach out to them.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-117. `extes_10947_9` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling extremely overwhelmed with my workload lately and I'm starting to experience signs of burnout.
- **binary_label**：合作

**context**

```text
来访者：You're right, I shouldn't neglect my well-being. I'll try talking to my supervisor and see if anything changes.
咨询师：That's a step in the right direction. Remember, addressing the issue is important and it reflects your commitment to finding a solution. How do you feel about taking this step?
来访者：Honestly, I'm nervous but hopeful. I really want to find a way to manage my workload and achieve better work-life balance.
咨询师：Change often starts with taking small steps, and expressing your concerns is definitely a positive move. I believe in your ability to find a better balance and create a healthier work environment for yourself.
来访者：Thank you so much for your support. It means a lot to me.
咨询师：You're welcome! Providing support is what I'm here for. Remember, it's okay to seek help when you need it. You're not alone.
```

**response（来访当前句）**

```text
I appreciate that. It's reassuring to know that someone understands.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作行为：来
```

---

### A-118. `extes_2059_9` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I work in a high-pressure environment and have been experiencing extreme work-related stress and burnout. I often find myself overwhelmed with my workload and struggling to maintain work-life balance.
- **binary_label**：合作

**context**

```text
来访者：I haven't given them a shot yet. It's challenging to find time for myself, but I understand the importance of self-care.
咨询师：Absolutely. Starting with small steps can make a significant difference. Even dedicating just 10 minutes a day to activities like taking a walk, listening to calming music, or practicing deep breathing can help you feel rejuvenated. Prioritizing self-care can positively impact both your mental and physical well-being.
来访者：That sounds doable. I'll definitely try to incorporate those activities into my routine. Thank you for suggesting it.
咨询师：You're welcome! Remember, change takes time, and progress may not always be linear. It's essential to be patient with yourself and embrace the small steps you take towards self-care. You have the strength to overcome this challenging phase.
来访者：Thank you for your support. I really appreciate it.
咨询师：You're welcome! Remember, I'm here for you if you need further support. Prioritize your well-being and take care of yourself.
```

**response（来访当前句）**

```text
I will. Thank you again. Goodbye!
```

**raw_output（若有，节选）**

```text
合作

# 以上是心理咨询师和
```

---

### A-119. `extes_10618_11` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed with my workload at work and it's affecting my mental health. I need some support and advice on how to manage this.
- **binary_label**：合作

**context**

```text
来访者：I never thought of journaling before. I'll give it a try. Hopefully, it will give me some peace of mind.
咨询师：That's a great approach! Remember, small steps can make a big difference. Give yourself credit for taking action and seeking support. You're on the right track toward finding balance.
来访者：Thank you so much for your kindness and support. I feel a little better after talking this through.
咨询师：You're welcome! I'm here for you anytime you need to talk or if you need further guidance. You're doing great, and I believe in your ability to navigate through these challenges.
来访者：Thanks again, I truly appreciate it.
咨询师：Of course! Remember, you're not alone in this. Reach out whenever you need someone to talk to. Take care and prioritize your well-being.
```

**response（来访当前句）**

```text
I will. Thanks. Take care too.
```

**raw_output（若有，节选）**

```text
合作

# 以上是本题的输入
```

---

### A-120. `extes_10608_2` — 合作 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been struggling with excessive workload and lack of support at my job, which has resulted in severe stress and burnout.
- **binary_label**：合作

**context**

```text
来访者：Hi, how's it going?
咨询师：Hey! I'm here, ready to chat. How are you doing today?
来访者：To be honest, I've been feeling extremely overwhelmed and burnt out lately.
咨询师：It sounds like you're facing a lot of stress and burnout. Can you share more about what's been happening at work?
```

**response（来访当前句）**

```text
I've been working long hours and taking on more responsibilities without any additional support. It feels like I'm constantly drowning in work and it's taking a toll on my mental and physical health. I just don't know how to cope anymore.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作，因为来访
```

---

### A-121. `extes_2592_1` — 合作 | __other__

- **scene**：Moving to a New City or Country
- **description**：Moved to a new city and having trouble adjusting to the different lifestyle and culture.
- **binary_label**：合作

**context**

```text
来访者：Hi there
咨询师：Hello! What's on your mind today?
```

**response（来访当前句）**

```text
I recently moved to a new city, and I'm having a hard time adjusting to the different lifestyle and culture here. It's been quite challenging for me.
```

**raw_output（若有，节选）**

```text
合作

## 心理咨询对话：
###
```

---

### A-122. `extes_286_2` — 合作 | __other__

- **scene**：Surviving and Recovering from Physical or Emotional Abuse
- **description**：My childhood friend recently confided in me about her abusive relationship with her partner. She feels trapped and doesn't know how to leave.
- **binary_label**：合作

**context**

```text
来访者：Hi, I'm feeling really worried and upset about my friend. She's been in an abusive relationship for a while now and she finally opened up about it. I don't know what to do to help her.
咨询师：Hi there, I'm here for you. It's great that your friend trusts you enough to confide in you. I'm here to listen and help you navigate through this situation.
来访者：Thank you. I just don't know how to support her. I want to help her leave this abusive relationship, but it's not easy for her.
咨询师：It's understandable that you feel helpless, but just being there for her and offering support can make a huge difference. Have you talked to her about what she wants or if she's open to seeking help?
```

**response（来访当前句）**

```text
Yes, she's expressed that she wants to leave, but she's afraid of the consequences and doesn't have the financial means to support herself. She's also worried about her safety if she leaves.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-123. `extes_271_5` — 合作 | __other__

- **scene**：Academic Stress or Pressure
- **description**：I have a big presentation coming up and I'm feeling really anxious about it.
- **binary_label**：合作

**context**

```text
来访者：Yeah, I just want to make a good impression and get a good grade.
咨询师：I completely understand. Presentations can be nerve-wracking, especially when they carry importance for your grade. You're not alone in feeling this way.
来访者：It just feels overwhelming right now.
咨询师：I hear you. It's totally understandable to feel overwhelmed when there's a lot on your plate. But remember, you've successfully handled similar situations in the past, and you can do it again.
来访者：I guess you're right. I need to focus on my strengths and believe in myself.
咨询师：Exactly! You have some great strengths. Have you considered practicing your presentation in front of a mirror or a friend? It can help boost your confidence and make you feel more prepared.
```

**response（来访当前句）**

```text
I haven't thought of that, but it sounds like a good idea. I'll give it a try.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-124. `extes_4854_3` — 合作 | __other__

- **scene**：Job Promotion Stress
- **description**：I recently applied for a promotion at work, but I am feeling stressed and anxious about the outcome.
- **binary_label**：合作

**context**

```text
来访者：Hey, I need someone to talk to.
咨询师：Hi there! How are you feeling today?
来访者：Honestly, I'm feeling really stressed out.
咨询师：I'm here to listen. What's been bothering you?
来访者：I recently applied for a promotion at work, and I can't stop thinking about it. I'm anxious about whether I'll get it or not.
咨询师：I understand. Waiting for a response can be nerve-wracking. How long ago did you apply?
```

**response（来访当前句）**

```text
It's been almost two weeks since I submitted my application. The anticipation is killing me. I keep second-guessing myself and wondering if I did enough.
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-125. `extes_110_10` — 合作 | __other__

- **scene**：Job Loss or Career Setbacks
- **description**：Just got laid off from my job due to budget cuts and feeling lost and uncertain about my future career.
- **binary_label**：合作

**context**

```text
来访者：I needed to hear that. It's comforting to know that there's still hope for a brighter future.
咨询师：In the meantime, it's crucial to prioritize self-care and manage any stress that arises. Engaging in activities you enjoy, practicing relaxation techniques, and seeking support from loved ones can all help you navigate this challenging time.
来访者：You're right, self-care should be a priority. I'll make sure to dedicate time to activities that bring me joy and help me unwind.
咨询师：That's wonderful to hear! Just remember that setbacks are not the end of the road but rather a detour. You have the strength and resilience to overcome this and build a fulfilling career once again.
来访者：Thank you for your support and encouragement. It means a lot to me. I'm feeling a bit more hopeful now.
咨询师：You're very welcome! Remember, you're not alone in this journey. Reach out for support whenever you need it. I believe in your ability to bounce back and create a bright future. Take care!
```

**response（来访当前句）**

```text
Thank you again. I appreciate your kindness and positivity. Take care too!
```

**raw_output（若有，节选）**

```text
合作
合作
合作
合作
合作
```

---

### A-126. `extes_506_6` — 合作 | __other__

- **scene**：Parenting Challenges and Parental Guilt
- **description**：My teenage daughter and I have been having constant arguments lately. She seems angry and distant, and I feel guilty for not being able to connect with her. I'm struggling to navigate through these challenges and find a way to rebuild our relationship.
- **binary_label**：合作

**context**

```text
来访者：I want to fix things, but I'm not sure where to start. I feel like everything I say or do just makes it worse.
咨询师：Don't lose hope! Rebuilding relationships takes time and effort. Start by letting your daughter know that you're there for her, listening without judgment can be a good starting point. It's important to show her that you want to find a way to understand each other.
来访者：I guess you're right, I need to be more patient and understanding. It's just hard when I feel like she doesn't want anything to do with me.
咨询师：It's completely valid to feel that way. Sometimes teenagers go through phases where they push away from their parents. Instead of taking it personally, try to empathize with her and understand that it might be her way of asserting her independence. It doesn't mean she doesn't care about you.
来访者：I never thought about it like that. I just want to be there for her, but I'm not sure how to reach out. Any suggestions?
咨询师：One suggestion could be to ask her about her interests and hobbies. Show genuine interest in her life and spend quality time together doing activities she enjoys. This can help create positive experiences and open the door for deeper conversations.
```

**response（来访当前句）**

```text
That sounds like a great idea! I'll give it a try. I just hope she's willing to open up to me. I miss our close relationship.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-127. `extes_421_8` — 合作 | __other__

- **scene**：Moving to a New City or Country
- **description**：Just moved to a new city for a job opportunity but feeling overwhelmed and having trouble adjusting to the new environment.
- **binary_label**：合作

**context**

```text
来访者：Thank you for your encouragement. It's just been hard feeling so alone.
咨询师：I completely understand. Adjusting to a new city can be overwhelming, and feeling alone is a natural response. Just know that you have the strength to overcome these challenges. In the meantime, is there anything you enjoy doing that helps distract you or brings you comfort?
来访者：I've always loved going for walks in nature. It helps me clear my mind.
咨询师：That's a fantastic idea! Nature walks can be so calming and refreshing. There might be beautiful parks or scenic spots in your new city that you could explore. Taking time to engage in self-care activities like walks in nature can help you destress and find some peace amidst the changes.
来访者：I'll definitely look for some nearby parks or green spaces. It sounds like just what I need right now.
咨询师：That's great to hear! Remember, you're not alone in this journey. You have the strength and resilience to overcome the challenges. If you ever need someone to talk to or support again, don't hesitate to reach out.
```

**response（来访当前句）**

```text
Thank you so much for your support and kind words. It means a lot to me.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-128. `extes_2578_7` — 合作 | __other__

- **scene**：Moving to a New City or Country
- **description**：Recently moved to a new city and struggling to adjust to the different lifestyle and culture.
- **binary_label**：合作

**context**

```text
来访者：That's a good idea! I haven't explored those options yet. Do you think it's better to join multiple groups or just focus on one?
咨询师：It varies from person to person, but joining multiple groups can increase your chances of meeting people with diverse backgrounds and interests. At the same time, being actively involved in one group can also help you foster deeper connections. It's worth exploring both approaches and finding what works best for you.
来访者：You're right! I'll try to find a good balance between joining multiple groups and staying connected with one. Do you have any advice on how to overcome the cultural differences in this new city?
咨询师：Navigating cultural differences can be challenging, but it can also be an exciting learning experience. Remember to approach new cultures with an open mind and embrace the differences. Engaging with locals, trying out local cuisine, and participating in cultural events can help you immerse yourself in the new environment and foster a sense of belonging.
来访者：That sounds like a good approach. I'll make an effort to immerse myself in the local culture. But some cultural customs still confuse me.
咨询师：It's completely normal to feel confused about certain cultural customs, especially in a new city. If there's any specific custom or tradition that you'd like to understand better, feel free to share, and I'll do my best to provide you with information.
```

**response（来访当前句）**

```text
Well, for example, I'm not sure when it's appropriate to bow as a sign of respect. It's different in my home country.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-129. `extes_141_5` — 合作 | __other__

- **scene**：Addiction and Recovery
- **description**：My best friend has been battling with alcohol addiction for years. He recently relapsed and is struggling to get back on track. I want to support him, but I'm not sure how to help him through this difficult time.
- **binary_label**：合作

**context**

```text
来访者：Exactly, I want to be there for him and encourage him, but I don't want to enable his behavior either. It's a delicate balance.
咨询师：Have you talked to your friend about his relapse? Open communication can sometimes help in understanding his perspective and providing support.
来访者：I have talked to him, and he admits he has a problem. He says he wants to get better, but I can sense his frustration and self-doubt.
咨询师：It sounds like your friend might be struggling with feelings of hopelessness and frustration. It's important to let him know that you believe in him and his ability to overcome this challenge.
来访者：Yes, I will continue to encourage him and remind him that he has people who care about his well-being. But I worry that my support isn't enough.
咨询师：Feeling that your support may not be enough is a common concern. Remember, you are doing your best, and simply being there for your friend can make a significant difference.
```

**response（来访当前句）**

```text
Thank you for reminding me of that. It's easy to lose perspective in these situations.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作：来访
```

---

### A-130. `extes_598_5` — 合作 | __other__

- **scene**：Addiction and Recovery
- **description**：My best friend has recently relapsed after a year of sobriety. I'm feeling worried and unsure how to support them without enabling their addiction.
- **binary_label**：合作

**context**

```text
咨询师：It can be difficult when someone we care about is not receptive to support. Have you considered seeking help or advice from a support group or counselor familiar with addiction recovery?
来访者：I haven't thought about that before. It might actually be helpful to connect with others who have gone through similar experiences.
咨询师：Joining a support group can provide you with a network of people who understand your situation and can offer guidance and encouragement.
来访者：That does sound like something worth exploring. I just want to make sure I'm doing everything I can to support my friend without enabling them.
咨询师：It's commendable that you want to support your friend in a healthy way. Remember, being there for them emotionally and offering encouragement can make a difference, even if they're not immediately receptive.
咨询师：Another suggestion is to take care of yourself during this challenging time. Engaging in self-care and setting personal boundaries can help you maintain your own well-being.
```

**response（来访当前句）**

```text
That's a good point. I often neglect my own needs when I'm worried about others. I will make sure to prioritize self-care too.
```

**raw_output（若有，节选）**

```text
合作

# 说明
合作。来访
```

---

### A-131. `extes_10721_5` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with a heavy workload and uncertain about future career prospects
- **binary_label**：阻抗

**context**

```text
来访者：Not really. I worry that they'll think I'm not capable or that they won't be understanding.
咨询师：It's important to remember that reaching out for help is a sign of strength. Your professors and advisors are there to support you and want to see you succeed. It might be helpful to schedule a meeting or send them an email to discuss your concerns. Many students face similar challenges.
来访者：You're right, I should try talking to them. I'll send an email today. Thanks for the encouragement.
咨询师：You're welcome! Is there anything else you'd like to talk about or any specific concerns you have?
来访者：Actually, I'm also feeling really uncertain about my future career prospects. It's hard to stay motivated when I'm not sure if my degree will lead to a job.
咨询师：Feeling uncertain about your future is completely normal. Many students face similar concerns, especially during this uncertain time. Have you considered speaking with a career counselor or exploring internships or job fairs to gain more insight into your field?
```

**response（来访当前句）**

```text
I haven't thought about that. I guess I just feel overwhelmed with my current workload and haven't made time to think about my career.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-132. `extes_2127_4` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with a heavy workload and struggling to manage time effectively.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, exactly! I have assignments piling up, multiple exams coming up, and it's starting to feel impossible to keep up.
咨询师：I hear you. It's completely understandable to feel overwhelmed with such a heavy workload. Take a moment to acknowledge that you're shouldering a lot of responsibilities, and it's natural to feel the pressure.
来访者：Thank you, I really needed to hear that. Sometimes I feel like I'm the only one struggling and everyone else has it figured out.
咨询师：You're definitely not alone in feeling this way. Many students experience similar struggles managing their workload and finding a balance. Remember, it's okay to ask for help and seek support when needed. We're all navigating through these challenges together.
来访者：That's reassuring to know. But even when I try to manage my time better, it feels like there's never enough time in a day to get everything done.
咨询师：I completely understand that time constraints can make it difficult to stay on top of your tasks. Have you considered breaking down your workload into smaller, more manageable chunks and prioritizing tasks based on their urgency?
```

**response（来访当前句）**

```text
I've tried that, but it's still overwhelming. It feels like there's always something else I should be doing, and it's hard to focus on one task at a time.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-133. `extes_2150_2` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with the workload for a major project
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I really need to talk about something. I'm feeling so overwhelmed with this major project I have to work on.
咨询师：I'm here for you. Take your time and tell me more about what you're going through.
来访者：It's just a huge project that I'm not sure I can handle alone. There are so many aspects to it, and I feel like I'm drowning in work. It's causing me so much stress and anxiety.
咨询师：It sounds like you're under a lot of pressure. It's completely understandable to feel overwhelmed with such a big project.
```

**response（来访当前句）**

```text
Thank you for understanding. It's just that the deadlines and expectations are weighing heavily on me. I'm afraid I won't be able to meet them.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-134. `extes_370_3` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Struggling to meet deadlines
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I really need to talk about something that's been bothering me.
咨询师：Sure, I'm here to listen. What's been going on?
来访者：I've been under so much pressure with my studies lately. My professors keep piling on assignments and deadlines, and I feel like I'm drowning. I'm constantly stressed and it's affecting my sleep and overall wellbeing.
咨询师：I hear you. It can be really overwhelming when you have a lot of academic responsibilities weighing on you.
来访者：Exactly, it's just hard to manage everything and stay motivated. Sometimes I question my ability to handle it all.
咨询师：I understand how this pressure can make you doubt yourself, but remember that you're capable and have gotten through tough times before. It's okay to feel overwhelmed, but also important to acknowledge your strength and resilience.
```

**response（来访当前句）**

```text
You're right, I've overcome challenges in the past. It's just difficult to see that in the midst of the stress.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-135. `extes_2393_3` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with multiple deadlines and struggling to keep up with coursework.
- **binary_label**：阻抗

**context**

```text
来访者：Hi, I'm really stressed about my assignments and deadlines. I don't know how to keep up with everything.
咨询师：Hey there! I'm here to listen. Can you tell me more about what's going on?
来访者：I have so many assignments due this week, and I'm finding it hard to manage my time effectively. It feels like everything is piling up and I'm getting more and more behind.
咨询师：It sounds like you have a lot on your plate right now. It's completely normal to feel overwhelmed in this situation. You're not alone in experiencing this.
来访者：I know, but I just can't seem to find the motivation to get started on my assignments. I keep procrastinating and it's making me even more stressed.
咨询师：I can understand how procrastination can amplify your stress levels. Breaking your tasks into smaller, more manageable parts might help. Have you tried setting specific goals and prioritizing your assignments?
```

**response（来访当前句）**

```text
I've tried that before, but I still feel anxious and intimidated by the workload. I wish there were more hours in the day.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-136. `extes_11059_3` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with a heavy workload and struggling with time management
- **binary_label**：阻抗

**context**

```text
来访者：Hey there, I really need someone to talk to. I've been feeling so overwhelmed with my coursework lately.
咨询师：Of course, I'm here to listen. Please tell me more about what you're going through.
来访者：Thanks for being here for me. Well, I have a ton of assignments and exams coming up, and I just can't seem to find enough time to get everything done. It's stressing me out and I'm afraid I won't be able to keep up.
咨询师：I can imagine how tough it must be to have so much on your plate. It's completely normal to feel overwhelmed and worried about keeping up with your workload. You're not alone in this.
来访者：Yes, it feels like a never-ending cycle of work and it's really impacting my motivation. I find myself getting distracted and struggling to focus on my tasks.
咨询师：It sounds like your motivation is taking a hit because of the heavy workload. Have you tried breaking your tasks into smaller, more manageable chunks?
```

**response（来访当前句）**

```text
I've been trying, but it still feels like there's so much to do. It's discouraging when I see all the assignments piled up, and I start doubting if I'll ever be able to finish them all on time.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-137. `extes_189_3` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Late-night studying for exams and feeling overwhelmed
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I've been feeling really overwhelmed with my studies lately and I was hoping to talk about it.
咨询师：Of course, I'm here to listen. What's been going on?
来访者：Well, it's almost exam time and I feel like I have so much to study. I've been staying up late every night trying to go through all the material, but it feels like there's never enough time.
咨询师：It sounds like you're under a lot of pressure. Studying for exams can be really stressful, especially when it feels like there's never enough time.
来访者：Exactly, I just can't seem to catch up. And it's hard seeing all my friends taking breaks and having fun while I'm stuck studying all the time.
咨询师：It's tough when it feels like you're missing out on other experiences because of your studies. It's important to take breaks and have fun too.
```

**response（来访当前句）**

```text
I know, but I'm constantly worried that if I take a break, I'll fall behind even more. It's a never-ending cycle of stress and anxiety.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-138. `extes_2385_4` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Struggling to balance part-time job and studies
- **binary_label**：阻抗

**context**

```text
来访者：Sure. I have a part-time job that requires a lot of hours, and as a result, I'm struggling to find enough time to focus on my studies. I feel exhausted and stressed all the time.
咨询师：It sounds like you're facing a lot of pressure trying to balance your work and studies. Feeling exhausted and stressed is completely understandable. How have you been coping with this situation?
来访者：Honestly, I've been trying my best, but it feels like I'm constantly running out of time. I'm falling behind in assignments and I feel like I'm not performing well in both my job and studies.
咨询师：It's tough when it feels like there aren't enough hours in a day to accomplish everything. Have you considered talking to your employer about your workload or exploring strategies to manage your time more effectively?
来访者：I haven't considered talking to my employer yet, but I have tried making a schedule and prioritizing tasks. However, it still feels like I'm racing against the clock and everything is piling up.
咨询师：It's common to feel overwhelmed and pressured when trying to balance work and studies. Many people face similar challenges. You're not alone. Have you tried taking short breaks throughout the day to give yourself some time for relaxation?
```

**response（来访当前句）**

```text
I've tried taking short breaks, but I often find myself feeling guilty for not using that time to catch up on work or do something productive.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-139. `extes_1865_3` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：Feeling overwhelmed with the workload of multiple difficult courses and the pressure to perform well in order to maintain a scholarship.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I wanted to talk about the stress I've been feeling with my academic workload. It's becoming really overwhelming and I'm not sure how to handle it.
咨询师：Of course! I'm here to listen. Can you tell me a bit more about what's been going on?
来访者：Well, I'm currently in my second year of college and I'm taking multiple difficult courses. On top of that, I have a scholarship to maintain, so there's a lot of pressure to perform well. I'm finding it hard to keep up with the workload and I feel like I'm constantly behind and rushing to get everything done.
咨询师：It sounds like you're carrying a heavy load and it's completely understandable that you're feeling overwhelmed. Balancing a challenging academic workload with the pressure to maintain a scholarship can be really tough.
来访者：Exactly. I've been trying my best to stay organized and manage my time effectively, but it just feels like there's never enough time in the day. I find myself getting anxious and stressed about meeting deadlines and keeping up with all the readings and assignments.
咨询师：I can imagine how stressful that must be for you. College can be demanding, especially when you have multiple difficult courses and the added pressure of maintaining a scholarship. Have you reached out to any of your professors or advisors for support or guidance?
```

**response（来访当前句）**

```text
I haven't yet. I guess I've been hesitant to seek help because I don't want to appear incompetent or incapable of handling the workload. I feel like I should be able to manage on my own.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-140. `extes_187_4` — 阻抗 | Academic Stress

- **scene**：Academic Stress
- **description**：struggling with online learning and lack of motivation
- **binary_label**：阻抗

**context**

```text
来访者：Well, I'm having a hard time with online learning. I used to love going to class and interacting with my peers, but now everything feels so disconnected and it's difficult to stay motivated.
咨询师：I understand how challenging the transition to online learning can be. It's not easy to adapt to such a drastic change and miss out on the social aspect of being in class.
来访者：Exactly. I used to be so engaged and proactive in my studies, but now it's hard to even find the motivation to log into my online classes. I feel like I'm falling behind and it's really frustrating.
咨询师：I can imagine how frustrating it must be for you. It's natural to feel demotivated when you're not getting the same level of interaction and support that you were used to.
来访者：Yes, it's been a struggle. I feel like I'm losing my passion for learning and it's affecting my grades too. I used to be an A student, but now I'm barely scraping by.
咨询师：It's disheartening to see your hard work not yielding the results you want. Remember, these circumstances are temporary and you're not alone in this challenge. Many students are facing similar difficulties.
```

**response（来访当前句）**

```text
I know, but it's still hard to stay motivated. I feel like I'm drifting further away from my academic goals and it's causing me a lot of stress and anxiety.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-141. `extes_9080_4` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Recently, I've been experiencing panic attacks at work. Every time I have to give a presentation or speak in front of a group, I start feeling extremely anxious and my heart races. It's affecting my performance and causing me a lot of stress and worry.
- **binary_label**：阻抗

**context**

```text
来访者：I've been having panic attacks at work whenever I have to give presentations.
咨询师：I'm really sorry to hear that, it sounds like a really challenging situation. Can you tell me more about what triggers these panic attacks?
来访者：It usually happens when I have to speak in front of a group. As soon as I start talking, I feel this overwhelming sense of anxiety and my heart starts pounding.
咨询师：So, it seems like the panic attacks are specifically related to public speaking. It can be quite common to feel nervous in front of groups, but when it starts affecting your well-being, it becomes important to address it. How long have you been experiencing these panic attacks?
来访者：It's been happening for a few months now, and it's really starting to impact my work performance. I'm afraid it'll cost me opportunities.
咨询师：I can understand why you would be concerned about it affecting your work and future prospects. It's natural to want to perform well and make a positive impression. Have you spoken to anyone at work about this issue?
```

**response（来访当前句）**

```text
I haven't opened up about it yet. I'm worried they'll think less of me if they know I'm struggling with anxiety.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-142. `extes_2211_3` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Lately, I've been feeling extremely anxious and panicky due to my upcoming job interview. The pressure to perform well is overwhelming, and I can't seem to control my racing thoughts and trembling. It's affecting my sleep and daily life, and I need some support to deal with this anxiety.
- **binary_label**：阻抗

**context**

```text
来访者：Hi there
咨询师：Hello! How can I assist you today?
来访者：I've been preparing for a job interview, but my anxiety is off the charts. I'm finding it hard to concentrate and manage my overwhelming thoughts.
咨询师：I understand how nerve-wracking job interviews can be. It sounds like the pressure is really getting to you, and it's making everything more challenging. Can you share some specific concerns you have about the interview?
来访者：One of my major concerns is freezing up during the interview. I'm afraid that I won't be able to articulate my thoughts clearly and might forget important information.
咨询师：It seems like you're worried about not being able to perform well during the interview and that it might affect your chances. That's a common fear, especially when you want to make a good impression. Have you considered practicing some mock interviews to boost your confidence?
```

**response（来访当前句）**

```text
I've tried some practice sessions, but it's not helping much. My anxiety gets the best of me, and I stumble over my words.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-143. `extes_2209_4` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Lately, I've been feeling extremely anxious whenever I have to meet new people. My heart races, I start sweating, and I often find it hard to breathe. This is making it difficult for me to attend social events and make new connections, which is causing a lot of frustration and loneliness.
- **binary_label**：阻抗

**context**

```text
来访者：To be honest, I've been feeling really overwhelmed with anxiety lately. I find it hard to attend social events because my heart starts racing, and I feel like I can't breathe. It's really impacting my ability to make new connections and I'm starting to feel really lonely.
咨询师：I understand how distressing social anxiety can be. It must be really tough for you and I'm here to listen. Can you tell me a little more about what specific situations trigger your anxiety?
来访者：It seems to happen whenever I have to meet new people or go to parties. The thought of striking up conversations and being the center of attention makes me feel extremely anxious.
咨询师：So, when you're in situations where you have to meet new people or attend parties, that's when you start feeling this overwhelming anxiety. It sounds like the fear of interacting with others and being in the spotlight triggers your anxiety. Have you tried any techniques to cope with these situations?
来访者：I have attempted breathing exercises and positive self-talk, but they don't seem to provide much relief. It's really frustrating not being able to overcome this anxiety.
咨询师：It's completely understandable to feel frustrated when your go-to coping techniques don't work as well as you'd hope. Overcoming social anxiety takes time and it's different for everyone. Have you considered seeking professional help or therapy? They can provide you with effective strategies to manage your anxiety in social situations.
```

**response（来访当前句）**

```text
I've thought about therapy, but I'm also scared of putting myself out there. I just want to feel more comfortable in social settings.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-144. `extes_2480_3` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Lately, I've been feeling extremely anxious about going back to work after a long break. The thought of interacting with colleagues, meeting deadlines, and managing workload is causing me significant panic. It's been keeping me up at night and I feel overwhelmed by these anxious thoughts.
- **binary_label**：阻抗

**context**

```text
来访者：Hey there
咨询师：Hi! How can I help you today?
来访者：I've been struggling with intense anxiety lately. The idea of returning to work after a long break feels overwhelming and it's affecting my sleep and overall well-being.
咨询师：I can understand how daunting it can be to go back to work, especially after a long break. The expectations, deadlines, and interactions with colleagues can certainly trigger anxiety. Can you tell me more about what specifically worries you?
来访者：I'm afraid that I won't be able to handle the workload and the pressure. What if I forget important tasks or make mistakes? The thought of facing the challenges at work scares me.
咨询师：You're expressing concerns about managing the workload, meeting expectations, and the fear of making mistakes. It's completely understandable to feel overwhelmed by these thoughts and worries. Have you communicated your concerns with your supervisor or coworkers?
```

**response（来访当前句）**

```text
I haven't spoken to anyone about it yet. I feel like they'll judge me or think I'm incapable. I guess I fear their reactions.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-145. `extes_716_4` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：Ever since my partner lost their job, I've been feeling really anxious about our financial situation. I'm struggling to cope with the uncertainty and it's affecting my daily life.
- **binary_label**：阻抗

**context**

```text
来访者：I've been feeling so overwhelmed and anxious lately. My partner recently lost their job and I'm really worried about our financial situation.
咨询师：I can understand why you would feel anxious in such a situation, especially when there is uncertainty about your financial stability.
来访者：Yes, it's just been really difficult to handle. I feel like I'm constantly on edge.
咨询师：I can imagine how stressful it must be for you, dealing with the uncertainty and the impact it's having on your daily life. It's completely valid to feel this way.
来访者：Thank you, it means a lot to have someone understand. Do you have any suggestions on how to cope with this anxiety?
咨询师：One strategy could be to focus on what you can control. Take some time to create a budget or financial plan to help alleviate some of the uncertainty. Additionally, practicing self-care activities like deep breathing exercises or meditation can help calm your mind.
```

**response（来访当前句）**

```text
That's a good idea. It's just hard not to constantly worry about what the future holds.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-146. `extes_55_5` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I'm feeling really anxious about returning to work after being on medical leave for anxiety. I'm worried about how my coworkers will perceive me and if I'll be able to handle the stress.
- **binary_label**：阻抗

**context**

```text
来访者：Exactly! It's been really hard for me to get back on track.
咨询师：I can relate to what you're going through. I've experienced anxiety myself, so I understand how challenging it can be to overcome and resume your regular routine.
来访者：It feels overwhelming, and I'm scared of having a panic attack at work.
咨询师：Remember, anxiety tends to amplify our worries and make them seem more intense than they actually are. It might help to remind yourself that you've coped with similar situations before, and you have the skills to manage your anxiety.
来访者：You're right. I have overcome anxiety in the past.
咨询师：That's wonderful to hear! You've already shown resilience and strength in dealing with anxiety before. You can definitely draw on that experience to manage your return to work.
```

**response（来访当前句）**

```text
I guess I'm also worried about what my coworkers will think of me after being on medical leave.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-147. `extes_2494_4` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been feeling extremely anxious and panicky lately due to my fear of flying. I have an upcoming trip and the thought of getting on a plane is causing high levels of anxiety and panic attacks.
- **binary_label**：阻抗

**context**

```text
来访者：I'm feeling really anxious and panicky. I have to take a flight soon and the fear of flying is overwhelming.
咨询师：I can understand why the thought of flying is causing you so much anxiety. It's a common fear, and it can be challenging to manage those intense feelings of panic and fear.
来访者：I just feel like I'm going to have a panic attack on the plane. It's making me reconsider the whole trip.
咨询师：It sounds like the fear of having a panic attack on the plane is really affecting your decision to go on the trip. It's tough when our fears stop us from doing things we want to do. Do you think there are any steps you could take to manage the anxiety during the flight?
来访者：I'm not sure. I've tried deep breathing in the past, but it didn't help much.
咨询师：Deep breathing is a great technique, but it might not be enough by itself. Have you considered trying relaxation exercises, such as progressive muscle relaxation or guided imagery? These techniques can help you relax your body and distract your mind from the fear.
```

**response（来访当前句）**

```text
I haven't tried those before. It could be worth a shot. But what if I have a panic attack and can't control it?
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-148. `extes_2491_6` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been having panic attacks recently due to my new job. The pressure and constant demand at work make me feel overwhelmed, and I start having panic attacks during meetings or when I have to deliver presentations.
- **binary_label**：阻抗

**context**

```text
来访者：I think it's mainly caused by the stress and pressure of my new job. The constant deadlines and high expectations make me feel overwhelmed, leading to panic attacks especially during meetings or presentations.
咨询师：I understand. So, it's the work-related stress and pressure to meet deadlines that trigger your panic attacks. Thank you for sharing that. Have you considered discussing these concerns with anyone at work?
来访者：I don't feel comfortable talking to my colleagues or my supervisor because I don't want them to think less of me.
咨询师：I completely understand your hesitation in discussing this with your colleagues or supervisors, but please know that asking for help doesn't make you weak. It takes courage to reach out and seek support. You may want to consider talking to HR or checking if there are any employee assistance programs available for managing stress at work.
来访者：I haven't thought about that. Maybe it's worth exploring. But I still need help managing my panic attacks in the moment.
咨询师：Absolutely! Let's focus on managing those panic attacks. Have you tried any relaxation techniques or mindfulness exercises?
```

**response（来访当前句）**

```text
I've heard about deep breathing exercises and mindfulness, but I'm not sure if they actually work.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
合作
```

---

### A-149. `extes_2496_2` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been feeling extremely anxious about my upcoming presentation at work. I'm worried that I won't be able to deliver it effectively and it will negatively impact my career.
- **binary_label**：阻抗

**context**

```text
来访者：Hey
咨询师：Hi! How are you doing?
来访者：I'm feeling really anxious and stressed about my presentation next week.
咨询师：I can understand why you would feel anxious about such an important presentation. It's completely normal to feel this way in situations like these.
```

**response（来访当前句）**

```text
Yeah, but my anxiety is getting the best of me. I can't stop thinking about all the ways I could mess up.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-150. `extes_2221_4` — 阻抗 | Anxiety and Panic

- **scene**：Anxiety and Panic
- **description**：I have been experiencing anxiety and panic attacks recently due to the pressure of starting a new job. It has been affecting my daily life, sleep quality, and ability to focus, and I'm not sure how to cope with it.
- **binary_label**：阻抗

**context**

```text
来访者：Lately, I've been dealing with a lot of anxiety and panic attacks. It's been overwhelming and it's affecting my job performance and personal life. I don't know how to handle it.
咨询师：I'm so sorry to hear that you're going through this. Dealing with anxiety and panic attacks can be incredibly challenging. It's completely understandable that it's impacting your work and personal life. Please know that you're not alone in this.
来访者：Thank you for understanding. It's been really tough because I can't seem to control my anxiety and panic attacks, especially at work.
咨询师：It sounds like you're feeling powerless when it comes to managing your anxiety and panic attacks, especially in a work setting. Your concerns are valid, and it takes a lot of strength to reach out for help. Can you identify any specific triggers at work that might be contributing to your anxiety?
来访者：I think it's the pressure to perform well in my new job. I constantly worry if I'm meeting expectations and I fear making mistakes or not being good enough.
咨询师：I understand. So, the pressure to perform well in your new job is triggering your anxiety. Thanks for sharing that. Have you discussed your concerns with your supervisor or any colleagues you trust?
```

**response（来访当前句）**

```text
I'm afraid that if I talk about my anxiety and panic attacks, they won't see me as capable and it might affect my career prospects. So, I've been keeping it to myself.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-151. `extes_1570_6` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being together for five years, I recently went through a painful breakup with my long-term partner. I'm feeling devastated and lost, not knowing how to start over.
- **binary_label**：阻抗

**context**

```text
来访者：I'm dreading the thought of starting over and finding happiness again. Will I ever be able to move on?
咨询师：I know it may not feel like it right now, but you will be able to move on and find happiness again. Healing takes time, and it's completely normal to have these doubts. In time, when you're ready, new opportunities will present themselves.
来访者：It's just hard to imagine a future without them. They were such a big part of my life.
咨询师：I completely understand. It's completely normal to feel that way. Right now, take the time and space you need to heal and rediscover yourself. It's an opportunity for personal growth and discovering new paths that you may not have considered before.
来访者：I can't help but think of all the memories and good times we shared. It seems impossible to replace them.
咨询师：It's completely understandable to reminisce about the good times you had together. Those memories are special and will always hold a place in your heart. Remember that with time, you'll create new memories and share those experiences with someone who values and cherishes you just as much.
```

**response（来访当前句）**

```text
I'm afraid I'll never find someone who loves me as much as my ex did. How can I overcome this fear?
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-152. `extes_9639_5` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After recently going through a painful divorce, I'm feeling lost and unsure about my future. I need someone to talk to and seek emotional support.
- **binary_label**：阻抗

**context**

```text
来访者：I feel devastated. My marriage was a big part of my life, and now it's all over. I don't know how to move forward.
咨询师：That's such a difficult situation to be in. Going through a divorce can bring up a range of emotions and leave you feeling lost. It's completely normal to feel this way. Take your time to process your emotions.
来访者：Thank you. It's hard not to think about all the good times we had together and what could have been.
咨询师：It sounds like you're grappling with a heavy mix of emotions as you reflect on your past and the possibilities that might have been. It's okay to have those thoughts, but try to also focus on finding new beginnings for yourself.
来访者：I'm just not sure how to start over. It feels overwhelming and scary. I'm afraid I won't find happiness again.
咨询师：Starting over can indeed be daunting, especially after such a significant life change. It's completely understandable to feel scared and uncertain about the future. But remember, happiness is still within reach. With time, healing, and support, there's plenty of potential for rediscovery and growth.
```

**response（来访当前句）**

```text
I hope you're right. I just can't picture a life without my ex-spouse. It feels like a huge void.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-153. `extes_11176_5` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：Recently, I ended a long-term relationship with my partner due to constant misunderstandings and disagreements on important values. I am feeling hurt and confused about how to move forward.
- **binary_label**：阻抗

**context**

```text
来访者：I keep questioning whether I made the right decision. It's weighing me down.
咨询师：It's completely normal to have doubts after such a significant life change. Remember that the decision you made was based on what you believed was best for both of you at the time.
来访者：It's hard to accept the reality. I miss my ex-partner so much.
咨询师：It's completely understandable to miss someone you shared a significant amount of time with. Give yourself permission to grieve the loss of the relationship. Healing takes time.
来访者：I'm not sure where to start with healing. Can you suggest some ways to begin the process?
咨询师：During this time, it's important to prioritize self-care. Consider engaging in activities you enjoy, spending time with supportive friends, and exploring personal growth opportunities. These steps can help in the healing process.
```

**response（来访当前句）**

```text
I'll try that out. It's just hard to imagine a future without them.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-154. `extes_10509_6` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After dating for 6 years, my partner and I recently broke up due to growing apart and not sharing the same life goals and aspirations anymore. I'm finding it difficult to cope with the feelings of loss and uncertainty about the future.
- **binary_label**：阻抗

**context**

```text
来访者：I keep blaming myself for the relationship falling apart. I feel like I failed.
咨询师：It's normal to question ourselves and feel responsible for the outcome. However, it's important to remember that relationships involve both parties, and it's rarely the fault of just one person. It's a complex dynamic affected by multiple factors.
来访者：I know deep down it wasn't entirely my fault, but I can't help feeling this way.
咨询师：It's completely valid to have those feelings. It takes time to heal and find peace after such a difficult experience. Be patient and gentle with yourself as you navigate through this challenging time.
来访者：I just don't know what to do with myself now. I feel like a huge part of my life is missing.
咨询师：It may help to focus on your own well-being right now. Consider engaging in activities that bring you joy and promote self-care. Surround yourself with loved ones who can provide support and understanding. Consider exploring new hobbies or seeking professional counseling to guide you through this transition.
```

**response（来访当前句）**

```text
I'll try my best, but it's hard to imagine a life without them right now.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-155. `extes_884_8` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being married for 5 years, my husband recently asked for a divorce. I am feeling devastated and unsure of how to navigate this new chapter in my life.
- **binary_label**：阻抗

**context**

```text
来访者：I just don't know how to move forward. Everything feels uncertain now.
咨询师：It's completely normal to feel uncertain and overwhelmed with the future right now. Keep in mind that this is an opportunity to rediscover yourself, your passions, and the things that bring you joy. The path ahead may seem unclear, but over time, you will gain clarity and find a new sense of purpose.
来访者：I never imagined starting over at this point in my life. It feels incredibly daunting.
咨询师：Starting over is indeed a journey into the unknown, and it can feel overwhelming. However, taking it one step at a time and seeking support from loved ones can make the process more manageable. Allow yourself to grieve, and when you're ready, embrace the potential for growth and new beginnings.
来访者：I'm scared I'll never find love again or be able to trust anyone.
咨询师：It's completely normal to have those fears, especially after such a painful experience. But remember, this chapter in your life doesn't dictate your future. Love and trust can be rebuilt, and there are people out there who will cherish you and respect your journey. Give yourself time to heal, and when you're ready, you'll be able to open your heart again.
```

**response（来访当前句）**

```text
I just don't know where to begin. It feels like my whole life has been turned upside down.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-156. `extes_10002_4` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After three years of marriage, my spouse and I have decided to go through a divorce. We have been growing apart and unable to find common ground, leading to constant arguments and unhappiness in our relationship.
- **binary_label**：阻抗

**context**

```text
来访者：My spouse and I have made the difficult decision to get a divorce. It's been emotionally draining for both of us.
咨询师：I'm really sorry to hear that. Divorces can be extremely challenging and bring about a lot of mixed emotions. How are you doing?
来访者：I've been feeling a rollercoaster of emotions - sadness, regret, anger. It's so overwhelming.
咨询师：It's completely normal to feel a range of emotions during this time. Divorces are complicated and can stir up a lot of conflicting feelings. Take your time to process and acknowledge these emotions.
来访者：Thank you for understanding. I can't help but feel like a failure for letting this happen. It's hard not to blame myself.
咨询师：It's understandable to have those thoughts, but please remember that the responsibility for a relationship doesn't solely rest on one person. Relationships require effort and growth from both parties. It's important not to burden yourself with all the blame.
```

**response（来访当前句）**

```text
You're right. It's just tough to accept that it didn't work out. I had hoped we would have a lifetime together.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-157. `extes_1259_4` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After being in a long-distance relationship for years, my partner and I decided to break up due to the challenges of maintaining the connection and the growing emotional distance. I feel lost and heartbroken, not knowing how to move forward.
- **binary_label**：阻抗

**context**

```text
来访者：We realized that the distance and the emotional disconnect were taking a toll on us. We couldn't find a way to bridge the gap, so we decided it was best to end things.
咨询师：I can imagine how difficult this must be for you. Going through a breakup is never easy, especially when distance and a lack of emotional connection play a role.
来访者：Exactly, it feels like a piece of me is missing. I didn't expect it to hurt this much.
咨询师：Breakups can be incredibly painful, and it's completely normal to feel like a part of you is gone. It's okay to take the time to grieve and heal.
来访者：I keep overthinking whether I made the right decision. It's hard to let go.
咨询师：It's understandable to question your decision. Breakups often bring uncertainty and doubts. Remember that you made the choice based on what you believed was best for both of you in the long run.
```

**response（来访当前句）**

```text
You're right, but it's still difficult to accept. I miss the good times we had.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-158. `extes_9672_6` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After three years of dating, my boyfriend and I have decided to end our relationship. We've been growing apart and unable to resolve our differences.
- **binary_label**：阻抗

**context**

```text
来访者：I can't help but blame myself for the relationship falling apart. Maybe I wasn't good enough.
咨询师：It's common to question ourselves and look for reasons why things didn't work out. But it's important to remember that relationships involve two people, and it's rarely the fault of just one. It's important to consider that multiple factors contribute to the outcome.
来访者：I suppose you're right. I'm just struggling to accept that it's over. I thought we had a future together.
咨询师：It's completely understandable to have difficulty accepting the end of a relationship, especially when you had envisioned a future together. Give yourself time to heal, and remember that new opportunities and paths will emerge.
来访者：What should I do now? I feel empty and don't know how to move forward.
咨询师：Take this time to focus on yourself and your well-being. Surround yourself with loved ones who can offer support during this challenging period. Engaging in activities you enjoy, such as pursuing a hobby or practicing self-care, can help in the healing process.
```

**response（来访当前句）**

```text
I'll try to do that. I'm just worried about being alone and starting over.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-159. `extes_896_3` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：After a 5-year long relationship, I recently went through a painful breakup with my partner. I'm feeling devastated and struggling to cope with the loss and loneliness.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I could really use someone to talk to. Are you available?
咨询师：Of course, I'm here for you. What's been going on?
来访者：I just went through a breakup with my partner of 5 years, and it's been really tough.
咨询师：I'm so sorry to hear that. Going through a breakup after such a significant amount of time can be incredibly challenging. How are you holding up?
来访者：I'm devastated and feeling so alone. I don't know how to navigate life without them anymore.
咨询师：It's completely normal to feel devastated and lost. Ending a long-term relationship can bring on a range of emotions. Give yourself permission to grieve and take this time to focus on healing.
```

**response（来访当前句）**

```text
I thought we would spend our lives together. It feels like everything's fallen apart.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-160. `extes_10328_5` — 阻抗 | Breakups or Divorce

- **scene**：Breakups or Divorce
- **description**：Lately, my girlfriend and I broke up after being in a long-distance relationship for two years. We tried our best to make it work, but the distance took a toll on us. I'm feeling overwhelmed by the sadness and loneliness.
- **binary_label**：阻抗

**context**

```text
来访者：It just hurts so much. I miss her and everything we had together.
咨询师：It's heartbreaking to miss someone who was such an important part of your life. Give yourself time to grieve and allow those emotions to process naturally.
来访者：I tried distracting myself by keeping busy, but it's hard to escape these thoughts and memories.
咨询师：That's understandable. Sometimes keeping yourself occupied can provide temporary relief, but it's also important to give yourself permission to feel and heal. Have you considered expressing your emotions through journaling or talking to a close friend or family member who can lend a listening ear?
来访者：I'll give talking to a friend a try. It's just so difficult to imagine my life without her right now.
咨询师：I can imagine how challenging it is to picture a future without the person you loved. Remember, healing takes time, and with time, the pain will gradually fade, and you'll be more open to new possibilities.
```

**response（来访当前句）**

```text
I hope so. I'm just afraid of going through another heartbreak. I don't know if I can trust someone again.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-161. `extes_5840_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently moved to a new city and I'm feeling lonely and disconnected from the people around me.
- **binary_label**：阻抗

**context**

```text
来访者：Hey there!
咨询师：Hello, how can I assist you today?
来访者：I've been feeling really lonely since I moved to this new city. I don't know anyone here and it's been difficult to make friends or connect with people.
咨询师：I can understand how challenging that must be. Moving to a new city can be overwhelming, and feeling lonely is completely normal in such situations. It takes time to build a new social circle and establish connections. Have you tried exploring any local groups or joining community events? These can be great opportunities to meet like-minded people.
来访者：I've tried attending a few events, but it's hard to break the ice and initiate conversations. I often feel like an outsider and it makes me question whether I made the right choice by moving here.
咨询师：I can imagine how discouraging that feels, especially when it seems difficult to fit in or find common ground with new people. Remember, building connections takes time and effort. It's natural to question your decision in the face of loneliness, but it doesn't mean you made the wrong choice. Give yourself some patience and keep exposing yourself to new opportunities. You never know when you might meet someone who becomes a wonderful companion.
```

**response（来访当前句）**

```text
I appreciate your understanding. It's just hard not having anyone to share experiences with or hang out with in this new city. I feel isolated and it's affecting my overall well-being.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-162. `extes_6800_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently started a new job and I'm struggling with a lack of confidence in my abilities. I constantly worry that I'm not capable of handling my tasks and that my colleagues will discover that I'm not as skilled as they think.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, can I talk to you about something that's been bothering me?
咨询师：Of course! I'm here to listen. What's been on your mind?
来访者：I recently started a new job and I'm feeling really insecure. I worry that I'm not good enough and that my colleagues will realize I'm not as competent as they think I am.
咨询师：I understand how overwhelming it can be to start a new job and feel like you're not measuring up. It's important to remember that many people experience these feelings of self-doubt. How has this lack of confidence been affecting your work?
来访者：It's been making it difficult for me to focus and fully engage in my tasks. I'm also hesitant to ask for help because I don't want to appear incompetent.
咨询师：It's completely understandable to feel that way, but remember that asking for help is a sign of strength rather than weakness. It shows that you're proactive and committed to delivering your best work. Have you discussed these concerns with anyone at your workplace?
```

**response（来访当前句）**

```text
Not yet. I feel embarrassed and worried about what others might think of me if I share my insecurities.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
合作
```

---

### A-163. `extes_2812_6` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently went through a breakup with my partner of five years and I'm feeling heartbroken and unsure of how to move forward.
- **binary_label**：阻抗

**context**

```text
来访者：Exactly. I thought we were going to spend our lives together. Now I don't know what to do or where to go from here.
咨询师：I can understand how overwhelming it must feel to suddenly have your future plans shattered. It's okay to feel lost and uncertain right now.
来访者：Thank you for understanding. It's just hard to imagine a life without them.
咨询师：It's completely normal to feel that way. Give yourself some time to grieve the loss of the relationship. Healing takes time, and eventually, you'll find your way forward.
来访者：I hope so. Right now, I just feel like I'll never be able to trust or love again.
咨询师：Feeling that way is completely understandable, but it's important to remember that this breakup doesn't define your ability to love or be loved. It's a setback, but it doesn't mean you won't find happiness and trust again in the future.
```

**response（来访当前句）**

```text
I guess you're right. It's just hard to see that possibility right now.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-164. `extes_8272_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：The user is feeling overwhelmed with balancing work and personal life responsibilities.
- **binary_label**：阻抗

**context**

```text
来访者：I don't know how to manage my work and personal life. I feel like I'm constantly juggling and never getting a break.
咨询师：Hey there! I can understand how overwhelming it can feel to handle both work and personal life responsibilities. Let's talk about it. What's been going on?
来访者：I have a demanding job that requires long hours, and when I come home, I have household chores and family responsibilities to take care of. It's exhausting and I don't have any time for myself.
咨询师：That does sound incredibly exhausting, having such a heavy workload and multiple responsibilities at home. You're doing your best, but it's essential to take care of your own well-being too. Are there any specific areas that you find most challenging in trying to find a balance?
来访者：I always seem to be prioritizing others' needs over my own. I feel guilty if I take time for myself, but it's taking a toll on my mental and physical health.
咨询师：I completely understand how you feel. It's a common challenge to prioritize others' needs and neglect our own. However, self-care is vital for maintaining good mental and physical health. Remember, you can't pour from an empty cup. By taking care of yourself, you will have more to give to others. What are some self-care activities that you enjoy?
```

**response（来访当前句）**

```text
I used to love painting, but I haven't picked up a paintbrush in ages. I feel guilty for spending time on hobbies instead of attending to my responsibilities.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-165. `extes_6949_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I'm feeling really anxious because I have to give a presentation in front of a large audience and I'm afraid of messing up.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, can I talk to you about something?
咨询师：Of course, what's on your mind?
来访者：I'm feeling really anxious right now. I have to give a presentation in front of a large audience and I'm afraid of messing up.
咨询师：Oh, I can understand why you feel anxious about giving a presentation. It can be nerve-wracking to be the center of attention and worry about making mistakes. How has this anxiety been affecting your confidence and preparation for the presentation?
来访者：I've been losing sleep over it and I can't seem to focus on anything else. I keep imagining worst-case scenarios and it's making me doubt my abilities.
咨询师：It sounds like your anxiety is impacting your overall well-being. It's completely normal to feel nervous before a big presentation, but it's important to remind yourself of your capabilities. Have you tried any relaxation techniques or breathing exercises to help calm your nerves?
```

**response（来访当前句）**

```text
I've tried taking deep breaths, but it only provides temporary relief. The anxiety always comes back.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-166. `extes_3506_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling disconnected from my friends lately. We used to be so close and spend a lot of time together. However, recently they've been cancelling plans and not reaching out to me as much. It's making me feel like maybe they don't value our friendship anymore.
- **binary_label**：阻抗

**context**

```text
来访者：Hey
咨询师：Hello! How are you doing?
来访者：I've been feeling disconnected from my friends lately. We used to be so close and spend a lot of time together. However, recently they've been cancelling plans and not reaching out to me as much. It's making me feel like maybe they don't value our friendship anymore.
咨询师：I'm sorry to hear that. It must be really tough to feel like your friends are withdrawing and not prioritizing your friendship. Have you talked to them about how you're feeling?
来访者：I haven't brought it up yet because I don't want to come across as needy or clingy. I don't want to push them away even more.
咨询师：I understand your concerns about not wanting to strain the friendship further. It can be difficult to bring up sensitive subjects. However, keeping your emotions bottled up may not help either. Is there a close friend among them that you feel comfortable talking to? Maybe you can express your feelings in a calm and open manner.
```

**response（来访当前句）**

```text
There's one friend whom I feel closer to. I'll try talking to her about this, but I'm worried she might take sides or get defensive.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-167. `extes_6055_2` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I recently moved to a new city and I'm having trouble making friends. I often feel lonely and it's been challenging to connect with people. I could use some support and guidance on how to navigate these social challenges.
- **binary_label**：阻抗

**context**

```text
来访者：Hey
咨询师：Hi! How can I assist you today?
来访者：I've been feeling quite lonely since I moved to a new city. I've been struggling to make friends and it's making me feel isolated and disconnected.
咨询师：I can imagine how difficult that must be. Moving to a new city and trying to make friends can be challenging, especially when you feel like you don't have that strong support system. Have you tried reaching out to any local social groups or communities in the city?
```

**response（来访当前句）**

```text
I've tried attending a few meetups and joining some social clubs, but it's been hard to break through and make genuine connections. I feel like an outsider.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-168. `extes_7195_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I'm feeling really anxious about an upcoming job interview and I need someone to talk to.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I could really use some support right now. I have a job interview coming up and I'm feeling extremely anxious about it.
咨询师：Hi there! I'm here to listen and offer support. I'm sorry to hear that you're feeling anxious about your upcoming job interview. Can you tell me more about what's been happening?
来访者：Thanks for listening. I've been preparing for this interview for weeks, but I can't shake this feeling of nervousness. I'm worried about making a good impression and answering all the questions correctly.
咨询师：I can understand how nerve-wracking job interviews can be. It's completely normal to feel anxious in such a situation. The pressure to make a good impression and perform well can be stressful. Is there anything specific about the interview that's causing you the most anxiety?
来访者：I think it's the fear of not being able to answer the questions properly or stumbling over my words. I don't want to come across as unprepared or incompetent.
咨询师：It's completely understandable to be worried about answering questions during an interview. The fear of not performing at your best can be overwhelming. Have you practiced answering common interview questions or done any mock interviews to help build your confidence?
```

**response（来访当前句）**

```text
I've done some practice, but I still feel like I'll freeze up during the actual interview. I get so nervous that I forget what I wanted to say.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-169. `extes_9252_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：I've been feeling really stressed out lately because my workload has doubled, and it's becoming overwhelming.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, can I talk to you about something? I've been feeling really overwhelmed lately.
咨询师：Of course! I'm here to listen. What's been going on?
来访者：My workload has doubled recently, and I'm finding it really hard to keep up. It's becoming overwhelming and affecting my stress levels.
咨询师：I completely understand how having an increased workload can be overwhelming and stressful. It's difficult when you feel like you're being pulled in different directions. How long has this been going on?
来访者：It's been going on for about a month now, and I feel like I can't catch a break. My stress levels are through the roof.
咨询师：I can imagine how exhausted and stressed you must be feeling right now, trying to manage the increased workload for such a prolonged period of time. It's important to take care of yourself and find ways to alleviate some of that stress.
```

**response（来访当前句）**

```text
I know, but it's so hard to find the time to relax. Every day feels like a never-ending cycle of work.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-170. `extes_3663_3` — 阻抗 | Communication Challenges

- **scene**：Communication Challenges
- **description**：A user is feeling frustrated and anxious because they have been assigned a new project at work but are struggling to understand the requirements and expectations.
- **binary_label**：阻抗

**context**

```text
来访者：Hey there
咨询师：Hi! How are you doing today?
来访者：I'm feeling really frustrated and anxious right now. I've just been assigned a new project at work, but I'm having a hard time understanding the requirements and expectations, and it's stressing me out.
咨询师：I can understand why you would feel frustrated and anxious. Starting a new project can be quite overwhelming, especially when you don't fully grasp the requirements or expectations. It's normal to feel this way. Can you tell me more about the project and what specifically is causing you the most stress?
来访者：Sure. The project manager gave me a brief outline, but it's quite vague, and I'm not entirely sure what the end goal is. I've been trying to reach out for clarification, but the project manager has been busy, and it's making me worry that I won't be able to deliver what is expected.
咨询师：I can empathize with your situation. It's frustrating when you receive a vague outline for a new project, and it's difficult to determine the end goal. Trying to seek clarification shows your commitment and dedication. Have you expressed your difficulties and concerns to the project manager?
```

**response（来访当前句）**

```text
I haven't had the chance to sit down with the project manager yet. I don't want to sound incompetent or bother them with my questions. But the more I delay, the more anxious I become about not being able to meet the expectations.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-171. `extes_6697_4` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I've been having a hard time communicating with my sibling lately. We used to have a close bond, but now we often misunderstand each other and end up arguing. It's really affecting me emotionally and I don't know how to resolve these conflicts.
- **binary_label**：阻抗

**context**

```text
来访者：Well, we were talking about plans for a family event, and I made a suggestion that my sibling interpreted as criticising their ideas. They got angry and defensive, and we ended up arguing instead of having a productive conversation.
咨询师：That sounds like a challenging situation. It's natural to feel frustrated and disappointed when miscommunication hinders your relationship with a loved one. How did that argument make you feel and what impact has it had on your sibling bond?
来访者：I felt hurt and misunderstood. It seems like every time we try to have a conversation now, it turns into a fight. It's putting a strain on our relationship, and I don't want to lose the close bond we used to have.
咨询师：I can understand why you're feeling that way. It's difficult to experience such tension and conflict with someone who is important to you. It must be really tough for you to see this change in your sibling relationship.
来访者：Yes, it's really disheartening. I miss the easy and open communication we had before. I just want things to go back to the way they used to be.
咨询师：It's common for siblings to go through rough patches in their relationship, especially as they grow and change. It might take some effort and understanding from both sides to find common ground again. Have you tried talking to your sibling about how these arguments are making you feel?
```

**response（来访当前句）**

```text
I haven't yet. I'm worried that they won't listen or understand, and it'll lead to another argument.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-172. `extes_4422_3` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I have been feeling distant from my best friend lately and I suspect there might be some unresolved issues between us. I want to address it and repair our friendship, but I don't know how to approach the conversation.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I need to talk about something that's been bothering me.
咨询师：Sure, I'm here to listen. What's been going on? You seem a bit troubled.
来访者：I've been feeling disconnected from my best friend recently. I think there might be some unresolved issues between us, and it's been weighing on me.
咨询师：I'm sorry to hear that. It can be tough when there's tension in a close friendship. Can you tell me a bit more about what makes you feel this way?
来访者：We used to talk all the time and share everything, but now it feels like we're drifting apart. We've been arguing more often, and there's a growing sense of distance between us.
咨询师：It's disheartening to experience a shift in a friendship and conflicts can certainly strain the relationship. Have you considered discussing your feelings with your friend?
```

**response（来访当前句）**

```text
I'm afraid that talking about it might make things worse or push us even further apart.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-173. `extes_6835_3` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling disappointed because my friend and I have been having misunderstandings lately, and it's causing strain in our relationship. We're having trouble understanding each other's perspectives and it feels like we're growing apart.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, do you have a moment to chat? I'm feeling really down about something.
咨询师：Of course, I'm here to listen. What's been bothering you?
来访者：Lately, my friend and I seem to be misunderstanding each other a lot. It's making me really sad. I feel like we're drifting apart and it's hard to communicate our thoughts and feelings properly.
咨询师：I can understand how that would be disheartening. Misunderstandings can create distances in relationships. Could you give me an example of a recent misunderstanding?
来访者：Sure, we were planning a get-together, and I assumed it would be a small gathering, but my friend invited more people without consulting me. I felt left out and like my opinion didn't matter.
咨询师：That sounds really tough. It's important to feel included and heard in a friendship. Have you tried expressing your feelings to your friend?
```

**response（来访当前句）**

```text
Yes, I tried talking to them about it, but they got defensive and said I was overreacting.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-174. `extes_8424_3` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my partner and I are having trouble communicating effectively. We constantly misunderstand each other's intentions and it's causing tension in our relationship.
- **binary_label**：阻抗

**context**

```text
来访者：Hi there, I need some advice regarding a communication issue I'm facing in my relationship.
咨询师：Of course, I'm here to listen. What's been going on and how are you feeling about it?
来访者：Lately, my partner and I have been having a hard time understanding each other. It's frustrating because we often misinterpret each other's words and intentions. This is causing a lot of tension and arguments between us, and I'm not sure how to resolve this communication problem.
咨询师：That sounds really tough. Communication issues can be incredibly challenging and emotionally draining. How has this been affecting you and your relationship?
来访者：It's been really draining and disheartening. Every conversation seems to end up in an argument, and I feel like we're constantly on different wavelengths. I love my partner and want to work through this, but it's hard when our words seem to get twisted or misunderstood.
咨询师：I can understand why you feel drained and disheartened by this situation. It's difficult to navigate a relationship when communication is strained and misunderstood. Your feelings are valid, and it's important to find a way to address this issue together. Have you talked to your partner about how you're feeling?
```

**response（来访当前句）**

```text
Yes, we've tried to talk about it, but it often ends up becoming another argument. We just can't seem to find a way to communicate effectively without getting defensive or feeling attacked.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-175. `extes_6560_3` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I am feeling frustrated about an ongoing conflict with my friend. We used to have a strong bond, but recently, we've been having constant arguments and misunderstandings, which is straining our friendship.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, do you have a moment to talk? I could really use some advice.
咨询师：Of course, I'm here to listen. What's been going on? It sounds like something is bothering you.
来访者：Yeah, I've been having a lot of conflicts with my friend lately and it's starting to affect our friendship.
咨询师：I'm sorry to hear that. Can you tell me more about what's been happening and how it's been making you feel?
来访者：We've been having constant arguments and misunderstandings. It seems like we can't agree on anything anymore.
咨询师：That sounds really challenging. It's tough when conflicts start to strain a once-strong friendship. Have you tried discussing the issues with your friend?
```

**response（来访当前句）**

```text
We've tried talking about it, but it always turns into a bigger argument. It feels like we're not getting anywhere.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-176. `extes_9633_4` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my best friend constantly cancels our plans at the last minute without any explanation.
- **binary_label**：阻抗

**context**

```text
来访者：Well, my best friend keeps canceling our plans at the last minute, and it's really frustrating.
咨询师：I want to make sure I understand the situation. Can you tell me more about how your friend cancels the plans?
来访者：Whenever we make plans, everything seems fine until the last minute. Then my friend sends a text saying they can't make it, without any explanation or rescheduling.
咨询师：That must be really disappointing and upsetting. It's understandable why you would feel frustrated when your friend consistently cancels plans without any clear communication or consideration. How have these cancellations been affecting you?
来访者：It makes me question the importance of our friendship. I feel like my time and effort are not valued, and it's taking a toll on our relationship. I don't know what to do.
咨询师：I can understand how you're feeling. It's disheartening when someone we care about repeatedly cancels plans without any regards for our feelings. It's important to address this situation and find a resolution that works for both of you. You deserve open communication and respect in any relationship.
```

**response（来访当前句）**

```text
You're right. I want to talk to my friend about this, but I'm afraid it might strain our friendship even more. I don't want to lose them.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-177. `extes_6197_5` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I've been having difficulties communicating with my coworker lately. We used to have a good working relationship, but recently there have been misunderstandings and arguments that have created tension between us. It's really affecting my motivation and productivity at work, and I don't know how to resolve these conflicts.
- **binary_label**：阻抗

**context**

```text
来访者：Sure, there was a project where we had different visions on how it should be executed. Instead of discussing and finding a middle ground, it turned into a heated argument. It's really demoralizing when we can't find a way to work together effectively.
咨询师：It sounds like a challenging situation. It can be tough when your work dynamic changes and conflicts arise. How do these disagreements make you feel and how does it impact your motivation?
来访者：I feel frustrated and unheard. These disagreements make me doubt my abilities and it's affecting my motivation to perform well at work. I used to enjoy collaborating with my coworker, but now I dread it and feel stressed whenever we have to interact.
咨询师：I can understand how disheartening that must be. Collaborating in a challenging environment can definitely have a negative impact on motivation and overall job satisfaction. It seems like you're longing for a harmonious work relationship.
来访者：Exactly. I miss the positive dynamics we used to have, where we could bounce ideas off each other and work together seamlessly. Now it feels like everything is a struggle and it's affecting both my productivity and my enjoyment of my work.
咨询师：It's understandable that you want to find a resolution. Have you tried initiating an open and honest conversation with your coworker, expressing your concerns and desire for improved collaboration?
```

**response（来访当前句）**

```text
I haven't yet. I've been hesitant because I'm not sure how my coworker will react or if it will make things worse. I'm worried that it might even further strain our working relationship.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-178. `extes_3134_4` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I'm feeling frustrated because my partner and I keep arguing about household chores.
- **binary_label**：阻抗

**context**

```text
来访者：Well, I've been feeling really frustrated because my partner and I keep arguing about household chores.
咨询师：I want to make sure I understand your situation. Can you tell me more about the arguments? What specifically is causing these disagreements?
来访者：It seems like we're constantly fighting over who should be responsible for what around the house. We have different standards and expectations, and it's causing a lot of tension between us.
咨询师：That sounds incredibly frustrating and stressful. Disagreements about household chores can add a lot of strain to a relationship. How has this been affecting your overall dynamic with your partner?
来访者：It's making me feel resentful towards my partner. I feel like I'm carrying most of the load and they don't appreciate my efforts. It's also affecting our intimacy because we're always mad at each other.
咨询师：I completely understand why you would feel that way. It's not easy when responsibilities feel unbalanced and it creates tension in your relationship. It's important for both partners to feel supported and valued. Have you communicated your feelings and concerns with your partner?
```

**response（来访当前句）**

```text
We've tried talking about it, but it often turns into an argument. We just can't seem to find a resolution.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-179. `extes_1664_4` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I am having trouble communicating with my best friend
- **binary_label**：阻抗

**context**

```text
来访者：We used to be so close and share everything, but recently, it feels like we're drifting apart. Whenever I try to talk to them about how I'm feeling, they seem disinterested or brush it off. It's really hurtful.
咨询师：That must be really tough for you to experience. Can you give me an example of a recent conversation where you felt brushed off or ignored?
来访者：Last week, I tried to talk to them about a problem I was facing at work. I wanted their support and advice, but they seemed distracted and changed the topic to something unrelated. It felt like they didn't really care about what I was going through.
咨询师：I understand how that could make you feel hurt and invalidated. It's difficult when you're seeking support from a best friend and they seem disengaged. Your feelings are valid.
来访者：I just don't know what to do. I've tried talking to them about it, but they don't seem interested in addressing the issue. I don't want to lose our friendship, but it feels like we're growing apart.
咨询师：It's understandable that you're concerned about losing a close friendship. It's important to remember that relationships go through ups and downs, and it takes effort from both sides to maintain a connection. Have you expressed your feelings and concerns about the drifting apart?
```

**response（来访当前句）**

```text
Yes, I've tried talking to them, but they always brush it off or say that everything is fine. I don't know how to make them understand how much this is affecting me.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-180. `extes_5864_4` — 阻抗 | Conflicts or Communication Problems

- **scene**：Conflicts or Communication Problems
- **description**：I had an argument with my sibling over a decision about selling our parents' house, and it's causing tension between us.
- **binary_label**：阻抗

**context**

```text
来访者：We were discussing whether or not to sell our parents' house. I strongly believe that we should sell because it's becoming a financial burden, while my sister wants to keep it for sentimental reasons. Our disagreement escalated and turned into a heated argument.
咨询师：It sounds like this decision is causing conflict between you and your sister. Can you share more about how you both feel about the house and why you have such different perspectives?
来访者：I feel like selling the house is the practical thing to do. The maintenance costs are getting high, and it's preventing us from moving forward in our lives. On the other hand, my sister sees the house as a symbol of our childhood memories and doesn't want to let go of that sentimental value.
咨询师：It's clear that both of you have valid reasons for your opinions. Your perspective on the financial burden and practicality makes sense, while your sister values the emotional connection to the house. Conflict around decisions involving emotional attachments can be challenging. It must be tough to face such disagreements with your sibling.
来访者：Yes, it's really hard because I love my sister and I don't want this disagreement to ruin our relationship.
咨询师：I understand how important family relationships are to you. It's completely normal to have disagreements, especially when it comes to decisions around valuable assets like a family home. Have you had a chance to talk to your sister about finding a middle ground or addressing the issue calmly?
```

**response（来访当前句）**

```text
We haven't really been able to talk since the argument. We both stormed off in anger, and now there's this tense atmosphere whenever we see each other.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-181. `extes_2238_6` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away due to a sudden heart attack, and I'm feeling lost. I've always been close to him, and his absence has left a huge void in my life.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, he was. It's just hard to imagine life without him. I feel like I'm constantly reminded of his absence.
咨询师：It's completely natural to feel that way. Grief can be overwhelming, and it takes time to adjust to life without someone who played such an important role. Remember to be patient with yourself throughout this process.
来访者：I'm trying to be patient, but it's tough. I find myself getting emotional at the smallest things that remind me of him.
咨询师：It's okay to cry and express your emotions. Grief is a complex journey, and it's not always easy. Remember that your feelings are valid, and it's important to give yourself permission to grieve. Is there anything in particular that triggers your emotions?
来访者：Sometimes it's a song that we used to listen to together or even his favorite dish that I come across. It just brings back so many memories and emotions.
咨询师：I can understand how those reminders can make you emotional. It's incredible how our senses can evoke such strong memories and emotions. Eventually, these triggers may serve as reminders of the bond you shared with your uncle, which can bring you comfort instead of sadness.
```

**response（来访当前句）**

```text
I hope so. Sometimes I worry that I'll never be able to move on from this overwhelming grief.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-182. `extes_1337_4` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle passed away recently, and I'm struggling to cope with the loss. I feel overwhelmed and don't know how to navigate my emotions.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, not great. My uncle passed away recently, and I'm having a really hard time.
咨询师：I'm sorry to hear that. It sounds like you're going through a challenging time. How have you been coping so far?
来访者：It's been really tough. I find myself feeling overwhelmed and not knowing how to express my emotions properly. Sometimes I just want to be alone.
咨询师：It's completely normal for you to feel overwhelmed and have difficulty processing your emotions. Grieving is a complex process, and everyone copes differently. Is there anything specific that you find comforting or that helps you feel supported?
来访者：I find solace in talking about the memories I had with my uncle and looking at old photographs. But there are moments when I just want to retreat to my own space.
咨询师：It's understandable that you find comfort in reminiscing about the good times and cherishing those memories. It's also crucial to respect your need for solitude during this grieving period, as everyone needs different amounts of space to heal. Have you considered seeking additional support, maybe from a grief counselor or joining a support group?
```

**response（来访当前句）**

```text
I haven't really thought about that. I guess I feel like I should be able to handle it on my own.
```

**raw_output（若有，节选）**

```text
阻抗

# 解释：
阻抗是
```

---

### A-183. `extes_1374_4` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My best friend recently passed away and I'm having a tough time dealing with the grief. We shared so many memories and experiences together, and now I feel lost without them. I need someone to talk to and help me cope with this loss.
- **binary_label**：阻抗

**context**

```text
来访者：I've been feeling so empty and lost since my best friend passed away. We were practically inseparable and now there's this void in my life that I don't know how to fill.
咨询师：I can only imagine how difficult it must be for you. Losing such a close friend leaves a huge impact, and it's completely normal to feel a sense of emptiness and uncertainty. Take your time to process your emotions.
来访者：Thank you for understanding. It's just hard to accept that they're gone. We had so many plans and dreams together.
咨询师：It sounds like you're reflecting on all the dreams and plans you shared with your best friend. Grieving the loss of those future possibilities can be challenging. Remember, though they may no longer physically be with you, their impact and memories will always remain.
来访者：Yes, but it's just so painful. I miss them every day. I wish I could have had more time with them.
咨询师：I can empathize with the pain you're feeling. Grief can be overwhelming, leaving you longing for more time with your loved one. Allow yourself to grieve and cherish the memories you have. It's okay to miss them and feel the pain deeply.
```

**response（来访当前句）**

```text
Thank you for your empathy. Sometimes it feels like the sadness will never go away.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-184. `extes_9884_2` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away from a prolonged illness. I'm struggling with grief and finding it hard to come to terms with his absence. I'm also feeling guilty for not being able to spend enough time with him before he passed.
- **binary_label**：阻抗

**context**

```text
来访者：Hi, I really need someone to talk to. I've been feeling so sad and guilty lately.
咨询师：Of course, I'm here for you. Tell me what's been going on. I'll listen.
来访者：Thank you, I appreciate it. My uncle recently passed away after a long illness, and it's hitting me hard. I can't help but feel guilty for not spending more time with him before he passed.
咨询师：I'm so sorry for your loss. Losing a loved one is never easy, especially when you harbor feelings of guilt. It's normal to have those thoughts, but remember that you did the best you could in the circumstances.
```

**response（来访当前句）**

```text
I know you're right, but I can't help but wish I had done more. I feel like I could have made him happier in his last days.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-185. `extes_1041_5` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My best friend recently passed away and I'm having a tough time dealing with the grief. We were like siblings and losing them has left a huge void in my life. I'm struggling to come to terms with their absence and it's affecting my daily life and emotional well-being.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. It's just hard to accept that they're no longer with us. I keep thinking about all the memories we shared and it makes me incredibly sad.
咨询师：It sounds like you're really missing the deep connection you had with your best friend and cherishing the memories you made together. Those memories will always be a part of you and can bring you comfort when you're ready.
来访者：Yes, exactly. I want to hold on to those memories and honor their legacy. But sometimes the pain feels overwhelming. I just wish they were here.
咨询师：I can imagine how overwhelming it must be for you. Grief can be like waves that come and go. It's normal to have those moments when the pain hits hard. Just remember to be compassionate with yourself and allow yourself to feel everything you need to feel.
来访者：Thank you for your kind words. It helps to know that what I'm going through is a natural part of the grieving process. I've been trying to find ways to cope, but it's been a struggle.
咨询师：I understand that it may feel like an uphill battle right now. But with time, the intensity of the pain will gradually lessen. You'll begin to find moments of joy amidst the sadness as you continue to honor your best friend's memory.
```

**response（来访当前句）**

```text
I really hope so. It's just hard to see a brighter future without them. They were such a positive influence in my life.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-186. `extes_2235_6` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle was recently diagnosed with a terminal illness and it's been really hard for me to come to terms with the fact that he may not be with us for much longer. I'm feeling a mix of sadness, anger, and confusion.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. It means a lot to me.
咨询师：Of course, I can imagine how heartbreaking it must be. Your love and concern for your uncle are shining through these difficult emotions. Remember to be gentle with yourself during this process.
来访者：It's just hard to see someone you care about suffering. I wish there was something more I could do.
咨询师：It's natural to want to help, but sometimes the most impactful thing we can do is simply be there for our loved ones. Your presence and support mean more to your uncle than you may realize.
来访者：I hope so. I've been spending as much time as I can with him and trying to make him comfortable.
咨询师：That shows a great deal of compassion and love. Your uncle is fortunate to have you by his side during this challenging time. Your presence alone can bring him comfort and peace.
```

**response（来访当前句）**

```text
I just wish there was some way I could take away his pain and help him feel better.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-187. `extes_1322_3` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My cousin recently lost his father to a sudden heart attack, and he's struggling with the grief and sense of loss. He has always been very close to his father and relied on his guidance in life. Now, he feels lost and doesn't know how to navigate through life without his father's support.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, are you there?
咨询师：Hello, how are you doing today?
来访者：I'm not doing so well. My cousin's father recently passed away from a heart attack, and he's really having a hard time. He feels lost and doesn't know how to move forward without his dad's guidance and support.
咨询师：I'm so sorry to hear that. Losing a loved one, especially a parent, can be incredibly tough. It's natural for your cousin to feel lost and overwhelmed by this sudden loss.
来访者：Yes, it's just so devastating to witness him in so much pain. I wish I could do something to help him through this.
咨询师：Your presence and support mean a lot to him, even if it may not seem like it's enough. Just being there to listen and offer comfort can go a long way in providing him some solace during this challenging time.
```

**response（来访当前句）**

```text
I try my best, but sometimes I'm at a loss for words. I'm afraid of saying or doing something that might make him feel worse.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-188. `extes_4976_5` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My cousin recently passed away after a long battle with a terminal illness, and I'm struggling to come to terms with the loss. I feel overwhelmed and unsure of how to cope with my emotions.
- **binary_label**：阻抗

**context**

```text
来访者：I feel so overwhelmed. I keep replaying memories in my head and it's making it even more difficult to accept that they're gone.
咨询师：It's completely normal to feel overwhelmed and lost during the grieving process. Your emotions are valid, and it's okay to take your time to accept the loss. Losing someone close to you is a profound experience.
来访者：Sometimes I feel guilty for not being able to do more for them. I wish I had spent more time with them while they were still alive.
咨询师：Guilt is a common emotion that often arises during grief. It's important to remember that you did what you could within your capabilities and circumstances. Your cousin knew you cared about them. Sometimes we have to cope with feelings of regret as a natural part of the grieving process.
来访者：You're right, I understand that intellectually, but emotionally it's hard to shake off the guilt.
咨询师：It's understandable that it will take time to process and let go of the guilt you're feeling. Remind yourself that you cared for your cousin and that you were there for them in the ways you could be. During this difficult time, focus on self-compassion and giving yourself permission to heal.
```

**response（来访当前句）**

```text
I'll try to be more forgiving towards myself. It's just so challenging.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-189. `extes_10379_5` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My best friend recently passed away and I'm having a tough time dealing with the grief. We were incredibly close, and her presence in my life made a big impact. Losing her has left a void and I'm struggling to navigate my emotions and daily life.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. I keep replaying all the memories we shared and it's heartbreaking to realize she's gone.
咨询师：It sounds like those memories hold a special place in your heart, and it's completely natural to miss someone you shared a deep connection with. Remember, those memories can bring comfort and serve as a reminder of the love and bond you shared.
来访者：You're right, but it's so hard without her. I just feel lost and empty.
咨询师：I can imagine how overwhelming it must feel. Losing a best friend can leave a great void in your life. It's okay to feel lost and empty. Allow yourself to grieve and lean on your support system during this difficult time.
来访者：It's just tough to picture my life without her. She was always there for me, and now she's gone.
咨询师：I understand how hard it is to imagine a life without your best friend by your side. It's a process that takes time. Little by little, you'll find moments of joy amidst the sadness. Your friend's memory will always be a part of you, guiding you as you navigate this new chapter.
```

**response（来访当前句）**

```text
I hope so. I wish she could have been here to share all the important moments in my life.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-190. `extes_2231_5` — 阻抗 | Coping with the illness or death of a loved one

- **scene**：Coping with the illness or death of a loved one
- **description**：My uncle recently passed away after a long battle with cancer. I am feeling overwhelmed with sadness and struggling to come to terms with his loss.
- **binary_label**：阻抗

**context**

```text
来访者：I just keep thinking about all the things I wish I could have said to him before he passed. It's eating me up inside.
咨询师：Feeling regret and wishing you had done or said more is a common experience when dealing with the loss of a loved one. It may help to remember that your uncle knew you cared for him deeply.
来访者：You're right, but it's hard not to dwell on those thoughts. I miss him so much.
咨询师：I can only imagine how painful this must be for you. It's completely valid to feel the depth of that loss. Is there anything that brings you comfort during this time?
来访者：Talking with friends and family who also knew him brings some comfort, but it's still difficult to accept that he's no longer here.
咨询师：It's great that you're finding support from your loved ones. Grieving takes time, and it's okay to allow yourself to feel all these emotions. Your uncle meant a lot to you, and healing will come gradually.
```

**response（来访当前句）**

```text
Thank you for saying that. I just wish there was a way to cope with this pain more easily.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-191. `extes_2022_5` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long battle with illness.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, it was incredibly difficult to see him like that. I miss him so much.
咨询师：I can only imagine how heartbroken you must feel right now. Our pets bring such joy and love into our lives.
来访者：He was such a special part of our family. It's hard to imagine life without him.
咨询师：I completely understand. Pets become like family to us, so it's natural to grieve their loss deeply. Remember that you gave your dog a loving and caring home throughout his illness.
来访者：Thank you for saying that. It means a lot to me.
咨询师：I understand your pain. I once had a dog who battled an illness as well. It took time for me to accept the loss, but the memories I have of him help me treasure the time we had together.
```

**response（来访当前句）**

```text
I hope I can reach that point too. Right now, I just feel overwhelmed with grief.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-192. `extes_10936_3` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away after a long battle with a serious illness
- **binary_label**：阻抗

**context**

```text
来访者：I'm feeling so heartbroken. My dog passed away yesterday after a long battle with a serious illness. I miss him so much.
咨询师：I am so incredibly sorry for your loss. Losing a pet is devastating, especially after witnessing their long battle with illness. It's completely normal to feel heartbroken and miss your beloved companion.
来访者：Thank you, I just can't stop thinking about all the moments we shared. It hurts knowing he's not here anymore.
咨询师：I can imagine how much pain you're experiencing right now. Your dog was a true companion, and the memories you created together will always hold a special place in your heart. It's natural to feel a deep sense of loss and emptiness without their comforting presence.
来访者：Yes, he was always there for me. It's difficult to imagine life without him.
咨询师：It's completely understandable. The bond you formed was remarkable, and it's hard to adjust to the life changes that come with losing a beloved pet. Allow yourself to grieve and take the time to heal.
```

**response（来访当前句）**

```text
I feel guilty for not being able to save him, for not doing enough.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-193. `extes_1406_5` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. Sometimes it still feels like he's here, and then reality hits and it's hard to accept that he's gone.
咨询师：I completely understand. I remember after my dog passed away, I would catch myself looking for her and expecting her to come running. It's incredibly challenging to adjust to their absence after they've been such a big part of our lives for so long.
来访者：It really is. I'm trying to cope with the grief, but some days it feels overwhelming. Will it ever get easier?
咨询师：Grieving takes time, and everyone's journey is different. It's normal to have ups and downs. Over time, as you begin to cherish the happy memories you shared with your dog, the pain will become more bearable. Healing is a gradual process, and you're taking the right steps by acknowledging your emotions.
来访者：Thank you for reassuring me. The pain is just so intense right now, but I'll hold on to those precious memories. Have you ever lost a pet?
咨询师：Yes, I have. I went through a similar experience when my cat passed away. It took me some time to be ready, but eventually, I adopted another furry friend. It was a way for me to honor the love and joy my previous pet brought into my life. When you feel ready, you may find comfort in opening your heart to another pet. Take the time you need, grief is different for everyone.
```

**response（来访当前句）**

```text
That's a nice thought. I'll definitely consider it in the future, but right now, I just want to process the loss. Sometimes, I blame myself for not being able to save him.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-194. `extes_20_4` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My cat passed away
- **binary_label**：阻抗

**context**

```text
来访者：She was 13 years old. We had shared so many wonderful moments together.
咨询师：It sounds like your cat was a true companion to you. What were some of your favorite memories with her?
来访者：One of my favorite memories was when she would curl up beside me while I worked. It was comforting to know she was always there for me.
咨询师：Having a furry friend by your side while working sounds truly special. It's amazing how pets provide us with such comfort and companionship.
来访者：Exactly, I miss her presence. It feels empty without her.
咨询师：I completely understand. Pets become such an integral part of our lives, and their absence can be deeply felt. It's normal to feel a sense of emptiness and loss after losing a beloved pet.
```

**response（来访当前句）**

```text
Thank you for understanding. I just hope this pain goes away soon.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-195. `extes_2262_4` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away unexpectedly and I'm feeling lost and heartbroken. He was my constant companion and filled my life with joy.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you. He brought so much happiness into my life and losing him feels like a big part of me is missing.
咨询师：Your dog was special to you, and the bond you shared was unique. It's absolutely okay to miss him and feel the void he left behind. Allow yourself the time and space to grieve.
来访者：I just can't shake off this overwhelming sadness. Every corner of my house reminds me of him.
咨询师：Dealing with grief can be incredibly challenging, and it may take some time to adjust to the absence of your furry friend. Have you found anything that brings you even a slight sense of relief during this difficult time?
来访者：Thinking and talking about all the happy memories and adventures we shared helps, but it's still hard to cope with the emptiness.
咨询师：It's completely understandable. Remembering the good times can be bittersweet, especially when you can't create new ones. It's okay to feel a mix of sadness and joy when you reminisce. You gave your dog a wonderful life, and those memories are a testament to the beautiful bond you had.
```

**response（来访当前句）**

```text
Sometimes, I find it difficult to accept that he's really gone.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-196. `extes_169_6` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My cat died suddenly
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for saying that. It's just hard not to blame myself.
咨询师：I know it's easier said than done, but I want to remind you that you did everything you could. Pets bring us so much joy during their lives, and it's natural to feel this overwhelming sadness when they're no longer with us. Give yourself time to grieve and be gentle with yourself.
来访者：It's just difficult to imagine life without her. She was always there for me and provided so much comfort.
咨询师：I can only imagine how much you miss her presence. Pets have a unique way of bringing comfort, companionship, and unconditional love into our lives. The loss of such a special bond is incredibly painful.
来访者：Exactly, she was like family to me. Everything feels so empty now.
咨询师：It's completely understandable to feel emptiness and a sense of loss without your cat. Pets hold a special place in our hearts, and their absence can leave a void that is not easily filled. Just remember, in time, the pain will become more manageable, and you'll be able to cherish the beautiful memories you shared with your cat.
```

**response（来访当前句）**

```text
I hope so. It's just really hard right now. I can't stop crying.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-197. `extes_10215_5` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away unexpectedly
- **binary_label**：阻抗

**context**

```text
来访者：I miss everything about him. His playful personality, the way he greeted me when I came home, and how he always knew how to comfort me when I was sad.
咨询师：It's completely natural to miss all those wonderful qualities that made Buddy who he was. Losing a pet means losing a family member, and the void they leave behind can be incredibly difficult to fill. Is there anything you'd like to remember or any experiences you'd like to share?
来访者：One thing I'll never forget is his love for car rides. He used to get so excited and his tail would wag like crazy. Those were some of the happiest moments we shared.
咨询师：Those car rides must have been full of pure joy and happiness. It's beautiful that you got to experience those moments with him. Remember that the love and bond you shared with Buddy can never be taken away. He will always hold a special place in your heart.
来访者：You're right. I'll always treasure those memories. But I can't help feeling guilty that I didn't get to say goodbye or be there with him when he passed.
咨询师：Guilt is a common emotion when faced with the loss of a pet. Please know that Buddy knew how much you loved him, and he felt your love every day. It's normal to wish for a different outcome or to have regrets when we lose someone we care about. Be gentle with yourself and remember the love and care you provided throughout his life.
```

**response（来访当前句）**

```text
Thank you for your kind words. I'm trying my best to cope, but the sadness keeps overwhelming me.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-198. `extes_10589_6` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：I recently lost my dog in a sudden accident and I'm feeling devastated
- **binary_label**：阻抗

**context**

```text
来访者：You're right. I'm trying to focus on the happy memories, but it's still painful.
咨询师：Absolutely! Your grief is completely valid, and it's important to allow yourself to feel all the emotions that come with it. Take your time and don't rush the healing process.
来访者：Thank you. It's just hard not having him around.
咨询师：I can understand how difficult it must be for you. Is there anything else you'd like to share or discuss about your dog, Max?
来访者：Yes, I've been feeling guilty lately. I keep thinking about what I could have done differently that day to prevent the accident.
咨询师：It's common to experience feelings of guilt and what-ifs after such a traumatic loss. Please remember that accidents can happen unexpectedly, and it's not your fault. You provided a loving home and did everything you could to keep Max safe.
```

**response（来访当前句）**

```text
I appreciate your kind words. I just wish I could turn back time.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-199. `extes_1384_2` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：My dog passed away unexpectedly
- **binary_label**：阻抗

**context**

```text
咨询师：Hey there, how are you feeling today?
来访者：Not too great. My dog passed away unexpectedly a few days ago, and I'm really struggling with the grief and sadness.
咨询师：I'm so sorry for your loss. Losing a beloved pet can be incredibly painful. Was there anything specific that happened?
来访者：Thank you for being understanding. He suddenly fell ill and unfortunately, we couldn't do anything to save him. It hurts so much.
咨询师：I can't even imagine how devastating it must be to lose your dog like that. It's heartbreaking when we are unable to help them. Give yourself some time to grieve and remember that you loved and cared for him.
```

**response（来访当前句）**

```text
I feel so guilty. Maybe if I had noticed earlier or done something differently, he would still be here.
```

**raw_output（若有，节选）**

```text
阻抗

# 解释：
阻抗行为
```

---

### A-200. `extes_1416_3` — 阻抗 | Dealing with the Loss of a Pet

- **scene**：Dealing with the Loss of a Pet
- **description**：I recently lost my beloved dog
- **binary_label**：阻抗

**context**

```text
来访者：Not great, to be honest. I recently lost my beloved dog. He was my best friend and losing him has been incredibly tough.
咨询师：I'm really sorry to hear that. Losing a furry friend who's been your best friend can be incredibly tough. Tell me more about your dog, what was his name?
来访者：Thank you for your kind words. His name was Buddy, and he was the most loyal and loving companion I could have asked for. It's so hard to imagine life without him by my side.
咨询师：Buddy sounds like a wonderful and cherished member of your family. Losing such a special companion is never easy, and it's natural to feel a deep sense of loss and emptiness.
来访者：Yes, his absence has left a void in my heart. I miss his warmth and companionship.
咨询师：Losing a pet can truly leave a void in our lives. I remember when I lost my cat, I felt the same way. It will take time, but eventually, the pain will become more bearable, and you'll be left with beautiful memories.
```

**response（来访当前句）**

```text
I hope so. Right now, it hurts too much. I can't stop thinking about all the amazing moments we shared.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-201. `extes_2519_8` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I recently went through a breakup with my long-term partner and I'm feeling really down and hopeless. We were together for so long and now I feel lost.
- **binary_label**：阻抗

**context**

```text
来访者：I wish I could fast forward through this pain. It feels like it'll never get better.
咨询师：I understand how it may seem that way right now, but remember that pain is temporary and healing takes time. Over time, you will grow stronger and discover new joys in life. Each day brings opportunities for growth and self-discovery.
来访者：I hope you're right. Right now, I just can't imagine being happy again.
咨询师：I completely understand why it's difficult to envision happiness right now. Just know that it's okay to feel this way. Healing happens in small steps, and I'm here to support you through them.
来访者：Thank you, I really appreciate that. Do you have any suggestions on how to start moving forward?
咨询师：There are various ways you can start the healing process. It might help to focus on self-care and give yourself permission to grieve. Engaging in activities you enjoy, such as hobbies or spending time with loved ones, can also provide a source of comfort.
```

**response（来访当前句）**

```text
I'll try to do that, but everything just feels so overwhelming right now.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-202. `extes_10758_4` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：Lately, I've been feeling overwhelmed and unmotivated. I recently lost my job and it's been difficult to find new opportunities. I'm struggling with self-doubt and it's impacting my overall mood and confidence.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, it's been a tough few weeks. I lost my job and it's been hard to stay positive. I feel like my confidence is taking a hit.
咨询师：I'm really sorry to hear that. Losing a job can be emotionally draining and it's completely valid to feel overwhelmed and struggle with your confidence. Can you share more about how it's been impacting you?
来访者：It's been tough to wake up every day with no sense of purpose. And the constant job rejections make me question my abilities and worth. It's hard to see a way out of this situation.
咨询师：I can understand how the lack of purpose and constant rejections can be demoralizing. It must be challenging to not see a way out at the moment. Is there anything specific that you find most difficult to handle in this situation?
来访者：The uncertainty of the future is what's really getting to me. Not knowing when I'll find a job and feeling like I'm losing control over my life is hard to deal with. It's affecting my self-esteem and overall mood.
咨询师：I can only imagine how difficult it must be to deal with the uncertainty and loss of control. It's completely understandable why it would impact your self-esteem and mood. Remember, you're not alone in this. Many people face similar challenges during job transitions, and it's important to keep hope alive. Have you been able to reach out to your network or explore different job opportunities?
```

**response（来访当前句）**

```text
I've been trying, but the constant rejections make it hard to stay motivated and keep searching. It's like my confidence takes a hit with every rejection email.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-203. `extes_9085_4` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I recently lost my job and have been feeling extremely down and hopeless. The financial stress is starting to take a toll on me, and I don't know how to pull myself out of this dark place.
- **binary_label**：阻抗

**context**

```text
来访者：I'm not doing well at all. I feel lost and can't seem to shake off this negative mindset. I just don't know what to do anymore.
咨询师：I'm here to support you. It sounds like you're going through a really tough time. Could you tell me more about how you're feeling?
来访者：I just hate the fact that I lost my job. It was my only source of income, and now I'm struggling to make ends meet. I've been applying for jobs, but haven't had much luck so far. It's making me feel worthless.
咨询师：Losing a job can be incredibly hard, both financially and emotionally. It's completely normal to feel overwhelmed and down. You are not alone in this.
来访者：I feel like I'm stuck in a never-ending cycle of rejection. Every job opportunity feels like a dead end, and it's really starting to affect my self-esteem.
咨询师：The job search process can be disheartening and frustrating. It takes a toll on your confidence. Have you considered exploring any other career options or reaching out to your network for support?
```

**response（来访当前句）**

```text
I've been trying to stay positive and keep an open mind, but it's becoming increasingly difficult. I've reached out to friends, but they don't seem to understand what I'm going through.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-204. `extes_213_8` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately because I lost my job and I'm struggling with financial difficulties. It's been hard to stay positive and motivated.
- **binary_label**：阻抗

**context**

```text
来访者：That would be really helpful. Thank you. I didn't realize there were organizations specifically for this. I guess I just need a little guidance and support right now.
咨询师：Of course, I'm here to help. Let's start by looking for local job assistance organizations in your area. Do you mind sharing your location with me?
来访者：I'm currently located in Los Angeles, California.
咨询师：Great! I'll do some research and find job assistance organizations in Los Angeles for you. While I'm doing that, I want you to remember that you're stronger than you think, and you have the ability to overcome these challenges. There are options out there, and with a little support, you can find a way forward. Is there anything else you'd like to talk about or any particular concerns you'd like me to address while I gather the information?
来访者：Thank you, that means a lot to hear. Actually, I've been feeling quite lonely lately. The loss of my job has also affected my social life and I feel disconnected from my friends.
咨询师：I can understand how losing your job can have an impact on your social life and lead to feelings of loneliness. It's difficult to stay connected when facing such challenges. Have you considered reaching out to your friends and sharing your feelings with them?
```

**response（来访当前句）**

```text
I haven't really opened up to them about what I've been going through. I guess I'm scared that they won't understand or that they'll judge me.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-205. `extes_64_5` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I recently lost my job and have been feeling really down and hopeless. I'm struggling to find motivation to get back on my feet and it's affecting my self-esteem.
- **binary_label**：阻抗

**context**

```text
来访者：I recently lost my job and it's been hard for me to find another one. It feels like all my efforts are going to waste and I'm starting to doubt myself
咨询师：Losing a job can be really tough. It's understandable that you would feel discouraged right now. Have you been actively looking for new job opportunities?
来访者：Yes, I've been applying to multiple positions every day, but so far, I haven't had much luck. It's really starting to affect my self-esteem
咨询师：I can imagine how frustrating that must be. It's important to remember that finding a new job takes time, especially given the current circumstances. Just know that you're not alone in feeling this way
来访者：I know, but it's just hard to stay positive when nothing seems to be working out. I feel like I'm stuck in this cycle of negativity
咨询师：I completely understand how you feel. It's natural to have moments of doubt and negativity, especially during challenging times. But I genuinely believe that things will get better for you
```

**response（来访当前句）**

```text
I hope so. It's just difficult to see past my current situation
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-206. `extes_200_6` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling down lately. It's hard to find motivation and everything feels like a chore.
- **binary_label**：阻抗

**context**

```text
来访者：I know, but it's frustrating. I want to get back to feeling like myself again and finding joy in things.
咨询师：Absolutely, it's completely understandable to feel frustrated. It sounds like you really want to make positive changes in your life. Is there anything specific causing these feelings or any recent events that might be contributing to this low mood? I'm here to listen.
来访者：I've been going through a breakup recently, which definitely triggered my low mood. It's been hard to deal with the ending of the relationship.
咨询师：Breakups can be really challenging and can definitely have a major impact on our mood. It's completely natural to feel down and mourn the loss of a relationship. Allow yourself the time to grieve and heal through this process. It's okay to not be okay.
来访者：Thank you, that means a lot to hear. It's just difficult to move on and let go.
咨询师：You're welcome. Moving on and letting go can be incredibly hard, especially when we invest so much of our time and emotions into a relationship. Give yourself permission to feel what you're feeling right now. Are there any support systems or coping mechanisms that have helped you in the past during tough times?
```

**response（来访当前句）**

```text
Writing in my journal and talking to close friends usually helps. But lately, it seems like nothing eases these feelings.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-207. `extes_214_3` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I recently lost my job and I'm feeling really down and hopeless. It's been hard to find motivation to search for new opportunities and I'm worried about my financial situation.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I'm feeling really depressed lately.
咨询师：Hi there, I'm sorry to hear that you're feeling depressed. What's been going on?
来访者：I recently lost my job and I'm feeling really down and hopeless.
咨询师：Losing a job can be incredibly tough and it's normal to feel down and hopeless right now. I'm here for you. Have you been able to find any new job prospects?
来访者：It's been hard to find motivation to search for new opportunities and I'm worried about my financial situation.
咨询师：I understand. It can be challenging to maintain motivation when facing uncertainty and financial worries. How have you been coping with these feelings so far?
```

**response（来访当前句）**

```text
Honestly, I've just been isolating myself and avoiding thinking about it.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-208. `extes_218_5` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I recently lost my job due to the pandemic and have been feeling hopeless and stuck in a cycle of negativity. Every day feels like a struggle to find motivation or purpose.
- **binary_label**：阻抗

**context**

```text
来访者：It's just that I had worked so hard to build my career, and now it feels like all my efforts were for nothing. I'm constantly worried about money and the uncertainty of the future.
咨询师：It must be incredibly disheartening to feel like the work you put in was all for nothing. I can imagine that the financial stress and uncertainty about the future are weighing heavily on you. Have you been able to explore any other job opportunities?
来访者：I've been applying to various jobs, but the job market is so competitive right now. It feels like no matter how much effort I put in, there's always someone more qualified or experienced. It's starting to make me doubt my abilities.
咨询师：I completely understand how frustrating and demoralizing that can be. The current job market is indeed challenging, and it's easy to question your own worth when facing rejection. Just remember that setbacks are a natural part of the journey, and it doesn't define your abilities or potential.
来访者：I appreciate your support, but it's just hard to stay positive when I keep facing rejection. I find myself getting caught in negative thought patterns and it's affecting my overall well-being.
咨询师：I hear you, and it's completely normal to feel discouraged in the face of repeated rejections. However, it's important to challenge those negative thoughts and remind yourself of your strengths and past achievements. Try to shift your focus towards self-care and activities that bring you joy, even if it's just for a little while each day.
```

**response（来访当前句）**

```text
I'll try, but sometimes it feels so overwhelming. I feel like I've lost my sense of purpose and direction.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-209. `extes_2431_3` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling constantly overwhelmed and exhausted lately. My workload has been piling up, and I'm struggling to manage my responsibilities while also taking care of myself.
- **binary_label**：阻抗

**context**

```text
来访者：Hey! How's it going?
咨询师：Hi there! I'm here for you. How have you been feeling lately?
来访者：Honestly, I've been feeling really overwhelmed. It feels like there's so much on my plate, and I can't keep up with it all. I constantly feel exhausted and drained.
咨询师：I'm sorry to hear that. Feeling overwhelmed with a busy workload can definitely take a toll on your mental and physical well-being. It's important to prioritize self-care and find ways to manage the stress. Is there anything specific that's been causing extra stress or taking up most of your time?
来访者：Yeah, work has been piling up recently, and it feels like there's no end in sight. I've been working late nights and weekends, but it still feels like I'm falling behind.
咨询师：It sounds like work has become quite demanding and consuming for you, leaving little room for a healthy work-life balance. The pressure to constantly catch up can be overwhelming. Have you spoken to anyone at work about the workload or potential ways to lighten it?
```

**response（来访当前句）**

```text
I haven't really talked to anyone about it. I guess I've been trying to handle things on my own and don't want to burden anyone else with my problems.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-210. `extes_2533_3` — 阻抗 | Depression and Low Mood

- **scene**：Depression and Low Mood
- **description**：I've been feeling really down lately because I recently went through a breakup and I'm struggling to move on. It feels like my whole world has been turned upside down and I can't stop thinking about my ex.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, how's it going?
咨询师：Hi there! I'm here for you. How have you been holding up?
来访者：Honestly, not great. I've been feeling really sad and heartbroken since my breakup. It's been really tough to move on.
咨询师：I'm really sorry to hear that. Going through a breakup can be incredibly difficult, especially when you're still reminiscing about your time together. It's completely natural to feel sad and heartbroken.
来访者：Yeah, it just feels like I'll never be able to find happiness again. I keep replaying all the good times in my head.
咨询师：I understand how challenging it can be to let go of those memories. But remember, healing takes time, and it's okay to grieve the loss of the relationship. Eventually, you'll be able to create new beautiful memories.
```

**response（来访当前句）**

```text
I know, but right now it feels impossible to imagine a future without them.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-211. `extes_10985_4` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently graduated from college and started my first job. However, I'm finding it difficult to manage my expenses and save money. I feel overwhelmed and stressed about my financial future.
- **binary_label**：阻抗

**context**

```text
来访者：Thanks, I really appreciate that. So, I just started my first job after college, but it's been challenging to handle my expenses. I feel like I'm barely making ends meet and it's causing a lot of stress.
咨询师：I understand how overwhelming it can be to adjust to new financial responsibilities. Starting a job and managing expenses can be quite challenging. Is there anything specific that's been causing the most stress for you?
来访者：Mainly, it's the feeling of not having enough money left after paying my bills. I try to budget and cut costs where I can, but it still feels like I'm not making enough progress.
咨询师：It sounds like you're feeling frustrated and discouraged about not seeing the financial progress that you were hoping for. It can be disheartening, especially when you're working hard to stay within a budget. Is there anything else that's been weighing on your mind?
来访者：Apart from the financial pressure, I also worry about my future. I feel like I should be saving more and investing for the long term, but I'm not sure where to start. It's adding to my anxiety.
咨询师：I hear your concern about planning for the future and feeling uncertain about how to save and invest. It's completely normal to feel overwhelmed by these decisions, especially when you're just starting out. Have you considered seeking professional advice or doing some research on personal finance management?
```

**response（来访当前句）**

```text
I haven't really looked into professional advice because I'm worried about the cost. I also find it confusing to understand all the investment options out there. It all feels so overwhelming.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-212. `extes_11003_2` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I'm struggling to make ends meet. I'm feeling anxious and overwhelmed about my financial situation and I don't know how to handle it.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I'm really stressed out right now. I just got laid off from my job and I don't know how I'm going to pay my bills. I feel like everything is falling apart.
咨询师：I'm really sorry to hear that you're going through this tough situation. Losing a job can be really challenging, especially when you have financial responsibilities. It's completely normal to feel stressed and overwhelmed right now. I'm here to offer support and provide some suggestions if you'd like.
来访者：Thank you for understanding. I don't know what to do. I've been applying for jobs, but nobody seems to be hiring. It's really discouraging.
咨询师：I can imagine how frustrating and discouraging that must be. The job market can be tough sometimes, especially during uncertain times. But don't lose hope, there are opportunities out there. It might take some time, but your persistence and determination will pay off.
```

**response（来访当前句）**

```text
I hope you're right. I just can't stop worrying about how I'm going to pay my bills and make ends meet. It feels like I'm drowning in debt.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-213. `extes_10670_4` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently had unexpected medical expenses and I'm feeling overwhelmed with financial worries. I'm struggling to pay off debts and it's causing a lot of stress in my life.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, not so great. I've been dealing with some financial difficulties lately. I had some unexpected medical expenses and I'm finding it hard to manage my debts. It's really stressing me out.
咨询师：I'm sorry to hear that. Dealing with unexpected expenses and financial burdens can be incredibly overwhelming. It's completely understandable why you're feeling stressed. Can you tell me more about the situation and what it's been like for you?
来访者：Well, I recently had a health issue that required medical treatment. I didn't anticipate the costs involved, and now I have a significant amount of debt to pay off. I feel like I'm drowning and it's impacting my mental well-being.
咨询师：I can imagine how overwhelming that must be. It's not easy to face unexpected medical expenses, especially when they create a burden of debt. It's completely normal to feel overwhelmed and stressed. Have you explored any options to help manage these expenses?
来访者：I've tried to look for additional sources of income, but it's been difficult to find something that fits my schedule and pays well enough.
咨询师：I hear you. It sounds like you've been actively searching for solutions, but it hasn't been easy to find suitable options. It's frustrating when efforts to improve the situation don't yield immediate results. Is there anyone in your life you can talk to about your financial concerns or anyone who might be able to offer support or guidance?
```

**response（来访当前句）**

```text
I have a few close friends who I trust, but I've been hesitant to open up about my financial situation. I don't want to burden them or feel judged.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-214. `extes_2349_2` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently received a huge medical bill that I wasn't expecting. It's causing a lot of stress and I'm not sure how I'm going to pay for it. I need some emotional support and guidance.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I hope you're doing well. I've been feeling really overwhelmed lately. I just got hit with a huge medical bill that I wasn't expecting and I have no idea how I'm going to pay for it. It's causing so much stress and anxiety.
咨询师：Hi there, I can understand why receiving a medical bill out of the blue would be incredibly stressful. It's natural to feel overwhelmed and anxious in this situation. I'm here to listen and support you. How are you holding up?
来访者：Thank you for understanding. It just feels like a huge weight on my shoulders. I don't have the financial resources to cover such a big expense. I'm not sure what to do.
咨询师：I can imagine how overwhelming it must be to face such a huge financial burden. It's not easy to come up with large amounts of money unexpectedly. It's completely understandable that you're feeling stressed and uncertain. Have you explored any options for financial assistance or payment plans with the medical provider?
```

**response（来访当前句）**

```text
I haven't looked into it yet. I'm not even sure where to begin. I feel so lost and helpless.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-215. `extes_1820_3` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and now I'm struggling to pay my rent. It's causing a lot of stress and anxiety.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, do you have a minute? I could really use someone to talk to.
咨询师：Of course, I'm here for you. What's going on?
来访者：I just got laid off from my job and I'm really worried about how I'm going to pay my bills. It's causing so much stress and I don't know what to do.
咨询师：I'm really sorry to hear that. Losing a job can be incredibly stressful, especially when it comes to financial responsibilities. It's completely understandable that you're feeling overwhelmed.
来访者：Yeah, it's been really tough. I've been trying to find another job, but it's not easy right now. I'm worried about falling behind on rent and not being able to make ends meet.
咨询师：It sounds like you're feeling the pressure to meet your financial obligations. Have you considered reaching out to your landlord to discuss your situation and see if they can offer any flexibility or temporary solutions?
```

**response（来访当前句）**

```text
I haven't thought about that. But I'm afraid they might not be understanding and could even kick me out if I can't pay the rent.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-216. `extes_1815_2` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently invested a large sum of money in a business venture that failed. Now I'm facing financial difficulties and I don't know how to recover from this loss.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, I've been going through a really tough time lately. I made a big investment in a business that didn't work out, and now I'm in a lot of debt. I'm not sure how to bounce back from this.
咨询师：I'm really sorry to hear about that. It must be incredibly stressful and overwhelming to be dealing with financial difficulties due to a failed investment. Please know that I'm here to listen and support you. How are you holding up?
来访者：Thanks for understanding. It's been really hard to sleep at night knowing the debt keeps piling up. I feel like such a failure for making such a bad decision.
咨询师：I can imagine why you'd feel that way, but please remember that making a bad investment doesn't define your worth or intelligence. It's common for people to encounter financial setbacks or make mistakes. You took a risk, and although it didn't work out as planned, it's courageous of you to have tried. You're not alone in going through difficulties, and I'm here to help you navigate through this trying time. It takes strength to reach out and talk about it.
```

**response（来访当前句）**

```text
I appreciate you saying that. It's just hard to see a way out of this situation. The debt feels suffocating, and I can't even think about future investments anymore.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-217. `extes_351_3` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：My partner and I are struggling with our finances and don't know how to make ends meet. The constant stress is taking a toll on our relationship, leading to frequent arguments and disagreements.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, how are you doing?
咨询师：Hi, I'm good, thank you. How about you?
来访者：I'm not doing so great. My partner and I are going through a really tough time with our finances, and it's putting a lot of strain on our relationship.
咨询师：I'm really sorry to hear that. It must be incredibly challenging for both of you to navigate through such difficult financial circumstances. How are you coping with the stress?
来访者：Honestly, it's been really tough. We're constantly worrying about bills, debts, and not knowing when we'll be able to find stable jobs. We find ourselves arguing more often, and it feels like we're both at our breaking point.
咨询师：I can imagine how the constant pressure and uncertainty could take a toll on your relationship. It's completely understandable that both of you are feeling overwhelmed and on edge. Have you tried discussing your concerns openly with your partner?
```

**response（来访当前句）**

```text
We have, but it always ends the same way—with heated arguments and hurtful words. It's like we're both too stressed and exhausted to have a calm conversation anymore.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-218. `extes_671_5` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：My best friend and I both lost our jobs and are struggling to pay our bills. We're feeling overwhelmed and uncertain about the future.
- **binary_label**：阻抗

**context**

```text
来访者：I've been applying to every job I can find, but it seems impossible to even get an interview. It feels like I'm stuck in this cycle of filling out applications and hearing nothing back.
咨询师：That can be really disheartening. It shows your determination that you keep pushing forward. Have you considered reaching out to any job placement agencies or networking with friends and family?
来访者：I haven't thought about job placement agencies. That's a good idea. As for networking, I feel embarrassed to ask for help. I don't want anyone to think I'm desperate.
咨询师：It's completely understandable that you might feel embarrassed, but remember that seeking help doesn't make you desperate. Many people have been in similar situations and understand how tough it can be. Your friends and family would want to support you.
来访者：You're right. I should try to reach out for assistance. It's just hard to admit that I need help.
咨询师：Taking that step can be really difficult, but it's also a sign of strength. It shows you're willing to do whatever it takes to overcome this challenge. I believe in you.
```

**response（来访当前句）**

```text
Thank you for your encouragement. It means a lot to me. How about you? Are you going through something similar?
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-219. `extes_10993_5` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I am struggling to pay my bills. My partner and I have been fighting a lot because of the financial stress. I feel overwhelmed and don't know what to do.
- **binary_label**：阻抗

**context**

```text
来访者：We've been arguing a lot lately. My partner thinks I should have saved more money and they are frustrated. I understand their point, but I couldn't foresee losing my job.
咨询师：I can understand why both of you may be feeling frustrated and stressed. It's easy for tensions to rise when there's a sudden change in financial circumstances. Have you had a chance to sit down and talk about your concerns?
来访者：We've tried, but our conversations always turn into arguments. It's like we're trapped in this constant cycle of stress and anger.
咨询师：It must be really challenging to be stuck in a cycle of stress and arguments. It's important for partners to create a safe space where they can openly express their worries without judgment. Have you considered seeking external assistance, like a relationship counselor or therapist? They could help facilitate healthier, more productive conversations.
来访者：We haven't thought about that, but it's worth a try. Thank you for the suggestion.
咨询师：You're welcome! Seeking professional help can provide you with tools and strategies to improve communication and strengthen your relationship. Remember, many couples face hurdles, especially during difficult times. You're not alone in this journey.
```

**response（来访当前句）**

```text
That's reassuring to hear. But I'm still stressed about the financial situation. I don't know how I'm going to pay my bills and find another job.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-220. `extes_2336_6` — 阻抗 | Financial Worries and Uncertainty

- **scene**：Financial Worries and Uncertainty
- **description**：I recently lost my job and I'm struggling to find employment. The mounting bills and debts are causing a lot of stress and anxiety in my life. I feel overwhelmed and unsure of how to make ends meet.
- **binary_label**：阻抗

**context**

```text
来访者：I've been actively searching for jobs and applying to various positions, but I haven't had much luck. It feels discouraging and demotivating.
咨询师：I understand how frustrating it can be to face rejection or not hear back from employers. Remember, finding a job takes time, especially in challenging times like these. Your determination and perseverance are admirable, and I have no doubt that the right opportunity will come along. Is there anything else you've tried that might provide some relief?
来访者：I've tried cutting back on expenses and budgeting, but it still feels like it's not enough. The fear of not being able to meet my basic needs keeps looming over me.
咨询师：It's great that you've already taken steps to cut back on expenses. That's a smart move. Have you considered reaching out to local community resources or organizations that offer support in difficult financial times? They might have programs or assistance available to help alleviate some of the burden. Additionally, creating a detailed budget plan might provide a clearer understanding of your financial situation and potential areas where further adjustments can be made. Every small saving can add up and make a difference.
来访者：I haven't really explored community resources yet. Maybe I should start looking into that. Budgeting sounds like a good idea, but it feels daunting when there's so little to manage.
咨询师：I totally understand your concerns. It can be challenging to create a budget with limited resources, but it can also bring about a sense of control and clarity. By tracking your spending and identifying areas where you can make small adjustments, you might find ways to save even a little bit. Remember, every little saving counts. I believe in your ability to manage it. You're doing your best, and that's commendable.
```

**response（来访当前句）**

```text
Thanks for your support and encouragement. Sometimes I feel so overwhelmed and hopeless, like things will never get better.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-221. `extes_9076_4` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I'm currently in a relationship with someone who has bipolar disorder. They've been going through a depressive episode and I don't know how to support them through it. It's been really tough on both of us.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, I just want to be there for them, but it feels like nothing I do is making a difference.
咨询师：It's understandable that you're feeling frustrated and helpless. Supporting someone with bipolar disorder can be challenging, but your efforts do matter.
来访者：Thank you. I just wish I knew what else I could do to make them feel better.
咨询师：One thing you could try is gently encouraging your partner to engage in self-care activities they enjoy. It could be something as simple as going for a walk together or watching a movie they love.
来访者：That's a good idea. I'll suggest doing something relaxing together.
咨询师：That's great. Just remember that their depressive episode may make it difficult for them to find joy in activities, but your support and presence can still make a difference.
```

**response（来访当前句）**

```text
I'll keep that in mind. It's just hard seeing them like this.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-222. `extes_2191_9` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've recently started a new job, and I'm finding it challenging to manage my bipolar disorder symptoms while trying to excel and fit in at work. I feel overwhelmed, and it feels like my disorder is holding me back from performing well.
- **binary_label**：阻抗

**context**

```text
来访者：It really is. Sometimes, I can't predict when my mood swings will happen, and it's embarrassing.
咨询师：It's completely understandable that you feel embarrassed. However, it's important to remember that bipolar disorder is a medical condition, and you have no control over when or how your moods fluctuate. It's not something to be ashamed of.
来访者：You're right. I need to remind myself of that. Are there any techniques that could help me improve my concentration?
咨询师：Of course! One technique you could try is breaking tasks into smaller, manageable chunks. This helps to make your workload feel less overwhelming. Additionally, using tools like time management apps or setting reminders can also be helpful in staying on track.
来访者：I'll give those techniques a try. Hopefully, they'll make a difference.
咨询师：That's a positive mindset! Remember, it may take some trial and error to find the strategies that work best for you. But stay persistent, and you'll eventually discover what helps you stay focused and productive.
```

**response（来访当前句）**

```text
I also struggle with maintaining a work-life balance due to my symptoms. It feels like I'm constantly under pressure and can't find time for myself or my loved ones.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-223. `extes_2479_7` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've been feeling extremely overwhelmed and anxious lately. My bipolar disorder is affecting my ability to concentrate and perform well at work. I'm worried about the impact it's having on my career.
- **binary_label**：阻抗

**context**

```text
来访者：Sometimes I worry that my bipolar disorder will hold me back in my career. I'm afraid I won't be able to meet expectations and it will negatively impact my future.
咨询师：It's understandable to have those concerns about how bipolar disorder may affect your career. Can you share more about what specifically worries you?
来访者：I've worked so hard to get this opportunity, and now I feel like my condition is holding me back. I'm scared of disappointing myself and others.
咨询师：Your fears are completely valid, but I want to remind you that you are not defined by your bipolar disorder. You have so much to offer, and this setback does not define your future success.
来访者：Thank you for reminding me of that. Sometimes I forget.
咨询师：Have you considered having an open conversation with your supervisor about your bipolar disorder? They might be understanding and able to provide you with the support you need to succeed in your role.
```

**response（来访当前句）**

```text
I'm afraid of disclosing my condition. I don't want to be treated differently or stigmatized at work.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-224. `extes_384_3` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I'm a single parent with bipolar disorder, and I'm currently struggling to balance my work responsibilities with taking care of my two young children. The constant mood swings and fatigue make it difficult for me to be there for them both emotionally and physically. I feel overwhelmed and guilty about not being the best parent I can be.
- **binary_label**：阻抗

**context**

```text
来访者：I feel like I'm failing as a parent because of my bipolar disorder.
咨询师：It sounds like you're experiencing a lot of self-doubt and guilt. Can you tell me more about how you're feeling?
来访者：Yes, I constantly worry about not being able to provide my children with the stability and attention they need.
咨询师：It's completely understandable to have these concerns. Parenting is challenging, especially when you're managing bipolar disorder. Your awareness of their needs shows how much you care.
来访者：Thank you, but I can't help feeling like I'm failing them when I have a depressive episode.
咨询师：It must be incredibly tough to navigate through those depressive episodes while still trying to be there for your children. Your efforts are commendable, and it's important to remember that asking for help is a sign of strength.
```

**response（来访当前句）**

```text
I often worry that they'll grow up resenting me because of my mood swings.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-225. `extes_2179_4` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've been feeling overwhelmed lately due to my bipolar disorder. It's impacting my ability to perform well at work and I'm struggling to maintain a healthy work-life balance.
- **binary_label**：阻抗

**context**

```text
来访者：I'm having difficulty concentrating at work, and my productivity is suffering because of the mood swings. I also find it hard to create a healthy work-life balance because I'm constantly worried about my mental state and how it may affect my relationships.
咨询师：When you mention your relationships, do you mean your relationships with colleagues, friends, or family members?
来访者：I mainly struggle with maintaining healthy relationships with my colleagues and friends. It's hard to explain to them why I have these mood swings and why I may seem distant or disengaged at times.
咨询师：It sounds really tough to navigate these challenges, especially when it comes to your work and relationships. It's completely understandable to feel overwhelmed with everything you're managing. You're doing your best.
来访者：Thank you, I really appreciate your understanding. It's just frustrating because I want to excel at my job and maintain strong connections with my friends, but it feels like my bipolar disorder is holding me back.
咨询师：Despite the challenges, remember that you are not defined by your condition. You have many strengths and abilities. Working on managing the bipolar disorder is a step towards pursuing your goals and maintaining meaningful relationships.
```

**response（来访当前句）**

```text
I guess you're right. I have been trying different coping mechanisms, but sometimes it feels like they're not enough.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-226. `extes_387_5` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have recently been diagnosed with bipolar disorder and I'm struggling to manage my symptoms. I often experience extreme mood swings and it's affecting my relationships and daily life.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you, but it's exhausting and I feel like I'm losing control of my life.
咨询师：I can only imagine how overwhelming it must feel to not have control over your own emotions. It takes immense strength to deal with this on a daily basis.
来访者：It's hard to maintain stability in my relationships. I've pushed away friends and loved ones because of my unpredictable mood swings.
咨询师：I understand how challenging it can be to maintain relationships while managing bipolar disorder. You're doing the best you can in a difficult situation.
来访者：I just wish there was a way to manage it better. I feel like I'm constantly letting people down.
咨询师：Remember, managing bipolar disorder is a journey and it often requires a combination of medications, therapy, and lifestyle adjustments. You're not alone in this struggle, and with the right support and resources, it's possible to find stability.
```

**response（来访当前句）**

```text
I've started therapy, but it's just the beginning. I feel overwhelmed by the long road ahead.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-227. `extes_2455_4` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I'm a college student with bipolar disorder, and I am currently struggling to balance my academic responsibilities with managing my mental health. The constant mood swings and anxiety make it difficult for me to focus on my studies and maintain healthy relationships. I feel overwhelmed and unsure about how to navigate through this stage of my life.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, I find it hard to concentrate and stay motivated. Some days, I have so much energy that I can't focus, and other days, I feel so low that I can't bring myself to do anything.
咨询师：It's completely understandable to feel this way. Bipolar disorder can greatly impact your ability to perform academically. Have you reached out to your school's disability support services for accommodations?
来访者：No, I didn't even know that was an option.
咨询师：I would highly recommend looking into it. Your college may have resources in place to support students with disabilities, including bipolar disorder. They can provide accommodations like extra time on exams, deadline extensions, or even note-taking assistance.
来访者：That could be really helpful. I'll make sure to contact them and see what options are available to me.
咨询师：That's a great step towards getting the support you need. Remember, reaching out for help is a sign of strength, and it can make a significant difference in managing your academic workload. Additionally, have you considered developing a routine or setting some boundaries for yourself?
```

**response（来访当前句）**

```text
I've tried, but it's challenging to stick to a routine when my mood swings are unpredictable. It often derails my plans.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-228. `extes_2473_6` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have been diagnosed with bipolar disorder and have been experiencing frequent mood swings and difficulty maintaining stability in my life. I am feeling overwhelmed and unsure of how to cope.
- **binary_label**：阻抗

**context**

```text
来访者：It's been a struggle to find the right treatment and strategies to cope with my symptoms. I've tried different medications, but it feels like a continuous battle.
咨询师：Have you been able to speak with a healthcare professional who specializes in bipolar disorder? They can provide valuable insights and work with you to find effective treatment and coping strategies.
来访者：Yes, I've been seeing a psychiatrist, but it still feels overwhelming to find what works for me on a day-to-day basis. Some days, it's harder to cope than others.
咨询师：It's understandable that navigating the daily challenges of bipolar disorder can feel overwhelming. Have you explored any coping techniques or resources that might be helpful in managing your symptoms on a daily basis?
来访者：I've tried different things like establishing routines, practicing mindfulness, and journaling. They help to some extent, but it's still a constant struggle to find stability.
咨询师：It sounds like you're putting in a lot of effort to explore different coping techniques. It can be frustrating when progress is not linear, but please remember that finding stability with bipolar disorder often involves trial and error.
```

**response（来访当前句）**

```text
I know that, but sometimes it's just disheartening to feel like I'm taking one step forward and two steps back. I want to be able to enjoy things without constantly worrying about my next mood swing.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-229. `extes_2207_3` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I've been feeling really overwhelmed with my workload and it's been affecting my ability to concentrate and stay focused. I'm worried that my bipolar disorder is making it difficult for me to excel in my job.
- **binary_label**：阻抗

**context**

```text
来访者：I feel like I'm drowning in work. It's hard to keep up with the demands and I'm worried about falling behind.
咨询师：It sounds like you're feeling a lot of pressure and it's taking a toll on your work performance. Could you provide more details about the specific challenges you're facing?
来访者：I have constant deadlines to meet and the workload keeps piling up. It feels like I can never catch a break. On top of that, I'm having trouble focusing because my mood swings make it hard to concentrate.
咨询师：It sounds like the combination of deadlines and mood swings is making it overwhelming for you. Are there any particular tasks or responsibilities that are causing the most stress?
来访者：I struggle with time management and prioritizing tasks. It's hard to keep everything organized and I often feel like I'm running out of time. The pressure to perform well only adds to the stress.
咨询师：It sounds like you have a lot on your plate and it's completely understandable that it's causing stress. You're doing your best in a challenging situation.
```

**response（来访当前句）**

```text
Thank you, but I can't help but worry that I won't be able to meet expectations. I feel like my bipolar disorder is holding me back.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-230. `extes_2196_2` — 阻抗 | Managing Bipolar Disorder

- **scene**：Managing Bipolar Disorder
- **description**：I have recently been diagnosed with bipolar disorder and I'm struggling to manage my symptoms. I often experience extreme mood swings and it's affecting my relationships and daily life.
- **binary_label**：阻抗

**context**

```text
来访者：I just had a huge fight with my partner because of my mood swings. I feel like I'm ruining our relationship and I don't know how to fix it.
咨询师：It sounds like your mood swings are causing a lot of distress in your relationship. Can you give me more details about what happened?
来访者：We were having a nice day together, and suddenly I felt this overwhelming sadness and irritability. I ended up snapping at my partner and saying hurtful things. Now, they are upset and I feel guilty for my behavior.
咨询师：It must be incredibly challenging to navigate your emotions in a relationship and feel like you're not in control. The fact that you recognize the impact of your behavior shows self-awareness and a willingness to improve.
```

**response（来访当前句）**

```text
Thank you, but I don't want to keep hurting them.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-231. `extes_681_3` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Struggling to find a job after being laid off from a corporate position.
- **binary_label**：阻抗

**context**

```text
来访者：Hey there
咨询师：Hi! How are you doing today?
来访者：I'm hanging in there, but I've been feeling really down lately. I lost my job a few months ago and haven't been able to find a new one. It's been incredibly frustrating.
咨询师：I completely understand how difficult and demoralizing unemployment can be, especially when you've been actively searching. It's okay to feel frustrated and down about it. Can you tell me a little more about your job search experience?
来访者：Thanks for understanding. It's been tough navigating the job market. I've been applying to multiple positions every day, but the responses have been scarce. I've had a few interviews, but nothing has materialized into an offer yet.
咨询师：I can imagine how discouraging that must be after investing time and effort into each application. It can feel like your qualifications are being overlooked, but please remember that you have valuable skills and experience. Have you considered reaching out to any professional connections for leads or recommendations?
```

**response（来访当前句）**

```text
Yes, I've tried networking as much as possible. I've reached out to former colleagues and friends, but unfortunately, most of them weren't aware of any suitable openings. It's been disheartening.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-232. `extes_4907_4` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and demotivated after being laid off due to company downsizing
- **binary_label**：阻抗

**context**

```text
来访者：Hey, honestly not so great. I recently got laid off from my job due to downsizing, and I'm feeling really overwhelmed and demotivated.
咨询师：I'm really sorry to hear that. Losing a job can be incredibly tough, especially when it's unexpected. How are you coping with the situation?
来访者：To be honest, it's been really challenging. I feel like I've lost my sense of purpose and I'm worried about my financial stability.
咨询师：I can understand why you'd feel that way. Losing a job can have a profound impact on various aspects of our lives. It's completely natural to experience a sense of loss and uncertainty during this time.
来访者：Thank you for understanding. It's just been difficult to stay positive and motivated.
咨询师：I can imagine how hard it must be for you. It's completely valid to have moments of doubt and frustration. But please remember, this setback is temporary. You have skills and qualifications that will be valued by another employer in the future.
```

**response（来访当前句）**

```text
I appreciate your words of encouragement. It's just hard not to feel discouraged.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-233. `extes_2114_4` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and lacking motivation due to a long period of unemployment.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, I've been feeling really down lately. It's been months since I lost my job, and I've been struggling to find a new one. The constant rejections are taking a toll on my motivation.
咨询师：I hear you. It's completely normal to feel down and lose motivation during a long job search. Rejections can be disheartening, but please remember that it doesn't define your worth or abilities. Could you tell me a bit more about the challenges you've been facing?
来访者：It feels like no matter how many applications I send or interviews I attend, nothing seems to work out. I'm starting to doubt my skills and wonder if I'll ever find a job that suits me.
咨询师：I understand how frustrating and discouraging it can be. The job search process can be challenging and may lead to self-doubt. Remember that this is a common experience, and many people have faced similar struggles. Have you considered reaching out to any networking connections or exploring different industries?
来访者：I've been relying on online applications mostly. I haven't had much luck with my networking connections so far. As for exploring different industries, it feels overwhelming since I've only worked in one field for a long time.
咨询师：I understand feeling overwhelmed, especially when you've been in one field for a while. Have you ever had any interests or curiosity about other industries? It might be worth exploring those areas and seeing if any skills are transferable. Starting with something you're genuinely curious about can make the transition smoother.
```

**response（来访当前句）**

```text
Well, I have always been interested in graphic design, but I don't have any experience or formal education in that field. It feels like a huge barrier.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-234. `extes_4901_5` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Having difficulty finding a job in the marketing industry
- **binary_label**：阻抗

**context**

```text
来访者：It's been almost nine months now, and I've sent out numerous applications, but I haven't received any positive responses yet.
咨询师：I can only imagine how disheartening that must feel. It takes a lot of perseverance to keep going without any positive outcomes. Have you considered any alternative options in the meantime?
来访者：I've thought about it, but marketing is what I'm truly passionate about. I've studied and worked hard to build a career in this field.
咨询师：I understand your passion and dedication. It can feel even more challenging when you're aiming for a specific field. However, it's important not to give up. Keep pushing forward, and the right opportunity will come your way.
来访者：Thank you for understanding. It's just frustrating to see my efforts not paying off. It feels like everyone else is moving forward, while I'm stuck.
咨询师：I can imagine how frustrating and discouraging that must feel. But remember, everyone's journey is different, and success can come at different times for different people. You have unique skills and qualities that will shine when the right opportunity arises.
```

**response（来访当前句）**

```text
It's just hard staying positive when things don't go as planned. I don't want to lose my motivation.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-235. `extes_4905_3` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Having difficulty finding a job in the technology industry
- **binary_label**：阻抗

**context**

```text
来访者：Hey, how's it going?
咨询师：Hi there, what's been happening? Is everything alright?
来访者：Not really. I've been feeling really stressed out lately because I'm having a tough time finding a job in the technology industry.
咨询师：I understand how frustrating that must be. The tech job market can be highly competitive. Can you tell me more about how long you've been searching for a job and the challenges you've faced?
来访者：It's been almost a year now, and I've applied to numerous positions but haven't received any positive responses. It's really discouraging.
咨询师：That sounds incredibly disheartening. It takes a lot of effort and perseverance to keep applying without any results. Have you considered any alternative options during this time?
```

**response（来访当前句）**

```text
I've thought about it, but I'm really passionate about working in the tech industry. I've spent years building my skills and it's my dream career.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-236. `extes_4912_5` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Dealing with the emotional impact of being laid off and struggling to find a new job.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. It's been a rollercoaster of emotions. I feel stressed about paying my bills and supporting myself. It's been hard not having a sense of purpose.
咨询师：I can imagine how overwhelming all of this might be. Your financial concerns and missing a sense of purpose are valid. Have you tried exploring different job opportunities or any side gigs?
来访者：I've been applying to various jobs, but I haven't had much luck so far. It's discouraging to keep getting rejected.
咨询师：I understand how disheartening it can be. Rejections can take a toll on your confidence. Remember that it doesn't define your worth. It's important to keep pushing forward and stay hopeful.
来访者：I appreciate your support. It's just hard to stay positive when things seem uncertain.
咨询师：I completely understand. Uncertainty can make it challenging to stay positive. But it's important to believe that things will get better. Opportunities can arise unexpectedly. In the meantime, consider pursuing activities you enjoy and focus on self-care.
```

**response（来访当前句）**

```text
You're right. I should try to focus on things outside of job hunting. It's just tough to shake off the stress.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-237. `extes_4902_5` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Having trouble finding a job in the marketing industry
- **binary_label**：阻抗

**context**

```text
来访者：It's been about seven months now. I've sent out countless applications, gone to interviews, but haven't received any positive responses.
咨询师：Wow, seven months is a long time to be job hunting without any success. That must be really discouraging. Have you considered exploring other related fields or expanding your job search to different industries?
来访者：I've thought about it, but I'm really passionate about marketing. I've invested a lot of time and effort into building my skills in this field.
咨询师：I can understand how important marketing is to you. It's challenging to keep going when it feels like you're not getting any closer to your goals. However, don't lose hope just yet. Persistence is key, and sometimes it just takes a bit longer to find the right opportunity.
来访者：Thank you for understanding. It's just frustrating to see others moving forward while I'm stuck in place.
咨询师：I can imagine how disheartening and isolating that must feel. Try to remember that everyone's journey is different and success comes at different times for each person. You have unique skills and qualities that will make you stand out when the right opportunity comes along.
```

**response（来访当前句）**

```text
It's just hard to stay positive when things aren't working out. I don't want to lose my motivation.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-238. `extes_1832_3` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling discouraged after multiple rejections from job applications
- **binary_label**：阻抗

**context**

```text
来访者：Hi there
咨询师：Hello! How are you doing today? How can I help?
来访者：Hey, I'm feeling really down. I've been applying for jobs for months, but all I get is rejections. It's starting to make me doubt my skills and worth.
咨询师：I can understand how frustrating and discouraging it can be. Receiving multiple rejections is tough, but please remember that it doesn't define your skills or worth as a person. Rejection is often a common part of the job search process. Would you like to tell me more about your experiences?
来访者：Thank you for understanding. It just feels like I'm not good enough or that I've wasted so much time.
咨询师：I hear your frustration and self-doubt. It's completely normal to have these thoughts, but they don't reflect your true value. Many successful people have faced rejections before finding their ideal jobs. Remember, one setback doesn't define your entire career.
```

**response（来访当前句）**

```text
I appreciate your encouraging words, but it's hard to stay positive.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-239. `extes_10697_4` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Struggling to find a job after being laid off from a long-term position in marketing
- **binary_label**：阻抗

**context**

```text
来访者：I'm not doing so great, honestly. I recently got laid off from my job in marketing and I'm really struggling to find a new job.
咨询师：I'm really sorry to hear that. Losing a job can be incredibly tough and it's normal to feel stressed and uncertain about the future. Would you like to talk more about what you're going through?
来访者：Yeah, it's been really tough to handle. Marketing was my passion, and now I don't know what to do next.
咨询师：I can understand how you must be feeling, especially when your job aligned with your passion. Have you reached out to your professional network or considered different industries where your skills can be valuable?
来访者：I've been reaching out to my contacts, but it seems that opportunities are limited in the current market. I've also considered exploring other industries, but it's difficult to start from scratch.
咨询师：It's definitely frustrating when opportunities are scarce, and transitioning to a different industry can feel daunting. Remember, it's okay to take some time to assess your options and even gain new skills through online courses or workshops. Your experience and adaptability will be assets in any field.
```

**response（来访当前句）**

```text
You're right, maybe I should use this time to broaden my skills. But it's hard to stay positive when I keep getting rejection emails.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-240. `extes_2378_4` — 阻抗 | Unemployment-related stress

- **scene**：Unemployment-related stress
- **description**：Feeling overwhelmed and discouraged due to a long period of unemployment
- **binary_label**：阻抗

**context**

```text
来访者：Not so great actually. I've been struggling to find a job, and it's really been getting me down.
咨询师：That sounds really tough. Searching for a job can be challenging and can affect your mood. It's completely normal to feel down in this situation. Would you like to share more about how you've been feeling?
来访者：Yeah, it just feels like there are no opportunities out there for me. I've been applying to so many places but haven't heard back from anyone.
咨询师：It sounds like you're feeling discouraged and frustrated with the lack of responses. Is that right?
来访者：Exactly! It's disheartening to put in so much effort and not see any results.
咨询师：I completely understand how that feels. It can be really tough to stay motivated when you're not getting the responses you hoped for. Please remember that this doesn't define your worth or abilities. Have you tried exploring different job search strategies or networking?
```

**response（来访当前句）**

```text
I've tried different strategies, but nothing seems to be working. Networking is also a challenge for me.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-241. `extes_10608_3` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been struggling with excessive workload and lack of support at my job, which has resulted in severe stress and burnout.
- **binary_label**：阻抗

**context**

```text
来访者：Hi, how's it going?
咨询师：Hey! I'm here, ready to chat. How are you doing today?
来访者：To be honest, I've been feeling extremely overwhelmed and burnt out lately.
咨询师：It sounds like you're facing a lot of stress and burnout. Can you share more about what's been happening at work?
来访者：I've been working long hours and taking on more responsibilities without any additional support. It feels like I'm constantly drowning in work and it's taking a toll on my mental and physical health. I just don't know how to cope anymore.
咨询师：That sounds incredibly challenging and exhausting. It's tough when you have a heavy workload without the necessary support. Feeling burnt out is a common reaction to such circumstances, and it's important to take care of yourself.
```

**response（来访当前句）**

```text
Thank you for understanding. But it feels like this cycle is never-ending, and I can't see a way out.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-242. `extes_343_5` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been experiencing work-related stress and burnout lately. It's been overwhelming and I don't know how to cope with it.
- **binary_label**：阻抗

**context**

```text
来访者：I constantly have to meet tight deadlines, work long hours, and deal with a demanding boss. It's taking a toll on my mental and physical health.
咨询师：That sounds incredibly tough. It's understandable that you're feeling stressed and burnt out with such a workload.
来访者：Yes, it feels like there's no end in sight. I'm starting to lose motivation and passion for my job.
咨询师：I can understand how that would be discouraging. Remember that your feelings are valid and it's okay to feel this way.
来访者：Thank you for understanding. I really need some guidance on how to handle this situation.
咨询师：Of course! Have you considered talking to your boss about your workload? They may not be aware of the impact it's having on you.
```

**response（来访当前句）**

```text
I'm afraid of confronting my boss. I don't want to appear incapable or jeopardize my job.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-243. `extes_663_4` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed and burned out at work. I have been working long hours and it feels like I can't catch a break. I'm finding it hard to stay motivated and I feel like I have no work-life balance.
- **binary_label**：阻抗

**context**

```text
来访者：I'm not doing great. I've been feeling extremely stressed and burnt out at work.
咨询师：I'm sorry to hear that. It sounds like you're going through a difficult time. Can you tell me more about what's been happening?
来访者：I've been working long hours and constantly dealing with tight deadlines. It feels like I can never get a break. On top of that, there's no work-life balance and it's taking a toll on my overall well-being.
咨询师：I can understand how that can be really overwhelming. It's tough when work takes over and leaves you with no time for yourself. What kind of work do you do?
来访者：I work in marketing. I have a lot of responsibilities and it always feels like there's more work than I can handle on my own.
咨询师：So, you've been in this role for quite some time now, and it seems like the workload has been increasing. Have you spoken to your supervisor about your concerns? Maybe they can help allocate resources or provide some support.
```

**response（来访当前句）**

```text
I haven't really talked to my supervisor about it. I fear that they won't understand and instead expect more from me.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-244. `extes_10636_3` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed and burnt out at work. I have been working long hours and taking on too many responsibilities. The constant pressure is affecting my mental health, and I need someone to talk to.
- **binary_label**：阻抗

**context**

```text
来访者：Hi there, I've been feeling really stressed out and burnt out at work. It feels like there's an endless amount of work and I can't seem to catch a break. It's taking a toll on me mentally and emotionally.
咨询师：Hey, I'm here to listen. I'm sorry to hear that you're experiencing such high levels of stress. Can you tell me more about what's been happening at work?
来访者：I've been given multiple projects with tight deadlines, and it feels like I'm drowning in work. I can never catch up, and it's affecting my well-being. I feel like I'm constantly on edge and overwhelmed.
咨询师：I can imagine how overwhelming that must be for you. It sounds like you've been carrying a heavy load for quite some time now. Have you tried reaching out to anyone at work for support?
来访者：I haven't really reached out because the company culture is very competitive, and there's a lack of emphasis on employee well-being. It feels like we're expected to give our all without considering our mental health.
咨询师：I understand, it must be difficult to cope without any support systems in place. Would it be helpful to discuss your concerns with your manager or HR? They may be able to provide some guidance or suggestions.
```

**response（来访当前句）**

```text
I'm afraid that speaking up might have negative consequences for my career. I've seen others face backlash for expressing their struggles. It's a difficult situation to navigate.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-245. `extes_10638_4` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling extremely stressed and burnt out at work. I have a demanding boss who constantly gives me new tasks without considering my workload. I often work long hours and struggle to find a work-life balance.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, I've been feeling really overwhelmed with work. My boss keeps piling on more tasks, and I can't seem to catch a break. I feel exhausted and discouraged.
咨询师：It sounds like you're dealing with a lot of stress and pressure at work. Your boss's constant demands without considering your workload must be incredibly challenging and draining.
来访者：Yes, exactly. I don't know how to cope with this constant overload. It's affecting my mental and physical health. I feel drained all the time, and I don't have time for myself anymore.
咨询师：I want you to know that your feelings are valid. It's completely normal to feel overwhelmed and burnt out when facing an excessive workload. Taking care of your mental and physical well-being is crucial, especially in such demanding circumstances.
来访者：I appreciate your understanding. But I don't want to let my boss down or appear incapable of handling the workload. I'm torn between taking care of myself and meeting the expectations at work.
咨询师：I completely understand that dilemma. It's tough to balance meeting work expectations and prioritizing your self-care. Remember, your health and well-being should always come first. It's important to find ways to address this issue while also communicating your needs to your boss.
```

**response（来访当前句）**

```text
I don't feel comfortable speaking up to my boss. I'm afraid it may negatively impact my job security or future opportunities.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-246. `extes_10973_7` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I'm feeling extremely overwhelmed and burned out at work. The workload keeps piling up, and I can't seem to find a balance.
- **binary_label**：阻抗

**context**

```text
来访者：Not really. The company culture is very competitive, and there's not much emphasis on employee well-being. It's as if we're expected to give our all without considering our own mental and emotional health.
咨询师：So it sounds like there's a lack of support and understanding for employee well-being in your company. Do you think it would be helpful to have an open conversation with your manager or HR about your concerns?
来访者：I'm afraid that speaking up might negatively impact my career. I've seen others face consequences for expressing their struggles. It's a difficult situation to navigate.
咨询师：I completely understand your hesitation. It's important to consider the potential risks. However, it's also crucial to prioritize your own well-being. Have you thought about seeking a new job or exploring other opportunities?
来访者：I have considered it, but job opportunities are scarce right now. Besides, leaving my current position would mean starting from scratch in a new environment, which can be daunting. I just wish I could find a way to manage my stress and regain some balance.
咨询师：I understand your concern. Switching jobs can indeed be challenging, especially when opportunities are limited. In the meantime, focusing on self-care might help you cope with the stress. Have you tried incorporating any stress management techniques into your routine?
```

**response（来访当前句）**

```text
I've tried going for walks and practicing mindfulness, but it feels like I can't truly disconnect from work. The constant pressure is always at the back of my mind.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-247. `extes_10949_6` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been assigned a new project at work which has significantly increased my workload and expectations. I'm feeling overwhelmed and exhausted, and I don't know how to manage it all.
- **binary_label**：阻抗

**context**

```text
来访者：Thank you for understanding. I'm starting to doubt if I'm capable of handling this much work.
咨询师：It's important to remember that your capabilities aren't defined by the amount of work you can handle. It's concerning how your workload has escalated without considering your well-being. You have the skills and strengths needed, but everyone has their limits. This workload would be overwhelming for anyone.
来访者：I appreciate your reassurance. But I feel like I'm sacrificing my personal life and mental health for my job.
咨询师：You're not alone in feeling this way. Work-life balance is crucial for our overall well-being, and it's unfortunate that it's being compromised for you. Your concerns are understandable, and it's essential to find a healthier balance.
来访者：I wish there was a way to manage my workload better and still excel at my job.
咨询师：Have you considered having an open conversation with your supervisor about your increased workload and the toll it's taking on your well-being? It might be helpful to express your concerns and explore potential solutions together.
```

**response（来访当前句）**

```text
I'm hesitant to bring it up because I don't want to seem incapable or ungrateful for the opportunities.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-248. `extes_10626_5` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling very stressed and burned out at work lately. I have been given more responsibilities without any extra support, and it's becoming overwhelming. I feel like I can't catch a break and it's taking a toll on my mental health.
- **binary_label**：阻抗

**context**

```text
来访者：I feel like I've been given so many additional responsibilities without any support. The workload keeps increasing and I just can't handle it anymore. It's really affecting my mental health.
咨询师：It sounds like you're going through a lot of pressure and it's getting overwhelming. Can you share more about how this is impacting you?
来访者：I constantly feel exhausted and overwhelmed. It's like a never-ending cycle. I've talked to my manager about it, but they don't seem to understand.
咨询师：I can only imagine how challenging and draining that must be for you. Feeling supported and understood at work is crucial. Do you have any coworkers who could relate to what you're going through?
来访者：Unfortunately, I'm the only one in my team with this kind of workload. It's really isolating and I feel like I have no escape.
咨询师：I understand that feeling. In my previous job, I was also the only one with a heavy workload, and it often felt impossible to manage. It's incredibly tough and discouraging. Have you considered talking to your manager again, emphasizing how it's affecting your well-being?
```

**response（来访当前句）**

```text
I haven't tried bringing it up again. I'm worried they won't take me seriously or consider my need for a better work-life balance.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-249. `extes_10954_4` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed and burnt out at work. Lately, I have been assigned a lot of projects with tight deadlines, and I'm struggling to keep up. It feels like there's never enough time to complete everything, and it's affecting my mental well-being.
- **binary_label**：阻抗

**context**

```text
来访者：I'm not doing great. I've been feeling extremely stressed and burnt out at work.
咨询师：I'm sorry to hear that. It sounds like you're going through a really tough time. Can you tell me more about what's been happening?
来访者：I've been given multiple projects with very tight deadlines, and it feels like I can never catch a break. I'm constantly working long hours and sacrificing my personal time. It's taking a toll on my overall well-being.
咨询师：So, you've been juggling multiple projects with demanding deadlines, and it's leaving you with little time for yourself. That definitely sounds overwhelming. What kind of work do you do?
来访者：I work in sales. With the increasing workload and pressure to meet targets, it feels like I'm drowning in work and can't find any balance.
咨询师：Sales can be a really demanding field, especially when there are high targets to meet. It sounds like you're carrying a heavy load. Have you spoken to your supervisor about your concerns? Perhaps they can provide additional support or help with prioritizing tasks.
```

**response（来访当前句）**

```text
I haven't discussed it with my supervisor yet. I worry that they'll think I can't handle the workload and may even give me more tasks.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-250. `extes_10953_6` — 阻抗 | Work-related Stress and Burnout

- **scene**：Work-related Stress and Burnout
- **description**：I have been feeling overwhelmed and burned out at work. I have been given too many projects with tight deadlines, and it feels like I can't catch a break. I constantly work long hours and have no work-life balance. This has started affecting my physical and mental health as well.
- **binary_label**：阻抗

**context**

```text
来访者：Well, just last week, I had to work late nights to meet a major deadline, which caused me to miss out on personal commitments. It's become a pattern, and I feel like I'm constantly sacrificing my personal life for work.
咨询师：It sounds like you've been consistently struggling to balance your personal commitments and work demands. Have you spoken to your manager about this issue?
来访者：I haven't really talked to my manager about it. I'm afraid they won't understand and might put even more pressure on me.
咨询师：I can understand why you might be hesitant. It's important to create a safe space where you can discuss your concerns without fearing judgment or criticism. However, it might be worth having an open and honest conversation with your supervisor. They may be more understanding than you think.
来访者：You're right. I should give it a try. But even if I do talk to them, I'm not sure things will change.
咨询师：Change can take time, but you never really know until you try. This situation is temporary, and there are always possibilities for improvement. In the meantime, have you considered setting boundaries around your work hours and prioritizing self-care?
```

**response（来访当前句）**

```text
I find it hard to set boundaries because there's always more work to be done. How do I prioritize self-care when work is demanding so much of my time?
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-251. `extes_610_3` — 阻抗 | __other__

- **scene**：Support for Loved Ones or Friends
- **description**：My best friend and I had a falling out because of a misunderstanding. We haven't spoken in weeks and I'm feeling really lonely and sad about it. I'm not sure how to fix the situation or if our friendship can ever be repaired.
- **binary_label**：阻抗

**context**

```text
来访者：I miss my best friend so much. We had a huge fight and now we're not talking anymore.
咨询师：I'm sorry to hear that you're going through this tough time. It sounds like you're feeling really lonely and sad without your best friend.
来访者：Yeah, I feel like a part of me is missing. We used to share everything and now I don't even know if we can fix things.
咨询师：It's completely understandable to feel that way. Losing such an important person in your life must be really hard. You're not alone in feeling like a part of yourself is missing.
来访者：I appreciate that. It's just hard to imagine our friendship being the same again.
咨询师：Change can be really difficult, especially when it involves a deep friendship. It's okay to feel uncertain about the future of your friendship.
```

**response（来访当前句）**

```text
I don't even know where to start to fix things. I'm afraid that things will never be the same again.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-252. `extes_227_4` — 阻抗 | __other__

- **scene**：Adjusting to a New Job or Role
- **description**：I recently started a new job and I am struggling to fit in with my new colleagues.
- **binary_label**：阻抗

**context**

```text
来访者：I'm feeling a bit out of place at my new job.
咨询师：Oh no, that doesn't sound great. Can you tell me a little more about what's been making you feel out of place?
来访者：I don't really seem to click with my new colleagues. They already have established relationships and I feel like an outsider.
咨询师：Feeling like an outsider can be tough, especially when everyone else seems to be well-acquainted. It's completely understandable that you're feeling this way.
来访者：Yeah, it's just hard to break into existing social circles.
咨询师：Absolutely, it can be challenging to find your place in a new environment. It takes time to build connections and establish a sense of belonging. But remember, you bring unique qualities to the team that no one else can.
```

**response（来访当前句）**

```text
I guess so, but it's still overwhelming at times.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-253. `extes_83_5` — 阻抗 | __other__

- **scene**：Parenthood and Parenting Challenges
- **description**：I'm a new parent and I'm feeling overwhelmed with the constant demands of taking care of my newborn. I'm struggling to find time for myself and it's causing me a lot of stress and exhaustion.
- **binary_label**：阻抗

**context**

```text
来访者：Yes, exactly! I just need some time to recharge and regain some energy.
咨询师：It's completely normal to feel overwhelmed and exhausted during this stage of parenting. Your feelings are valid.
来访者：Thank you for understanding. Sometimes I feel guilty for wanting time for myself.
咨询师：Remember, taking care of yourself is essential in order to be able to take care of your baby. It's about finding a balance between your needs and your baby's needs.
来访者：You're right. I guess I hadn't thought about it that way.
咨询师：Have you tried asking for support from your partner or family members? Getting help can make a big difference.
```

**response（来访当前句）**

```text
I have, but sometimes it feels like I'm the only one who can take care of the baby properly.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-254. `extes_100_3` — 阻抗 | __other__

- **scene**：Cultural Identity and Belonging
- **description**：I'm feeling disconnected from my cultural heritage after moving to a new country.
- **binary_label**：阻抗

**context**

```text
来访者：Hey, how's it going?
咨询师：Hi there! I'm here and ready to listen. How are you doing today?
来访者：Honestly, I've been feeling a bit lost lately.
咨询师：I understand. It can be tough to adjust to a new country and feel disconnected from your cultural roots. Can you tell me more about what you're experiencing?
来访者：I recently moved to a new country, and I feel like I've lost touch with my cultural identity.
咨询师：That sounds like a challenging situation. It must be hard not to have the same cultural experiences and connections you used to. Have you tried exploring any local cultural communities or groups?
```

**response（来访当前句）**

```text
I haven't really found any communities that align with my cultural background here.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-255. `extes_4886_3` — 阻抗 | __other__

- **scene**：Relationship Struggles and Communication Issues
- **description**：My cousin and I used to be really close, but lately, we've been having a hard time communicating and it's causing tension in our relationship. I want to find a way to address the issue without further damaging our bond.
- **binary_label**：阻抗

**context**

```text
来访者：Hello
咨询师：Hi there! How are you today?
来访者：Hey, I'm doing alright, thanks. Actually, I've been feeling a bit troubled lately. My cousin and I used to be really close, but recently, we've been having a hard time communicating. It's causing tension and I really want to find a way to address it without hurting our relationship.
咨询师：I understand. It can be challenging when changes occur in our relationships, especially with family members. Can you share some more about the communication issues you're facing with your cousin?
来访者：Sure. It feels like we can't have a simple conversation without it turning into an argument. We often misunderstood each other and end up yelling or saying hurtful things. I miss the good times we used to have.
咨询师：It sounds tough to be constantly arguing with someone you're close to. It's understandable that you miss the positive aspects of your relationship. Have you tried to talk to your cousin about the recent communication issues?
```

**response（来访当前句）**

```text
I've tried a few times, but it's always ended up in an argument. I feel like we're trapped in this cycle and it's frustrating.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-256. `extes_446_3` — 阻抗 | __other__

- **scene**：Low Self-Esteem or Lack of Confidence
- **description**：I've been feeling a lack of confidence in my professional abilities lately. I constantly doubt myself and worry that I'm not capable of succeeding in my job.
- **binary_label**：阻抗

**context**

```text
来访者：Hi there
咨询师：Hello! How are you feeling today?
来访者：Honestly, not so great. I've been feeling really down and insecure lately.
咨询师：I hear you. It's tough when our self-confidence takes a hit. Can you pinpoint any specific reasons for feeling this way?
来访者：I think it's mainly because I made a few mistakes at work recently. It's making me doubt my abilities and worry that I'm just not good enough.
咨询师：Making mistakes is a normal part of learning and growing. It doesn't define your worth or competence. Remember, everyone makes mistakes, even the most successful people.
```

**response（来访当前句）**

```text
I know deep down that you're right, but it's still hard to shake off the feeling of inadequacy.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

### A-257. `extes_100_4` — 阻抗 | __other__

- **scene**：Cultural Identity and Belonging
- **description**：I'm feeling disconnected from my cultural heritage after moving to a new country.
- **binary_label**：阻抗

**context**

```text
来访者：Honestly, I've been feeling a bit lost lately.
咨询师：I understand. It can be tough to adjust to a new country and feel disconnected from your cultural roots. Can you tell me more about what you're experiencing?
来访者：I recently moved to a new country, and I feel like I've lost touch with my cultural identity.
咨询师：That sounds like a challenging situation. It must be hard not to have the same cultural experiences and connections you used to. Have you tried exploring any local cultural communities or groups?
来访者：I haven't really found any communities that align with my cultural background here.
咨询师：Have you been actively looking for such communities or groups? It might be worth searching online or reaching out to local organizations that focus on your cultural heritage.
```

**response（来访当前句）**

```text
I've tried searching online, but the options are limited. It's disheartening.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-258. `extes_9131_4` — 阻抗 | __other__

- **scene**：Parenting Challenges and Parental Guilt
- **description**：My teenage daughter and I have been having constant arguments lately. She is rebellious and refuses to listen to my rules. I am feeling guilty about not being able to connect with her and not being a good parent.
- **binary_label**：阻抗

**context**

```text
来访者：To be honest, I'm really struggling. My relationship with my daughter has been difficult lately. We constantly argue and it's making me feel like a failure as a parent.
咨询师：I can understand why that would be challenging for you. It's tough when you feel like you're not connecting with your child, especially when it causes arguments. Parenting is a journey with its ups and downs.
来访者：I just don't know what to do. I've tried talking to her, setting boundaries, and being understanding, but nothing seems to work. I feel like I'm failing her.
咨询师：It sounds like you've been putting in a lot of effort to improve your relationship with your daughter. Parenting can be incredibly challenging, and it's important to remember that this is not a reflection of your worth as a parent. Sometimes, despite our best efforts, conflicts can arise.
来访者：I appreciate the reassurance... but it still weighs heavily on me. I want to be there for her and be a positive influence in her life, but it feels like she's pushing me away.
咨询师：It's understandable that you want to have a strong bond with your daughter. It's possible that her behavior may be driven by her own challenges and struggles. Have you tried having an open conversation with her to understand her perspective?
```

**response（来访当前句）**

```text
I've tried, but she always shuts me out. It feels like she doesn't want to share anything with me. I'm worried I'm losing her.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-259. `extes_247_2` — 阻抗 | __other__

- **scene**：Parenthood and Parenting Challenges
- **description**：I'm having trouble adjusting to being a new parent. I feel overwhelmed and exhausted all the time.
- **binary_label**：阻抗

**context**

```text
咨询师：Hey, how are you doing?
来访者：I'm okay, but I've been feeling really overwhelmed lately.
咨询师：I'm here for you. Would you like to talk about what's been going on?
来访者：Sure. Being a new parent has been more challenging than I expected. I always feel tired, and I'm not sure if I'm doing things right.
咨询师：It's completely normal to feel overwhelmed when adjusting to parenthood. It's a big change and requires a lot of energy and attention.
```

**response（来访当前句）**

```text
I know, but I still feel like I should be handling everything better. I compare myself to other parents and it makes me doubt myself.
```

**raw_output（若有，节选）**

```text
阻抗
阻抗
阻抗
阻
```

---

### A-260. `extes_89_3` — 阻抗 | __other__

- **scene**：Lack of Confidence in Public Speaking
- **description**：I have to deliver a presentation at work tomorrow, but I lack confidence in public speaking and I'm extremely nervous about it.
- **binary_label**：阻抗

**context**

```text
来访者：Hey
咨询师：Hi there! How are you doing today?
来访者：I'm feeling really anxious and worried. I have to give a presentation at work tomorrow, and I'm so nervous about it. I feel like I lack the confidence to speak in front of a group of people, and I'm afraid of messing it up.
咨询师：I completely understand how you feel. It can be intimidating to speak in front of a group, and it's natural to feel nervous. Many people struggle with public speaking and confidence, so you're not alone.
来访者：Thank you for understanding. It just feels overwhelming, and I want to do well and make a good impression on my colleagues.
咨询师：I hear you. It's important to remember that everyone has to start somewhere. Even the most confident public speakers had to overcome their fears and gain experience. You're taking a brave step by preparing for this presentation.
```

**response（来访当前句）**

```text
You're right. I've been practicing and preparing a lot, but I can't shake off the feeling of self-doubt.
```

**raw_output（若有，节选）**

```text
阻抗
合作
阻抗
合作
```

---

## Part B — resist_fine.json（按 fine_category 抽样，附 binary join）

| # | stratum | sample_id | join_ok | binary_label | fine_category | fine_label |
|---|---------|-----------|---------|--------------|---------------|------------|
| 1 | resist_fine \| A2 | `extes_2746_4` | yes | 阻抗 | A2 | 争辩-贬低 |
| 2 | resist_fine \| A2 | `extes_109_4` | yes | 阻抗 | A2 | 争辩-贬低 |
| 3 | resist_fine \| A2 | `extes_594_5` | yes | 阻抗 | A2 | 争辩-贬低 |
| 4 | resist_fine \| A2 | `extes_6765_3` | yes | 阻抗 | A2 | 争辩-贬低 |
| 5 | resist_fine \| A2 | `extes_8186_5` | yes | 阻抗 | A2 | 争辩-贬低 |
| 6 | resist_fine \| A2 | `extes_2613_3` | yes | 阻抗 | A2 | 争辩-贬低 |
| 7 | resist_fine \| A2 | `extes_1876_3` | yes | 阻抗 | A2 | 争辩-贬低 |
| 8 | resist_fine \| A2 | `extes_7368_3` | yes | 阻抗 | A2 | 争辩-贬低 |
| 9 | resist_fine \| B5 | `extes_4264_3` | yes | 阻抗 | B5 | 否认-悲观 |
| 10 | resist_fine \| B5 | `extes_1567_3` | yes | 阻抗 | B5 | 否认-悲观 |
| 11 | resist_fine \| B5 | `extes_10418_3` | yes | 阻抗 | B5 | 否认-悲观 |
| 12 | resist_fine \| B5 | `extes_8244_4` | yes | 阻抗 | B5 | 否认-悲观 |
| 13 | resist_fine \| B5 | `extes_4543_4` | yes | 阻抗 | B5 | 否认-悲观 |
| 14 | resist_fine \| B5 | `extes_2225_3` | yes | 阻抗 | B5 | 否认-悲观 |
| 15 | resist_fine \| B5 | `extes_9677_4` | yes | 阻抗 | B5 | 否认-悲观 |
| 16 | resist_fine \| B5 | `extes_5063_3` | yes | 阻抗 | B5 | 否认-悲观 |
| 17 | resist_fine \| C2 | `extes_9699_4` | yes | 阻抗 | C2 | 回避-界限设定 |
| 18 | resist_fine \| C2 | `extes_4250_4` | yes | 阻抗 | C2 | 回避-界限设定 |
| 19 | resist_fine \| C2 | `extes_588_3` | yes | 阻抗 | C2 | 回避-界限设定 |
| 20 | resist_fine \| C2 | `extes_6631_6` | yes | 阻抗 | C2 | 回避-界限设定 |
| 21 | resist_fine \| C2 | `extes_7063_3` | yes | 阻抗 | C2 | 回避-界限设定 |
| 22 | resist_fine \| C2 | `extes_2607_4` | yes | 阻抗 | C2 | 回避-界限设定 |
| 23 | resist_fine \| C2 | `extes_3075_4` | yes | 阻抗 | C2 | 回避-界限设定 |
| 24 | resist_fine \| C2 | `extes_10948_4` | yes | 阻抗 | C2 | 回避-界限设定 |
| 25 | resist_fine \| D1 | `extes_9753_2` | yes | 阻抗 | D1 | 忽视-不关注 |
| 26 | resist_fine \| D1 | `extes_1937_6` | yes | 阻抗 | D1 | 忽视-不关注 |
| 27 | resist_fine \| D1 | `extes_4142_5` | yes | 阻抗 | D1 | 忽视-不关注 |
| 28 | resist_fine \| D1 | `extes_4553_3` | yes | 阻抗 | D1 | 忽视-不关注 |
| 29 | resist_fine \| D1 | `extes_9751_2` | yes | 阻抗 | D1 | 忽视-不关注 |
| 30 | resist_fine \| D1 | `extes_4669_4` | yes | 阻抗 | D1 | 忽视-不关注 |
| 31 | resist_fine \| D1 | `extes_3091_4` | yes | 阻抗 | D1 | 忽视-不关注 |
| 32 | resist_fine \| D1 | `extes_10643_3` | yes | 阻抗 | D1 | 忽视-不关注 |
| 33 | resist_fine \| C1 | `extes_8208_3` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 34 | resist_fine \| C1 | `extes_10773_5` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 35 | resist_fine \| C1 | `extes_5550_4` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 36 | resist_fine \| C1 | `extes_2537_3` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 37 | resist_fine \| C1 | `extes_2377_5` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 38 | resist_fine \| C1 | `extes_5838_2` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 39 | resist_fine \| C1 | `extes_931_3` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 40 | resist_fine \| C1 | `extes_4680_3` | yes | 阻抗 | C1 | 回避-最小的回应 |
| 41 | resist_fine \| B1 | `extes_9884_2` | yes | 阻抗 | B1 | 否认-责怪 |
| 42 | resist_fine \| B1 | `extes_1994_3` | yes | 阻抗 | B1 | 否认-责怪 |
| 43 | resist_fine \| B1 | `extes_1285_3` | yes | 阻抗 | B1 | 否认-责怪 |
| 44 | resist_fine \| B1 | `extes_10055_2` | yes | 阻抗 | B1 | 否认-责怪 |
| 45 | resist_fine \| B1 | `extes_2332_2` | yes | 阻抗 | B1 | 否认-责怪 |
| 46 | resist_fine \| B1 | `extes_9845_3` | yes | 阻抗 | B1 | 否认-责怪 |
| 47 | resist_fine \| B1 | `extes_10223_2` | yes | 阻抗 | B1 | 否认-责怪 |
| 48 | resist_fine \| B1 | `extes_1735_7` | yes | 阻抗 | B1 | 否认-责怪 |

### Part B 全文（逐条）

### B-1. `extes_2746_4` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't really tried that before. It seems difficult to set boundaries without feeling like I'm neglecting someone or something.
```

**binary.context（对齐全文）**

```text
来访者：I feel really overwhelmed with trying to balance my work and personal life. I have so many deadlines to meet at work, but I also want to spend quality time with my family and take care of myself.
咨询师：It sounds like you have a lot on your plate right now. Juggling work demands with personal commitments can be challenging. How are you feeling about it all?
来访者：I'm feeling stressed and guilty. I worry that I'm not doing enough for my job or my family, and I'm neglecting my own needs in the process.
咨询师：I hear you. It's completely normal to feel stressed when you're pulled in multiple directions. It's important to remember that you're only human, and it's impossible to do everything perfectly. Taking care of yourself is equally important as meeting work and family obligations. Let's explore some strategies that might help you find a better balance. How do you usually prioritize your tasks?
来访者：I often feel torn between attending work meetings and spending time with my family. I end up feeling guilty no matter what choice I make.
咨询师：I see. It sounds like you struggle with prioritizing work and family time, which leads to feelings of guilt. Have you considered setting boundaries or having open communication with both your work and family? That way, you can establish clear expectations and find ways to manage your time more effectively.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't really tried that before. It seems difficult to set boundaries without feeling like I'm neglecting someone or something.
```

**description**：A user is feeling overwhelmed and stressed about balancing work and personal commitments and is seeking emotional support.

---

### B-2. `extes_109_4` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Academic Stress or Pressure

**resist_fine.response（若 join 失败则仅此句）**

```text
I have, but I often get overwhelmed and don't stick to it.
```

**binary.context（对齐全文）**

```text
来访者：I'm alright, just feeling overwhelmed with everything.
咨询师：It sounds like you have a lot on your plate. Can you tell me more about what's been going on?
来访者：Yeah, I'm taking five classes this semester and working part-time. It's tough to juggle both.
咨询师：That sounds really challenging. It's important to acknowledge how hard you're working.
来访者：Yeah, it's just difficult to find time for everything.
咨询师：Have you considered creating a schedule or a to-do list to manage your time more efficiently?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I have, but I often get overwhelmed and don't stick to it.
```

**description**：I am struggling with balancing my coursework and part-time job.

---

### B-3. `extes_594_5` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Spirituality and Faith

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm just scared of being judged by others for questioning my spirituality and exploring different beliefs.
```

**binary.context（对齐全文）**

```text
来访者：I fear that by questioning and doubting my beliefs, I'm betraying my faith and disappointing those around me who are still strong in their convictions.
咨询师：It's understandable to have concerns about disappointing others or feeling like you're betraying your faith. However, it's important to remember that your spiritual beliefs are incredibly personal and unique to you. Your journey may involve periods of questioning and exploration, and that doesn't mean you are betraying anything. Your growth and self-discovery are valuable, and seeking your own truth is a courageous path to take.
来访者：But what if I never find the answers I'm seeking? What if I'm forever lost in this confusion and doubt?
咨询师：It's natural to have concerns about finding the answers you're seeking. Instead of focusing solely on the end result, try to embrace the process of self-discovery and the exploration of different beliefs and perspectives. Often, clarity comes not in finding definite answers, but in developing a deep understanding and acceptance of your own unique spiritual journey. Remember, the path itself can be transformative and enriching.
来访者：I just wish I had some guidance or a starting point to help me navigate this confusion. It feels overwhelming without any direction.
咨询师：I understand that feeling overwhelmed without a clear starting point can be challenging. One helpful approach could be to start small, perhaps by setting aside some time for self-reflection or meditation to connect with your inner self. You could also explore books or online resources that discuss different spiritual philosophies or seek out spiritual communities or mentors who can provide guidance and support. Remember, your journey is unique, and taking small steps can lead to significant progress over time.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm just scared of being judged by others for questioning my spirituality and exploring different beliefs.
```

**description**：Lately, I've been feeling a lack of connection to my spirituality and it's causing me distress. I used to have a strong faith, but now I feel lost and unsure about what I believe. I'm seeking guidance and support to help me find my way back to my spiritual path.

---

### B-4. `extes_6765_3` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't discussed it with anyone yet. I'm worried they'll think I can't handle the job or that I'm slacking off. Plus, I don't want to seem like I'm complaining so early on.
```

**binary.context（对齐全文）**

```text
来访者：Hey, are you free to talk? I've been feeling really stressed lately.
咨询师：Of course! I'm here to listen. What's been going on?
来访者：I recently started a new job, and it's been really challenging. The workload is overwhelming, and I'm struggling to manage my time effectively. I feel like I can't keep up with the expectations and meet all the deadlines.
咨询师：It sounds like you're going through a tough time with your new job. Managing a heavy workload and meeting deadlines can be overwhelming, especially when you're still trying to adjust. How have you been coping with the stress?
来访者：I've been trying to set priorities and create a schedule, but it feels like there's never enough time to get everything done. I end up working late and sacrificing my personal time, which is really affecting my well-being.
咨询师：It's understandable to feel pressured when there's a lot on your plate. Trying to balance work and personal life can be challenging, especially in a new job. It's great that you're trying to prioritize and create a schedule, but remember to also take breaks and set aside time for self-care. Have you talked to your manager or colleagues about your workload concerns?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't discussed it with anyone yet. I'm worried they'll think I can't handle the job or that I'm slacking off. Plus, I don't want to seem like I'm complaining so early on.
```

**description**：I recently started a new job, and I'm feeling overwhelmed with the workload and expectations. I'm struggling to manage my time and meet deadlines.

---

### B-5. `extes_8186_5` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I just don't know what to do anymore. I feel demotivated to go to work and I can't shake this feeling of being an outsider.
```

**binary.context（对齐全文）**

```text
来访者：Yes, it's been tougher than I expected. I feel like I'm always left out of conversations during breaks and social events.
咨询师：I understand that feeling left out can be disheartening. Could you provide more details about what happens during breaks and social events?
来访者：During breaks, everyone already seems to have their own groups and they engage in conversations I can't participate in. And during social events, they often make plans without inviting me.
咨询师：It sounds frustrating to witness cliques forming and feeling excluded from conversations. It's completely natural to desire a sense of belonging.
来访者：Exactly! It's making me doubt myself and my ability to fit in. I want to contribute and be part of the team.
咨询师：I can understand how that could affect your confidence and make you question your place in the team. It's important to remember that it takes time to build these connections, and it doesn't reflect your value or abilities.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I just don't know what to do anymore. I feel demotivated to go to work and I can't shake this feeling of being an outsider.
```

**description**：I recently started a new job and I'm finding it difficult to communicate with my co-workers. I feel left out and it's affecting my confidence.

---

### B-6. `extes_2613_3` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't spoken to my boss yet. I'm afraid that if I do, they might think I can't handle my responsibilities or that I'm not committed enough to my job.
```

**binary.context（对齐全文）**

```text
来访者：Hi there
咨询师：Hey, how's it going?
来访者：I'm feeling really overwhelmed right now. My boss keeps giving me more and more work, and I'm struggling to meet the deadlines.
咨询师：Oh, that sounds really tough. It can be really overwhelming when you have too much on your plate and tight deadlines. How has this affected your stress levels and ability to cope?
来访者：I've been feeling so stressed out lately. I can't seem to catch a break. I've been working late every night and sacrificing my personal time to meet all the expectations.
咨询师：It sounds like your work-life balance has been negatively impacted. That can be really challenging and can lead to burnout. Have you tried communicating your concerns with your boss, and letting them know about the workload you're currently dealing with?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't spoken to my boss yet. I'm afraid that if I do, they might think I can't handle my responsibilities or that I'm not committed enough to my job.
```

**description**：I'm feeling really overwhelmed because my boss keeps piling on more work and I'm struggling to meet the deadlines.

---

### B-7. `extes_1876_3` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Academic Stress

**resist_fine.response（若 join 失败则仅此句）**

```text
Exactly. Sometimes I can't help but think that maybe I'm just not capable enough to handle all of this.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I've been feeling so overwhelmed lately. I have so many exams coming up and I can't seem to manage my time effectively.
咨询师：I hear you. It sounds like you have a lot on your plate and finding it challenging to balance everything with your exams.
来访者：Exactly! I feel like no matter how much I study, I still have so much more to cover. It's stressing me out and I'm afraid my grades will suffer.
咨询师：It's completely normal to feel stressed and worried when you have a heavy workload and important exams coming up. Your dedication to studying is evident, but it's important to find a balance to avoid burnout.
来访者：Thanks for understanding. It just feels like time is slipping away, and the pressure to perform well is constantly hanging over me.
咨询师：I can imagine that it must be frustrating to have such limited time and feel the weight of expectations. It's understandable that you would feel overwhelmed.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Exactly. Sometimes I can't help but think that maybe I'm just not capable enough to handle all of this.
```

**description**：Feeling overwhelmed with upcoming exams and struggling to manage time effectively

---

### B-8. `extes_7368_3` — resist_fine | A2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：A2 / 争辩-贬低
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I've tried making to-do lists before, but it feels like there's just so much to do that it becomes overwhelming.
```

**binary.context（对齐全文）**

```text
来访者：Hi, can I talk to you about something?
咨询师：Of course! I'm here to listen. What's going on?
来访者：I've been feeling so stressed lately. I have so many tasks piling up at work, and I just don't know how to manage everything.
咨询师：I'm sorry to hear that you're feeling this way. It sounds like you've been facing a lot of pressure. It's completely understandable to feel overwhelmed in such situations.
来访者：Yes, it's been really challenging to keep up with everything. I don't know where to start or how to prioritize my tasks.
咨询师：It's difficult when you have a lot on your plate and you don't know where to begin. Have you tried making a to-do list or breaking down your tasks into smaller, more manageable steps?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I've tried making to-do lists before, but it feels like there's just so much to do that it becomes overwhelming.
```

**description**：I'm feeling really overwhelmed with my workload and I don't know how to manage all the tasks.

---

### B-9. `extes_4264_3` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm struggling to stay positive amidst all this pain.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I'm really struggling right now. My long-distance relationship just ended.
咨询师：I'm here for you. Can you tell me more about what happened and how you're feeling?
来访者：We tried so hard to make it work, but the distance just became too much for both of us. I feel so heartbroken and lost.
咨询师：I can only imagine how difficult this must be for you. Long-distance relationships can be incredibly challenging, and it sounds like you gave it your all. It's okay to feel heartbroken and lost right now.
来访者：Thank you for understanding. I just don't know how to move on from here.
咨询师：I want you to remember that you're strong and resilient. It's completely natural to feel unsure of how to move forward after such a significant breakup, but you have the power to create a new path for yourself.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm struggling to stay positive amidst all this pain.
```

**description**：After being in a long-distance relationship for five years, my partner and I decided to end things due to the strain distance was putting on our relationship. I'm feeling heartbroken and unsure of how to move forward.

---

### B-10. `extes_1567_3` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm not sure how to move forward. I thought we would be together forever.
```

**binary.context（对齐全文）**

```text
来访者：Hi, I'm feeling really down right now.
咨询师：Hey there, I'm here to listen. What's been going on that's been bothering you?
来访者：My partner and I just broke up after being in a long-term relationship for several years.
咨询师：I'm really sorry to hear that. It must be a difficult time for you. How are you feeling about it all?
来访者：I'm feeling heartbroken and lost. I never imagined we would come to this point.
咨询师：I completely understand how you feel. It's tough when relationships change, and it's okay to grieve the loss of what you envisioned for your future together.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm not sure how to move forward. I thought we would be together forever.
```

**description**：After being together for several years, my partner and I recently ended our relationship due to growing apart. I'm feeling heartbroken and uncertain about my future.

---

### B-11. `extes_10418_3` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
It just hurts so badly. I can't believe he's gone.
```

**binary.context（对齐全文）**

```text
来访者：Not so great. My dog passed away yesterday and I am heartbroken.
咨询师：I'm so sorry to hear about your loss. Losing a beloved pet can be incredibly painful. Can you tell me a little bit about your dog?
来访者：Thank you. My dog was a Labrador Retriever named Max. He was my loyal companion for 10 years.
咨询师：Max sounded like an amazing friend and was part of your family for a long time. It's really tough to say goodbye to such a close companion.
来访者：Yes, he truly was. I miss him so much. He was always there for me, through the good and bad times.
咨询师：Grieving the loss of a pet is completely normal. It's okay to feel a deep sense of sadness and loss right now. Take your time to process your emotions and don't rush the healing process.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
It just hurts so badly. I can't believe he's gone.
```

**description**：My dog passed away after a sudden illness

---

### B-12. `extes_8244_4` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I guess you're right, but it's still discouraging. I feel like I'm always on the outside looking in.
```

**binary.context（对齐全文）**

```text
来访者：To be honest, not great. I've been feeling really lonely since I moved to this new city.
咨询师：I'm sorry to hear that. It can be tough to adjust to a new place and feel lonely. It's completely normal to have these emotions in a new environment.
来访者：Yeah, it's been harder than I expected. I find it difficult to connect with people and make new friends.
咨询师：It must be frustrating and disappointing to have difficulty connecting with others and forming new friendships.
来访者：Exactly! I feel like everyone has their own established friend groups, and I just don't fit in.
咨询师：Feeling like an outsider and not fitting in can be really hard. It's important to remember that forming new friendships takes time and effort.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I guess you're right, but it's still discouraging. I feel like I'm always on the outside looking in.
```

**description**：I recently moved to a new city and have been feeling quite lonely. Making friends has been a struggle for me, and I find it hard to connect with people in social settings.

---

### B-13. `extes_4543_4` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I never thought I'd be single again. It's scary to start over.
```

**binary.context（对齐全文）**

```text
来访者：It's just been so hard. I feel heartbroken and lost. I never expected our relationship to end like this.
咨询师：I can understand how devastating this must be for you. It's normal to feel heartbroken and lost when a long-term relationship ends. Your emotions are valid.
来访者：Thank you. I'm struggling to come to terms with the fact that it's over. Everything feels so overwhelming.
咨询师：It's completely understandable to feel overwhelmed and struggle with acceptance. Breakups bring significant changes, and accepting the end of a relationship takes time. It's important to give yourself permission to grieve the loss and be patient with your healing process.
来访者：I just keep replaying all the good memories in my head and it hurts so much. How do I let go?
咨询师：It's natural to reflect on the good times and feel a sense of loss. However, holding onto those memories can make it harder to move forward. Consider reframing your thoughts about the breakup. Focus on the lessons learned and the opportunities for personal growth. By shifting your perspective, you can open yourself up to the possibility of new experiences and a brighter future.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I never thought I'd be single again. It's scary to start over.
```

**description**：After being in a long-term relationship with my boyfriend for seven years, we recently went through a painful breakup. The breakup has left me feeling devastated and stuck, and I need support to navigate through this difficult time.

---

### B-14. `extes_2225_3` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm finding it hard to believe that I'll ever find happiness again. I'm scared to start over.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I've been feeling really lost and down since my divorce. I don't know how to move forward.
咨询师：Hi there. I can imagine how difficult and overwhelming this must be for you. Can you tell me a bit more about what you're going through?
来访者：After a decade of marriage, my partner and I decided to end our relationship. It's been emotionally exhausting, and I'm having a hard time adjusting to this new reality.
咨询师：That sounds incredibly tough. Going through a divorce after being together for so long can bring immense emotional pain and uncertainty. It's okay to feel lost and exhausted right now.
来访者：I feel like everything fell apart. I thought we would always be together, but now I'm left with a void and a fear of being alone forever.
咨询师：It's completely understandable to feel that way. Divorce often brings a mix of emotions, including loss, fear, and sadness. Remember that these feelings are valid, and it's okay to take time to grieve and heal.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm finding it hard to believe that I'll ever find happiness again. I'm scared to start over.
```

**description**：I recently went through a divorce after being married for 10 years. It has been a challenging and emotional experience, and I'm struggling to navigate through the pain and uncertainty.

---

### B-15. `extes_9677_4` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm trying to stay positive, but it's hard to stop thinking about her.
```

**binary.context（对齐全文）**

```text
来访者：It's devastating. I never expected this. We seemed so happy together.
咨询师：I can only imagine how devastating this must be for you. It's truly heart-wrenching when a relationship you thought was solid comes to an end.
来访者：Yeah, it's really hard. I feel like a huge part of my life has been taken away.
咨询师：Absolutely understandable. Ending a long-term relationship can make you feel as though a significant part of your identity has been lost. Give yourself time to grieve and process the emotions.
来访者：I don't know how to begin moving on. It feels impossible right now.
咨询师：I know it may seem impossible at the moment, but with time, healing will come. Focus on taking care of yourself and engaging in activities that bring you joy. Surround yourself with loved ones who can offer support during this difficult time.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm trying to stay positive, but it's hard to stop thinking about her.
```

**description**：After being in a long-term relationship for seven years, my girlfriend and I recently broke up. I'm feeling heartbroken and lost, and I'm struggling to cope with the pain and move on.

---

### B-16. `extes_5063_3` — resist_fine | B5

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B5 / 否认-悲观
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
But right now, it's hard for me to see any positives. I feel like my whole world has turned upside down.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I really need someone to talk to. I'm feeling so shattered right now.
咨询师：Hi there. I'm here for you. I'm sorry to hear that you're going through such a tough time. Can you tell me more about what happened?
来访者：We were together for 5 years, and we were planning to get married. But our constant arguments and inability to communicate effectively took a toll on our relationship. It's hard for me to accept that it's over.
咨询师：That sounds incredibly difficult. It's heartbreaking when a long-term relationship doesn't work out as planned, especially when marriage was on the horizon. It's normal to feel shattered and unsure of what comes next.
来访者：I invested so much love and effort into this relationship, and now it feels like everything was a waste. I don't know if I can ever trust someone again.
咨询师：I completely understand why you feel that way. It's natural to question your ability to trust after going through a painful breakup. Remember, not all relationships will be the same. This experience can bring growth and teach you more about yourself and what you truly deserve in a partner.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
But right now, it's hard for me to see any positives. I feel like my whole world has turned upside down.
```

**description**：I recently broke up with my long-term partner after being together for 5 years. We were planning to get married, but our constant conflicts and lack of communication led to the end of our relationship. I'm feeling devastated and lost, and I don't know how to move on.

---

### B-17. `extes_9699_4` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Coping with the illness or death of a loved one

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't really considered that. I feel like I should be able to manage on my own.
```

**binary.context（对齐全文）**

```text
来访者：Honestly, I'm not doing well. My uncle passed away recently, and it's been tough.
咨询师：I'm so sorry to hear about your loss. It sounds like you're going through a difficult time. How have you been coping so far?
来访者：I've been feeling overwhelmed and lost. It's hard to process my emotions, and sometimes I just feel like crying all day.
咨询师：I want you to know that it's completely okay to feel overwhelmed and not know how to process your emotions. Grieving is a complex journey, and it affects each person differently. Is there something specific that brings you solace or makes you feel supported?
来访者：Talking about my uncle and looking at old pictures brings me some comfort. But there are times when I just want to be alone with my thoughts.
咨询师：It's completely understandable that reminiscing about the good times and cherishing those memories brings you comfort. It's also important to honor your need for solitude during this grieving period, as everyone requires different amounts of space to heal. Have you considered seeking professional help or joining a support group to supplement your coping mechanisms?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't really considered that. I feel like I should be able to manage on my own.
```

**description**：My uncle recently passed away due to a terminal illness, and I'm finding it hard to cope with the loss. I feel overwhelmed and uncertain about how to navigate this emotional journey.

---

### B-18. `extes_4250_4` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
You're right. It's just difficult to open up about it. I don't want people to judge me.
```

**binary.context（对齐全文）**

```text
来访者：It's just so hard to accept that someone I loved so deeply could betray me like that. I feel broken and lost.
咨询师：I can't imagine the pain you're experiencing right now. It's completely normal to feel broken and lost after going through such a betrayal. If you're comfortable sharing, can you tell me more about what happened?
来访者：I found out that my ex-partner was cheating on me with my best friend. It feels like a double betrayal.
咨询师：That's an incredibly difficult situation to deal with. Discovering a cheating partner is challenging enough, but also finding out that it involves your best friend can make it feel like a double betrayal. Have you been able to reach out to someone supportive, like another friend or a family member?
来访者：I haven't really talked to anyone about it. I feel ashamed and embarrassed.
咨询师：Feeling ashamed and embarrassed is common, but please remember that you have nothing to be ashamed of. Betrayal can bring up a range of emotions, and it's important to talk to someone you trust. Sharing your feelings with a supportive friend or family member might provide you with some comfort.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
You're right. It's just difficult to open up about it. I don't want people to judge me.
```

**description**：After ending a 3-year relationship, I'm struggling to overcome the feelings of heartbreak and betrayal.

---

### B-19. `extes_588_3` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Spirituality and Faith

**resist_fine.response（若 join 失败则仅此句）**

```text
But what if I disappoint my family or go against everything I've been taught? I'm scared of the consequences.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I've been feeling really confused about my spiritual beliefs lately. And I don't know what to pursue. Can I talk to you about it?
咨询师：I'm here for you. It sounds like you've been going through a challenging time with your spiritual beliefs. I'm here to listen and support you as you navigate this journey.
来访者：Thanks, it means a lot to have someone to talk to about this. I've been raised in a certain religious tradition, but lately, I find myself questioning everything.
咨询师：It's completely normal to question your beliefs, especially when you're seeking your own personal truth. Your journey of self-discovery is unique to you, and I want you to feel validated in exploring these doubts and questions.
来访者：I've been reading about other religions and spiritual practices, and I can't help but wonder if there's something else out there that aligns more with my personal values and beliefs.
咨询师：Exploring other spiritual beliefs and practices can be a meaningful part of your journey as you discover what resonates with you on a deeper level. It's important to find alignment with your personal values, and seeking different perspectives can be a valuable step in that process.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
But what if I disappoint my family or go against everything I've been taught? I'm scared of the consequences.
```

**description**：I have been feeling lost and disconnected from my spirituality lately. I used to have a strong faith, but recently I've been questioning everything and I don't know where to turn.

---

### B-20. `extes_6631_6` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't asked for help yet. I didn't want to seem incapable or bothersome.
```

**binary.context（对齐全文）**

```text
来访者：I haven't really talked to them about it. I'm not sure how to approach the situation.
咨询师：It's understandable to feel unsure about how to address this. Open and honest communication is usually a good approach. Perhaps you could schedule a one-on-one coffee or lunch with one of your coworkers to get to know them better and express your concerns. Establishing a personal connection may make it easier to collaborate in a professional setting.
来访者：That's a good idea. I'll try to initiate conversations and find common interests with my coworkers.
咨询师：Great! Finding common interests is a wonderful way to build rapport and improve communication. Additionally, active listening can be incredibly beneficial in conversations. Taking the time to understand and validate your coworkers' perspectives can help create a more positive and collaborative work environment. Is there anything else you're finding challenging at your new job?
来访者：Apart from the communication issues, I'm also struggling with understanding the company's processes and procedures. It's overwhelming at times.
咨询师：I can imagine it can be overwhelming to navigate through new processes and procedures. Getting familiar with them takes time and practice. Have you reached out to your supervisor or colleagues to seek clarification and guidance?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't asked for help yet. I didn't want to seem incapable or bothersome.
```

**description**：I recently started a new job and I'm having difficulty communicating with my coworkers. I feel left out and misunderstood, and it's affecting my overall job satisfaction.

---

### B-21. `extes_7063_3` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I usually end up not saying anything and keeping my thoughts to myself. I'm afraid of being interrupted or dismissed, so I prefer to avoid speaking up altogether.
```

**binary.context（对齐全文）**

```text
来访者：Hey there!
咨询师：Hello! How can I assist you today?
来访者：I've been feeling frustrated at work lately. I recently started a new job, and I'm having trouble communicating with my colleagues and expressing myself effectively in team meetings. It's really affecting my confidence and job performance.
咨询师：I'm sorry to hear that you're feeling frustrated at work. It can be incredibly challenging to navigate communication dynamics in a new job, especially with colleagues and in team settings. Can you tell me more about the specific difficulties you're encountering?
来访者：Sure! I often feel misunderstood when I express my ideas. Sometimes, my colleagues speak over me, and I find it hard to get my point across. It's making me second-guess myself and reluctant to speak up during meetings.
咨询师：It sounds like you're experiencing a lack of effective communication and active listening from your colleagues, which can be discouraging. It's important to be able to express yourself openly and have your ideas heard and valued. How do you typically handle these situations when they occur? Do you have any strategies that you've tried before?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I usually end up not saying anything and keeping my thoughts to myself. I'm afraid of being interrupted or dismissed, so I prefer to avoid speaking up altogether.
```

**description**：I recently started a new job, but I'm having difficulty communicating effectively with my colleagues and expressing my ideas clearly in team meetings.

---

### B-22. `extes_2607_4` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I have been trying to prioritize, but it still feels like I have too much on my plate. It's hard to strike a balance.
```

**binary.context（对齐全文）**

```text
来访者：I've been feeling incredibly stressed lately. My workload at work has been increasing, and I'm finding it difficult to manage everything efficiently. It's starting to take a toll on my productivity and well-being.
咨询师：I can understand how overwhelming that must feel. It's tough when your workload becomes too much to handle and it affects both your work and personal life. Have you spoken to your supervisor about this issue?
来访者：Yes, I have. They acknowledged my concerns, but the workload is still consistently high without any visible solutions. It's really frustrating.
咨询师：I can totally understand your frustration. It's disheartening when you raise concerns and there aren't immediate changes. It's important to remember that your concerns are valid, and it's not uncommon to feel stressed in these situations.
来访者：Thank you. It feels good to have my feelings validated. I just wish there was some way to better manage my stress and workload.
咨询师：Absolutely! Remember, you have control over how you respond to stress. Have you tried setting clear boundaries and prioritizing your tasks? It could help in making your workload feel more manageable.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I have been trying to prioritize, but it still feels like I have too much on my plate. It's hard to strike a balance.
```

**description**：I've been feeling really stressed lately because my workload at work has been increasing and I'm struggling to manage everything efficiently.

---

### B-23. `extes_3075_4` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Conflicts or Communication Problems

**resist_fine.response（若 join 失败则仅此句）**

```text
I've thought about it, but I was hoping we could resolve it ourselves. The idea of involving others feels uncomfortable to me.
```

**binary.context（对齐全文）**

```text
来访者：Well, I've been having difficulties communicating with my coworker and it's causing tension between us. It's been affecting our work relationship and making it hard to collaborate effectively.
咨询师：That sounds like a challenging situation. Communication breakdowns can be frustrating and impact the overall work environment. How has this been affecting you personally?
来访者：It's been really stressful, to be honest. I feel like our ideas clash, and we don't understand each other. I'm worried that if this continues, our work quality will suffer.
咨询师：I completely understand how that could be overwhelming. Feeling out of sync with a coworker can add a lot of pressure and affect your motivation. Has there been any attempt to address this issue with your coworker?
来访者：I tried talking to them a couple of times, but they seem resistant to any kind of conversation. It's like they don't want to acknowledge the issue or work towards a solution.
咨询师：When direct communication doesn't work, you might consider involving someone else, like a supervisor or a mediator. They can help facilitate a constructive conversation and give a fresh perspective. Have you thought about seeking assistance from a higher authority?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I've thought about it, but I was hoping we could resolve it ourselves. The idea of involving others feels uncomfortable to me.
```

**description**：I'm having a hard time communicating with my coworker and it's causing tension in our work relationship.

---

### B-24. `extes_10948_4` — resist_fine | C2

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C2 / 回避-界限设定
- **scene（fine metadata）**：Work-related Stress and Burnout

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm afraid that if I speak up, I'll be seen as someone who can't handle the workload or is unable to meet expectations. Plus, what if nothing changes even after I talk to them?
```

**binary.context（对齐全文）**

```text
来访者：Yeah, it's just been really intense. I've been working long hours and juggling lots of projects. The worst part is that I'm not getting any additional support or resources. I'm constantly feeling overwhelmed and exhausted.
咨询师：I can only imagine how tough that must be for you. It sounds incredibly challenging to handle such a heavy workload without the necessary support. Feeling overwhelmed and exhausted is a normal reaction to such circumstances. It's important to remember that you're not alone in experiencing this.
来访者：Thank you for understanding. Sometimes it just feels like I'm drowning in work and I can't catch a break.
咨询师：I completely understand how it can feel that way, but it's vital to hold on to the fact that things can change. You have the strength to overcome this.
来访者：I hope so, but right now all I can see is this endless cycle of work with no way out.
咨询师：Starting with small steps can often lead to change. Have you considered having an open and honest conversation with your supervisor about your workload and the impact it's having on you? It might help address the issue.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm afraid that if I speak up, I'll be seen as someone who can't handle the workload or is unable to meet expectations. Plus, what if nothing changes even after I talk to them?
```

**description**：I have been feeling extremely overwhelmed with my workload lately and I'm starting to experience signs of burnout.

---

### B-25. `extes_9753_2` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
It's just really hard. I keep expecting him to greet me at the door or to hear his barks in the house. Everything feels so quiet now, and I can't help but feel aching sadness.
```

**binary.context（对齐全文）**

```text
咨询师：Hi there! How are you doing today?
来访者：Not so great. My dog recently passed away and I'm really struggling to cope with it. He was such a big part of my life and now there's just this emptiness.
咨询师：I'm so sorry to hear that. Losing a pet can feel incredibly painful, especially when they've been such an important part of our lives. It's completely natural to feel empty and lost without their presence. Can you share some special memories or moments you had with your dog?
来访者：Thank you for understanding. I have so many wonderful memories with him. Like when we used to go for long walks together, or how he would always curl up next to me whenever I was feeling down. I miss his wagging tail every time I came home.
咨询师：Those sound like such precious moments. Dogs have an incredible way of bringing us comfort and being loyal companions. It's obvious that your dog meant the world to you and brought so much joy to your life. It's completely normal to feel a deep sense of loss without him by your side.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
It's just really hard. I keep expecting him to greet me at the door or to hear his barks in the house. Everything feels so quiet now, and I can't help but feel aching sadness.
```

**description**：My dog passed away unexpectedly and I'm having a hard time coping with the loss. I feel so empty without him.

---

### B-26. `extes_1937_6` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you for sharing your experience. It gives me hope that I'll eventually feel better. Right now, it just feels like my world is falling apart.
```

**binary.context（对齐全文）**

```text
来访者：I hadn't thought about that. Do you think it could really help?
咨询师：Absolutely! Support groups can provide a safe space to share your feelings and connect with people who can relate to what you're going through. It's comforting to know that you're not alone. You might find it helpful to talk to others who have successfully moved on and can offer guidance based on their own experiences.
来访者：That sounds like a good idea. I'll give it a try. I just wish the pain would go away. I feel like I'll never find someone who made me as happy as she did.
咨询师：I understand your desire for the pain to fade, but it's important to remember that healing takes time. Instead of rushing the process, try focusing on self-care and personal growth. Rediscovering who you are as an individual can lead to finding someone who is truly compatible and makes you just as happy, if not happier, in the future. Have you considered engaging in activities that you enjoy and give you a sense of purpose?
来访者：I've been trying to keep busy, but it's hard to find joy in anything right now. How did you manage to find happiness after a breakup?
咨询师：Breakups can be incredibly difficult, but finding happiness after one is possible. It's all about taking small steps towards self-discovery. During my healing process, I focused on rediscovering old hobbies, connecting with loved ones, and practicing self-care. It's not an easy journey, but you will find moments of joy and happiness along the way.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you for sharing your experience. It gives me hope that I'll eventually feel better. Right now, it just feels like my world is falling apart.
```

**description**：After a painful breakup, my girlfriend and I decided to end our relationship. We had been together for five years and it's been really hard for me to move on.

---

### B-27. `extes_4142_5` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Conflicts or Communication Problems

**resist_fine.response（若 join 失败则仅此句）**

```text
I know, but sometimes I wonder if we're just not meant to be friends. Maybe we're just too different in how we communicate and it won't get better.
```

**binary.context（对齐全文）**

```text
来访者：It's been happening for a few weeks now. I feel like we're talking past each other and not really listening to what the other person is saying.
咨询师：It must be really frustrating when you feel like your friend isn't hearing you out. Can you give me an example of a recent misunderstanding?
来访者：Just the other day, we were planning a surprise gathering for our mutual friend. I suggested having it at their place, but my friend misunderstood and thought I was trying to pressure them into hosting. It turned into a huge argument.
咨询师：It's tough when simple suggestions get misinterpreted, leading to arguments. Feeling like your intentions aren't understood can be really frustrating. Have you tried discussing your communication issues with your friend outside of these arguments?
来访者：I've tried to bring it up, but it's hard to have a calm conversation without it escalating. It feels like my friend immediately becomes defensive and things get worse.
咨询师：That sounds really challenging. It's natural to feel frustrated when it seems impossible to have a peaceful conversation without defensiveness. Remember that you're not alone in experiencing difficulties like this.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I know, but sometimes I wonder if we're just not meant to be friends. Maybe we're just too different in how we communicate and it won't get better.
```

**description**：I'm feeling really frustrated with my friend because we've been having constant misunderstandings lately and it's becoming a strain on our friendship.

---

### B-28. `extes_4553_3` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I wish I could fast forward to the part where I'm happy again. It feels like an uphill battle to find joy on my own.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I'm really struggling with my recent divorce. It's been tough for me to move on and I feel overwhelmed. I could really use someone to talk to.
咨询师：Hi there, I'm here to listen. Can you tell me more about what you're going through?
来访者：I feel like everything has changed so suddenly. It's hard to accept that my marriage is over and it hurts knowing that I failed. I don't even know where to begin to heal.
咨询师：I can only imagine how deeply shifting and painful this loss must be for you. Remember that divorce doesn't signify failure; it's a complex and challenging situation that many people face. It's okay to feel hurt and overwhelmed. Take one step at a time as you navigate through this healing process. Your emotions are valid.
来访者：Thank you, I really need to hear that. It's just difficult adjusting to a life without my partner by my side. There's a void that I don't know how to fill.
咨询师：I understand how big of an adjustment this is for you. Losing someone who was once such a big part of your life can truly leave a void. Allow yourself the space to grieve and process your emotions. Know that it will take time to heal and eventually rediscover a new sense of fulfillment. Be patient with yourself.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I wish I could fast forward to the part where I'm happy again. It feels like an uphill battle to find joy on my own.
```

**description**：I recently got divorced and I'm having a hard time coping with the aftermath. I feel a mix of emotions including sadness, anger, and confusion. It's difficult for me to imagine a life without my ex-spouse and I could use some emotional support to help me navigate through this tough time.

---

### B-29. `extes_9751_2` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
I just can't seem to fill the void. I keep expecting her to come running when I open the front door or to jump on the bed in the morning, but she's not here anymore. It breaks my heart.
```

**binary.context（对齐全文）**

```text
咨询师：Hi, how are you doing today?
来访者：I'm struggling, to be honest. My dog passed away recently and I'm feeling lost without her. She was such an important part of my life and now there's just this emptiness.
咨询师：I'm really sorry to hear that. Losing a pet can be incredibly difficult, and it's obvious that your dog meant a lot to you. Grief is a complex emotion, and it's okay to feel empty and lost without your companion. Can you share some fond memories you have of your dog?
来访者：Thank you for understanding. I have so many cherished memories of her. Like when she used to greet me with wagging tail whenever I came back home, or the way she cuddled with me on the couch. She was always there for me, providing comfort and love.
咨询师：Those sound like such amazing moments. Dogs have a unique way of bringing joy and warmth into our lives. It's clear that your dog was a true companion and brought immense happiness to your home. It's completely natural to feel a deep sense of loss without her presence.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I just can't seem to fill the void. I keep expecting her to come running when I open the front door or to jump on the bed in the morning, but she's not here anymore. It breaks my heart.
```

**description**：I recently lost my beloved dog and I'm finding it hard to cope with the empty void in my life. I miss her companionship and the unconditional love she brought into my home.

---

### B-30. `extes_4669_4` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Conflicts or Communication Problems

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you for understanding. I don't know how to address this issue without causing more conflict.
```

**binary.context（对齐全文）**

```text
来访者：It's about my colleague. Lately, they've been ignoring my ideas and taking credit for my work, and it's driving me crazy.
咨询师：That sounds incredibly frustrating. Can you give me an example of when this happened?
来访者：Just yesterday, in our team meeting, I proposed a new strategy, but my colleague dismissed it and later presented it as their own idea.
咨询师：I can understand why you'd feel frustrated and undermined. It must be really disheartening to have your contributions disregarded.
来访者：Yes, exactly! It feels like my hard work is being stolen and my voice isn't being heard.
咨询师：I hear you. It's incredibly unfair that your colleague is not acknowledging your efforts and is taking credit for your work. You deserve to be recognized for your contributions.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you for understanding. I don't know how to address this issue without causing more conflict.
```

**description**：I'm feeling really frustrated with my colleague because they never listen to my ideas and keep taking credit for my work. It's causing a lot of tension in our team.

---

### B-31. `extes_3091_4` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Conflicts or Communication Problems

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't really spoken to anyone about this. I didn't want to burden my other friends or family with my relationship problems.
```

**binary.context（对齐全文）**

```text
来访者：I've been having a problem with my best friend. We had a falling out a few months ago, and we haven't spoken since. I miss our friendship, but I'm not sure how to initiate conversation or resolve the issues between us.
咨询师：That sounds really tough. A rupture in a close friendship can be incredibly painful and leave you feeling a sense of loss. How have you been feeling since this happened?
来访者：I've been feeling really upset and lonely. We used to talk and support each other all the time, and now there's just this void. It's been hard to move on from it.
咨询师：I can understand why you feel upset and lonely. Losing a valued friendship can be a profound loss, and it's completely normal to miss the connection and support you had. Have you considered reaching out to your friend to discuss the situation?
来访者：I've thought about it, but I'm afraid of making things worse. I don't want to push them away even further or face rejection if they're not ready to address the issues yet.
咨询师：It's completely understandable to have those fears. Have you ever talked to someone who might have a neutral perspective and be able to offer some guidance on how to approach the situation?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't really spoken to anyone about this. I didn't want to burden my other friends or family with my relationship problems.
```

**description**：I'm feeling upset because my best friend and I had a falling out and haven't spoken in months. I miss our friendship and don't know how to approach the situation to resolve it.

---

### B-32. `extes_10643_3` — resist_fine | D1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：D1 / 忽视-不关注
- **scene（fine metadata）**：Financial Worries and UncertAInty

**resist_fine.response（若 join 失败则仅此句）**

```text
You're right, I should try to stay positive and keep pushing forward. But it's hard to stay motivated when there's bills piling up and no income coming in.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I've been feeling really down lately and I could use someone to talk to. Are you available?
咨询师：Of course! I'm here for you. I can only imagine how tough things must be for you right now. Take your time and let's talk about it.
来访者：Thank you, I appreciate it. I lost my job a couple of months ago and I haven't been able to find a new one. It's been really hard to keep up with my expenses and the stress has been weighing me down.
咨询师：I'm really sorry to hear that. Losing a job can really take a toll, especially when it affects your financial stability. It's completely normal to feel overwhelmed. Have you been reaching out to any job search resources or networking?
来访者：I've been applying to jobs online and reaching out to contacts in my industry, but so far, I haven't had much luck. It's disheartening to receive constant rejections.
咨询师：I hear you. Job hunting can be discouraging, but remember that it only takes one opportunity to turn things around. Stay positive and remain persistent. Sometimes, the right opportunity just takes a bit more time to come along.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
You're right, I should try to stay positive and keep pushing forward. But it's hard to stay motivated when there's bills piling up and no income coming in.
```

**description**：I recently lost my job due to company downsizing and I'm struggling to find a new one. It's been hard to keep up with my bills and expenses, and I'm feeling overwhelmed and stressed about my financial future.

---

### B-33. `extes_8208_3` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you for your kind words. Take care!
```

**binary.context（对齐全文）**

```text
来访者：Hey, how's it going?
咨询师：Hello! I'm here to listen and support you. How are you feeling today?
来访者：I'm feeling really stressed out and overwhelmed. Work has been really tough lately.
咨询师：It sounds like work has been challenging for you. Can you tell me more about what's been going on?
来访者：I have a major project with a tight deadline, and I'm struggling to keep up. The problem is that I don't feel comfortable talking to my boss about it. I don't want to appear incapable or incompetent.
咨询师：I can understand why you might feel that way. It can be difficult to ask for help or express concerns without fearing negative judgments. Were there any specific instances that made you feel uncomfortable discussing your workload with your boss?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you for your kind words. Take care!
```

**description**：I've been feeling really stressed out at work lately. I have a tight deadline to meet, and I'm having trouble communicating with my boss about it.

---

### B-34. `extes_10773_5` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Depression and Low Mood

**resist_fine.response（若 join 失败则仅此句）**

```text
I've been trying to keep myself busy, but it's hard to find joy in activities that used to bring me happiness. I feel like there's a void inside me that I can't fill.
```

**binary.context（对齐全文）**

```text
来访者：I recently went through a breakup with my long-term partner, and ever since then, I've been feeling hopeless and lost. It's hard to imagine a future without them.
咨询师：I can only imagine how difficult and painful the breakup must be for you. Ending a long-term relationship can leave you feeling bereft and uncertain about the future. It's important to remember that healing takes time and you will eventually find your way forward. Have you been able to talk about your feelings with someone close to you or seek professional support?
来访者：I have spoken to a few friends who have been supportive, but I still can't shake this overwhelming sense of loss. I'm struggling to move on.
咨询师：It sounds like you're feeling stuck and finding it hard to move forward. It's completely normal to feel that way after a breakup. Remember that healing is a gradual process, and it's okay to give yourself time to grieve. Is there anything specific that you've been finding particularly challenging in moving on?
来访者：One of the things that's been really challenging is the constant reminders of our relationship. It feels like everywhere I turn, I'm reminded of the times we shared and it brings up a flood of emotions.
咨询师：I can understand how these reminders can bring back a rush of emotions and make it difficult to fully move forward. Sometimes, creating new routines and finding new places to spend time can help create new memories and lessen the impact of those reminders. Have you been able to explore any new hobbies or activities to redirect your focus?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I've been trying to keep myself busy, but it's hard to find joy in activities that used to bring me happiness. I feel like there's a void inside me that I can't fill.
```

**description**：I've been feeling extremely down and hopeless since my breakup with my long-term partner.

---

### B-35. `extes_5550_4` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't really looked into it. Maybe that could help, but I'm nervous about putting myself out there.
```

**binary.context（对齐全文）**

```text
来访者：I'm doing alright, but I've been having a hard time making friends in this new city.
咨询师：I'm sorry to hear that. It can be tough to make new connections, especially when you're feeling a bit anxious about it.
来访者：Yeah, it feels like everyone already has their own friend groups and I don't fit in.
咨询师：That must be really challenging to feel like you don't belong. It's completely normal to feel anxious when trying to make new friends.
来访者：I guess so, but it's frustrating. I want to have a social circle here.
咨询师：I understand. It's natural to want to have a sense of community and support. Have you considered joining any social groups or organizations in the city?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't really looked into it. Maybe that could help, but I'm nervous about putting myself out there.
```

**description**：I recently moved to a new city and I'm having trouble making friends. Whenever I try to initiate conversations with people, I feel anxious and end up stumbling over my words.

---

### B-36. `extes_2537_3` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Depression and Low Mood

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you so much for your kindness. Take care too!
```

**binary.context（对齐全文）**

```text
来访者：Hi
咨询师：Hello, how are you feeling today?
来访者：Honestly, not great. Lately, I've been feeling really isolated and unmotivated. I just can't seem to find the energy to do anything.
咨询师：I'm sorry to hear that. Feeling isolated and lacking motivation can be incredibly hard to cope with. It must be tough not having the drive to do the things you enjoy. Could you tell me more about what's been going on?
来访者：I've been working from home for several months now, and it's made me feel more disconnected from others. I miss the social interaction I used to have at the office. On top of that, I've been feeling exhausted all the time, and it's hard to find any motivation to engage in activities I used to enjoy.
咨询师：It sounds like working from home has affected your overall well-being and sense of connection. Is there anything specific that you used to enjoy before that you feel you can't find the energy for anymore?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you so much for your kindness. Take care too!
```

**description**：Struggling with feelings of isolation and lack of motivation

---

### B-37. `extes_2377_5` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Unemployment-related stress

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't really thought about that. I guess it's worth a shot. But I'm a bit hesitant to ask for help.
```

**binary.context（对齐全文）**

```text
来访者：Thank you for understanding. It's been really tough on me. I had been with the company for years and now I feel lost without it. I'm worried about finding another job in this economy.
咨询师：I can imagine how challenging it must be for you, especially after dedicating so much time and effort to your previous job. It's completely understandable to feel uncertain about what the future holds. It's important to remember that it's not a reflection of your abilities. Is there anything specific that concerns you about finding a new job?
来访者：One of my main concerns is that there aren't many job openings in my field right now. I've been searching but it feels like slim pickings.
咨询师：It sounds like you're feeling discouraged by the limited job opportunities available in your field. Is that right?
来访者：Exactly! It's frustrating because I've been sending out applications, but I haven't heard back from many places.
咨询师：I understand that it can be demoralizing not to receive responses. In addition to online job boards, have you considered reaching out to your network for potential job leads? Sometimes, personal connections can be a great resource for finding hidden job opportunities.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't really thought about that. I guess it's worth a shot. But I'm a bit hesitant to ask for help.
```

**description**：Feeling overwhelmed and uncertain about the future due to being recently laid off

---

### B-38. `extes_5838_2` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Communication Challenges

**resist_fine.response（若 join 失败则仅此句）**

```text
I've looked into a few clubs, but I haven't taken the leap to join any. I guess I'm just nervous about putting myself out there and not connecting with anyone.
```

**binary.context（对齐全文）**

```text
来访者：Hi
咨询师：Hello, how can I assist you today?
来访者：I've been feeling really lonely and isolated since I moved to a new city. It's been challenging for me to make friends, and I'm not sure what to do.
咨询师：I understand how difficult it can be to move to a new place and try to establish new connections. Feeling lonely and isolated is a natural response to being in an unfamiliar environment. It might take some time, but you can definitely overcome this. Have you tried joining any clubs or organizations related to your hobbies or interests?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I've looked into a few clubs, but I haven't taken the leap to join any. I guess I'm just nervous about putting myself out there and not connecting with anyone.
```

**description**：I recently moved to a new city and find it difficult to make friends, causing me to feel lonely and isolated.

---

### B-39. `extes_931_3` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I'm trying to stay positive, but it's tough. I keep thinking about all the memories we shared and it's making it harder to move on.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I just went through a breakup and I'm feeling really down and lost.
咨询师：Hi there. I'm really sorry to hear that. Breakups can be tough. Can you let me know more about what you're going through?
来访者：We were together for five years, but as time went on, we realized that we were growing apart and had different life goals. It's heartbreaking because we both still care about each other, but we could see that the relationship wasn't working anymore.
咨询师：That sounds really challenging. I can understand how difficult it must be to realize that even though you both care about each other, the relationship is no longer compatible. How are you feeling at the moment?
来访者：I'm feeling lost and devastated. It's hard to accept that the relationship has come to an end after investing so much time and love into it.
咨询师：I can really imagine how devastated and lost you must feel. Ending a long-term relationship can be incredibly painful. Remember to give yourself time to grieve and heal. It's okay to feel a rollercoaster of emotions right now.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I'm trying to stay positive, but it's tough. I keep thinking about all the memories we shared and it's making it harder to move on.
```

**description**：After being together for five years, my girlfriend and I recently broke up due to growing apart and having different life goals. I'm feeling lost and struggling to accept the end of our relationship.

---

### B-40. `extes_4680_3` — resist_fine | C1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：C1 / 回避-最小的回应
- **scene（fine metadata）**：Conflicts or Communication Problems

**resist_fine.response（若 join 失败则仅此句）**

```text
I haven't brought it up yet because I'm afraid it might lead to an argument or strain our relationship even more.
```

**binary.context（对齐全文）**

```text
来访者：Hey, can I talk to you about something that's been bothering me?
咨询师：Sure, I'm here to listen. What's been going on? You seem a bit troubled.
来访者：I've been avoiding discussing an ongoing issue with my roommate, and it's starting to affect our relationship. We've been having conflicts over cleanliness in our shared space.
咨询师：I'm sorry to hear that. Can you tell me more about what specifically has been causing conflicts between you and your roommate?
来访者：We have different standards when it comes to cleanliness. I prefer a tidy space, but my roommate is more relaxed about it. It's frustrating because I feel like I'm constantly cleaning up after them.
咨询师：It sounds like there's a difference in expectations and standards for cleanliness. Have you had a chance to communicate your concerns to your roommate?
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I haven't brought it up yet because I'm afraid it might lead to an argument or strain our relationship even more.
```

**description**：I've been avoiding discussing an ongoing issue with my roommate. We've been having conflicts over cleanliness in our shared space, and it's causing tension between us.

---

### B-41. `extes_9884_2` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Coping with the illness or death of a loved one

**resist_fine.response（若 join 失败则仅此句）**

```text
I know you're right, but I can't help but wish I had done more. I feel like I could have made him happier in his last days.
```

**binary.context（对齐全文）**

```text
来访者：Hi, I really need someone to talk to. I've been feeling so sad and guilty lately.
咨询师：Of course, I'm here for you. Tell me what's been going on. I'll listen.
来访者：Thank you, I appreciate it. My uncle recently passed away after a long illness, and it's hitting me hard. I can't help but feel guilty for not spending more time with him before he passed.
咨询师：I'm so sorry for your loss. Losing a loved one is never easy, especially when you harbor feelings of guilt. It's normal to have those thoughts, but remember that you did the best you could in the circumstances.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I know you're right, but I can't help but wish I had done more. I feel like I could have made him happier in his last days.
```

**description**：My uncle recently passed away from a prolonged illness. I'm struggling with grief and finding it hard to come to terms with his absence. I'm also feeling guilty for not being able to spend enough time with him before he passed.

---

### B-42. `extes_1994_3` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you. Sometimes I blame myself for not noticing any signs of illness earlier. Maybe I could have saved him.
```

**binary.context（对齐全文）**

```text
来访者：I'm feeling really down today. My childhood dog passed away unexpectedly, and I'm finding it hard to cope with the loss.
咨询师：Oh no, I'm so sorry to hear that. Losing a beloved pet can be incredibly tough, especially when it happens unexpectedly. It must be really heartbreaking for you. Can you tell me more about your dog?
来访者：Sure, my dog's name was Max. He was a loyal companion who was always there for me. We grew up together and shared so many happy memories.
咨询师：Losing a longtime companion can be particularly difficult. I remember when my childhood cat passed away, and it felt like a part of my childhood was gone too. It's amazing how pets become such integral parts of our lives.
来访者：Exactly, it feels like a piece of me is missing now. I keep thinking about our adventures and the love Max gave us.
咨询师：I completely understand how you feel. It's normal to feel intense sadness and grief right now. Max was more than just a pet; he was a family member. Your emotions are valid, and it's okay to grieve.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you. Sometimes I blame myself for not noticing any signs of illness earlier. Maybe I could have saved him.
```

**description**：My childhood dog passed away unexpectedly

---

### B-43. `extes_1285_3` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you, I really appreciate that. I can't help but blame myself for the end of our relationship.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I could really use someone to talk to right now. Can you lend an ear?
咨询师：Of course, I'm here for you. What's been going on?
来访者：I just went through a breakup with my partner. It's been really tough for both of us.
咨询师：I'm sorry to hear that. Breakups can be incredibly challenging and emotionally draining. How are you coping with it?
来访者：I'm feeling lost and heartbroken. I never thought it would come to this.
咨询师：It's completely understandable to feel that way. Ending a long-term relationship can be devastating. Take your time to process your emotions and seek support from loved ones who can offer their understanding and care.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you, I really appreciate that. I can't help but blame myself for the end of our relationship.
```

**description**：After a long-term relationship of four years, my partner and I have decided to break up. We have been struggling with communication and feeling disconnected in our relationship.

---

### B-44. `extes_10055_2` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
I understand, but it's just hard to accept that I couldn't do anything to save him.
```

**binary.context（对齐全文）**

```text
咨询师：Hi there, how are you doing today?
来访者：I'm feeling really down. My dog passed away suddenly last week and it's been really hard for me.
咨询师：I'm so sorry to hear about the loss of your dog. Losing a furry companion can be incredibly tough, especially when it happens unexpectedly. How are you coping with this heartbreaking situation?
来访者：It's been really difficult. I keep replaying the last moments in my head and blaming myself for not realizing sooner that something was wrong.
咨询师：I can imagine how painful it must be for you to replay those moments and feel a sense of guilt. It's important to remember that dogs can sometimes hide their pain or illnesses really well. Please try not to blame yourself. Your love and care for your dog were evident, and you couldn't have known what was going to happen.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I understand, but it's just hard to accept that I couldn't do anything to save him.
```

**description**：My dog passed away suddenly

---

### B-45. `extes_2332_2` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Financial Worries and Uncertainty

**resist_fine.response（若 join 失败则仅此句）**

```text
Thanks, but it's hard not to beat myself up about it. I should have been more careful with my money.
```

**binary.context（对齐全文）**

```text
来访者：Hi, how's it going?
咨询师：Hey there! I'm doing alright, thanks for asking. How about you?
来访者：To be honest, I'm feeling really down. I made a bad investment and now I'm in a financial mess. I don't know how to recover from this.
咨询师：I'm sorry to hear that. It can be really tough to go through a setback like this, especially when it involves your hard-earned savings. It's completely normal to feel stressed and uncertain right now. Just know that you're not alone.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thanks, but it's hard not to beat myself up about it. I should have been more careful with my money.
```

**description**：I recently invested my savings in a business venture that didn't go as planned. Now I'm facing a significant financial setback and I'm feeling stressed and uncertain about how to recover.

---

### B-46. `extes_9845_3` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Breakups or Divorce

**resist_fine.response（若 join 失败则仅此句）**

```text
I keep wondering what I did wrong and questioning my worth. It's been difficult to move past the self-blame.
```

**binary.context（对齐全文）**

```text
来访者：Hey, I've been feeling really down lately. Can we talk about something?
咨询师：Of course, I'm here for you. What's on your mind?
来访者：I recently ended a long-term relationship and it's been really tough for me.
咨询师：I'm so sorry to hear that. Breakups can be incredibly challenging and emotional. How have you been coping?
来访者：I've been feeling lost and empty. It's hard to adjust to being alone after spending so many years with someone.
咨询师：It's completely normal to feel that way after a breakup. It takes time to adjust to a new routine and the absence of someone you were so close to. Give yourself permission to grieve and take the time you need to heal.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I keep wondering what I did wrong and questioning my worth. It's been difficult to move past the self-blame.
```

**description**：My long-term partner and I recently ended our relationship after realizing that we wanted different things in life. We had built a life together and now I find myself starting over and trying to navigate this new chapter of my life.

---

### B-47. `extes_10223_2` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
Thank you for understanding. It means a lot. I just can't help but think of all the things I could have done differently to save him.
```

**binary.context（对齐全文）**

```text
咨询师：Hi there, how are you doing today?
来访者：Hey, I'm feeling really down since my dog passed away. He was my best friend, and I miss him so much.
咨询师：I'm so sorry to hear about the loss of your beloved dog. Losing a cherished pet can be extremely heartbreaking, especially after going through a difficult illness together. How have you been coping with this loss?
来访者：It's been really tough. I find myself crying a lot, and it's hard to come to terms with the fact that he's gone. I feel a huge void in my life without him.
咨询师：I can understand why you're feeling that way. Your dog was not just a pet but a true companion who shared so many special moments with you. It's natural to feel a void and struggle to adjust to life without him. It's okay to give yourself time to grieve and allow those emotions to come out.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
Thank you for understanding. It means a lot. I just can't help but think of all the things I could have done differently to save him.
```

**description**：My dog passed away after a long battle with illness

---

### B-48. `extes_1735_7` — resist_fine | B1

- **join_ok**：True
- **binary_label**：阻抗
- **fine_category / fine_label**：B1 / 否认-责怪
- **scene（fine metadata）**：Dealing with the Loss of a Pet

**resist_fine.response（若 join 失败则仅此句）**

```text
I really hope so. In the meantime, I can't help but blame myself for not being able to do more.
```

**binary.context（对齐全文）**

```text
来访者：Thank you for saying that. It's comforting to know that I'm not alone in feeling guilty.
咨询师：Of course, many pet owners experience these feelings of guilt after the loss of a pet. With time, you'll hopefully be able to focus more on the positive memories and the love you shared with your dog. The pain may never fully go away, but it will become more manageable.
来访者：I really hope so. Right now, it feels like the guilt is overpowering everything.
咨询师：During this healing process, remember to prioritize self-care. Engaging in activities that you enjoy, spending time with loved ones, and seeking support from friends or family can provide comfort and solace.
来访者：I'll try my best to take care of myself. It's just hard to find joy in anything right now.
咨询师：I understand that everything might seem gray at the moment. Grieving the loss of a pet takes time, and it's okay to feel the way you do. There will be ups and downs, but eventually, you'll find moments of happiness and peace amidst the sorrow.
```

**binary.response（应与 fine 一致场景下来访句）**

```text
I really hope so. In the meantime, I can't help but blame myself for not being able to do more.
```

**description**：My dog passed away and I'm struggling with feelings of guilt

---


*脚本：`extes_pipeline/audit_review_packet.py`*
