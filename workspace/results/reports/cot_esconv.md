# ESConv · COT 抽检与全量简析

## 一、全量统计（整份 JSON）

- **样本条数**（按轮/按任务一行）: **5720**
- **不同 `character_id`（对话）数**: **1300**
- **`internal` 为空或仅空白**: **1** （0.0%）
- **`raw_cot` 以 `ERROR:` 开头**: **0**
- **`internal` 字符数**: 均值 **805.4**, 中位数 **825**

**`cot_prompt_key` 频次（Top 15）** — 反映模板路由分布：

- `A2`: 2306（40.3%）
- `CBS4`: 1018（17.8%）
- `CBS6`: 753（13.2%）
- `CBS2`: 522（9.1%）
- `CBS3`: 209（3.7%）
- `B5`: 150（2.6%）
- `B4`: 150（2.6%）
- `A1`: 126（2.2%）
- `B1`: 86（1.5%）
- `CBS5`: 85（1.5%）
- `C1`: 73（1.3%）
- `B6`: 69（1.2%）
- `D2`: 49（0.9%）
- `D1`: 36（0.6%）
- `B3`: 25（0.4%）

## 二、简析（基于统计 + 下方随机条）

- 未见 `ERROR:` 前缀的失败行（粗检）。
- 空 `internal` 占比较低，解析整体可用。
- 路由以 **`A2`** 为主（40.3%），抽检时可重点看该键下独白是否与「合作/阻抗」任务一致。

下方随机条用于**质性**判断：是否贴咨询师上一句、是否编造对话中未出现的事实、英文/中文风格是否与数据集一致。

---

## 三、随机抽检

自 `workspace/results/cot/esconv.json` 随机 **8** 条（`--sample-size=8`, `seed=42`）。

### 1. `esconv_1188` · turn_pos=3 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末若干轮节选）**:
  therapist: Hello, how is your head or heart today?
  client: Hello, I would like to talk to someone about my situation at work.
  therapist: I hear you need someone to talk to. What is your situation at your work?
- **therapist_turn**: I hear you need someone to talk to. What is your situation at your work?
- **client_response**: My company is going through redundancies at the moment and I will not find out for another month if I am going to be included.

**internal（解析后）**:

> [Perception] They’re asking me to say what’s actually happening, so I’m laying it out plainly: this isn’t just general stress, it’s a real redundancy process and I’m left in limbo for a month. That uncertainty is the part that’s been weighing on me most — I can’t tell whether to brace for losing my job or try to carry on as normal. It feels important that they understand this is about not knowing if my income and stability are about to disappear.
> 
> [Decision] I’m going to keep it concrete so they can see why I’m anxious. If I explain the situation clearly enough, maybe they’ll understand that this isn’t something I can just breathe through or think positively about — it’s about waiting to find out whether I can keep paying my bills. I want them to grasp the reality of it before suggesting anything.

**raw_cot 前缀**:

```
<internal>
[Perception] They’re asking me to say what’s actually happening, so I’m laying it out plainly: this isn’t just general stress, it’s a real redundancy process and I’m left in limbo for a month. That uncertainty is the part that’s been weighing on me most — I can’t tell whether to brace for losing my job or try to carry on as normal. It feels important that they understand this is about not knowing if my income and stability are about to disappear.

[Decision] I’m going to keep it concrete so they can see why I’m anxious. If I explain the situation clearly enough, maybe they’ll understand that this isn’t something I can just breathe through or think positively about — it’s about waiting to find out whether I can keep paying my bills. I want them to grasp the reality of it before suggesting anything.
</internal>
```

---

### 2. `esconv_196` · turn_pos=13 · 阻抗 / `A2`

- **cot_prompt_key**: `A2`
- **context（末若干轮节选）**:
  therapist: No problem. I all ears
  therapist: What has you stressed out
  client: i am feeling pressured from the covid19 crisis
  client: job loss has effected me and i have no idea what to do
  therapist: I hear you there. Are you alone or friend s around
  therapist: What do you do work wise
- **therapist_turn**: What do you do work wise
- **client_response**: i have friends and family who also suffers from job loss

**internal（解析后）**:

> [Perception] They keep asking simple questions like they’re not really hearing me. Saying “Are you alone or friends around” and “What do you do work wise” feels like they’re fishing around instead of understanding that COVID has already shut down my whole life. It hits the part where I’m scared and overwhelmed because I need real help, not small talk. They sound like they want me to explain the obvious or maybe give advice that doesn’t fit my situation.
> 
> [Decision] I’m not going to just open up and let them lead me nowhere. If they can’t come with something concrete, I’ll keep my answers short and force them to be useful. I need real options, not someone acting like they’re helping while not actually getting what I’m dealing with.

**raw_cot 前缀**:

```
<internal>
[Perception] They keep asking simple questions like they’re not really hearing me. Saying “Are you alone or friends around” and “What do you do work wise” feels like they’re fishing around instead of understanding that COVID has already shut down my whole life. It hits the part where I’m scared and overwhelmed because I need real help, not small talk. They sound like they want me to explain the obvious or maybe give advice that doesn’t fit my situation.

[Decision] I’m not going to just open up and let them lead me nowhere. If they can’t come with something concrete, I’ll keep my answers short and force them to be useful. I need real options, not someone acting like they’re helping while not actually getting what I’m dealing with.
</internal>
```

---

### 3. `esconv_44` · turn_pos=1 · 阻抗 / `B6`

- **cot_prompt_key**: `B6`
- **context（末若干轮节选）**:
  therapist: Hi, how are you doing?
- **therapist_turn**: Hi, how are you doing?
- **client_response**: Hello. I suppose I could be doing better.

**internal（解析后）**:

> [Perception] She’s just opening the conversation, but even that lands on the same sore spot — that I’m not actually doing well, and I’m here because things with her feel like they’re sliding. If I answer too honestly, it all becomes real again: the distance, the possibility that I moved my life for nothing, the fear that I’m already losing her. If I act fine, I don’t have to face that yet.
> 
> [Decision] So I’ll stay vague for a second. “Could be doing better” says enough to be truthful without throwing everything on the table at once. I want to keep a little control here, protect myself from saying too much too fast, and see if this is a place where I can talk without immediately having to admit how bad it feels.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s just opening the conversation, but even that lands on the same sore spot — that I’m not actually doing well, and I’m here because things with her feel like they’re sliding. If I answer too honestly, it all becomes real again: the distance, the possibility that I moved my life for nothing, the fear that I’m already losing her. If I act fine, I don’t have to face that yet.

[Decision] So I’ll stay vague for a second. “Could be doing better” says enough to be truthful without throwing everything on the table at once. I want to keep a little control here, protect myself from saying too much too fast, and see if this is a place where I can talk without immediately having to admit how bad it feels.
</internal>
```

---

### 4. `esconv_499` · turn_pos=5 · 合作 / `CBS6-情感探索`

- **cot_prompt_key**: `CBS6`
- **context（末若干轮节选）**:
  client: Hi, how's your day going?
  therapist: Hello. Im doing good. How are you doing?
  therapist: Hello. Im doing good. How are you doing?
  client: Not so good unfortunately.
  therapist: Why. Can you talknto me about it?
- **therapist_turn**: Why. Can you talknto me about it?
- **client_response**: Due to this pandemic, I am fearful for my job security and future in general.

**internal（解析后）**:

> [Perception] The therapist actually asked me what was going on instead of brushing past it, and that made it feel a little safer to say the real thing. What hit me most is the uncertainty — the sense that the pandemic could take away my job and make my whole future feel unstable. I can feel how scared I am underneath the numbness and frustration.
> 
> [Decision] I decided to admit it plainly instead of pretending I’m just “fine.” I’m letting myself say I’m fearful because keeping it bottled up has been making it heavier, and maybe if I say it out loud, it’ll feel a little less isolating. I’m not ready to be optimistic, but I am ready to be honest about how much this is affecting me.

**raw_cot 前缀**:

```
<internal>
[Perception] The therapist actually asked me what was going on instead of brushing past it, and that made it feel a little safer to say the real thing. What hit me most is the uncertainty — the sense that the pandemic could take away my job and make my whole future feel unstable. I can feel how scared I am underneath the numbness and frustration.

[Decision] I decided to admit it plainly instead of pretending I’m just “fine.” I’m letting myself say I’m fearful because keeping it bottled up has been making it heavier, and maybe if I say it out loud, it’ll feel a little less isolating. I’m not ready to be optimistic, but I am ready to be honest about how much this is affecting me.
</internal>
```

---

### 5. `esconv_444` · turn_pos=5 · 阻抗 / `A2`

- **cot_prompt_key**: `A2`
- **context（末若干轮节选）**:
  therapist: Hello there, how is life treating you?
  client: Hello! Life is treating me fair, what about you?
  therapist: Well, I've been a bit worried this year due to Covid and everything. Have you been worrying about anything?
  client: Yes, not covid tho. Mostly, it's academics. It paralyses me.
  therapist: Do you work in academia then? Or are you a student?
- **therapist_turn**: Do you work in academia then? Or are you a student?
- **client_response**: I am a college student, and I miss my high school days.

**internal（解析后）**:

> [Perception] They immediately went to the most basic, surface-level question like they hadn’t even really heard me say “academics paralyses me.” Then when I said I’m a college student and miss high school, it felt like they were still just collecting labels instead of getting why this matters so much. It made me think they might not understand how intense this is for me, or they’re going to respond with generic, obvious stuff that doesn’t help. That annoyed me because I already feel shaky about this, and I don’t want to have to explain myself to someone who seems a step behind.
> 
> [Decision] So I’m going to keep it short and a little guarded. If they’re going to ask obvious questions, I’ll answer in a way that sounds fine and controlled, but I’m not going to give them the vulnerable part right away. I don’t really trust that they’ll get it, and I don’t want to hand over more of myself just to be misunderstood or told something useless.

**raw_cot 前缀**:

```
<internal>
[Perception] They immediately went to the most basic, surface-level question like they hadn’t even really heard me say “academics paralyses me.” Then when I said I’m a college student and miss high school, it felt like they were still just collecting labels instead of getting why this matters so much. It made me think they might not understand how intense this is for me, or they’re going to respond with generic, obvious stuff that doesn’t help. That annoyed me because I already feel shaky about this, and I don’t want to have to explain myself to someone who seems a step behind.

[Decision] So I’m going to keep it short and a little guarded. If they’re going to ask obvious questions, I’ll answer in a way that sounds fine and controlled, but I’m not going to give them the vulnerable part right away. I don’t really trust that they’ll get it, and I don’t want to hand over more of myself just to be misunderstood or told something useless.
</internal>
```

---

### 6. `esconv_402` · turn_pos=8 · 阻抗 / `A2`

- **cot_prompt_key**: `A2`
- **context（末若干轮节选）**:
  client: I have been better
  therapist: Do you want to tell me what happened?
  client: Well its happening still. I have end of term exams coming up and I have been trying real
ly hard to study but I am afraid I will fail my classes.
  therapist: Is there a reason for you to think that way?
  client: I havent done really well on the other tests. I turn in all my work and study hard but I can not seem to pass the exams
  therapist: First of all, try not to overthink right now and do your best to review your materials
- **therapist_turn**: First of all, try not to overthink right now and do your best to review your materials
- **client_response**: I have. I have been through the book, read my notes but when i take any practice tests, I still dont do as well as i would like.

**internal（解析后）**:

> [Perception] It sounded like they were brushing past how bad this actually feels. “Don’t overthink” and “review your materials” made it seem like they were treating this like I just needed a generic study tip, not that I’ve already been doing everything I can and still keep bombing the tests. It hit the part of me that’s terrified this means I’m just not capable, and instead of helping, they sounded kind of dismissive—like maybe they don’t really get how hard I’m trying.
> 
> [Decision] So I’m going to shut down a little and not act like that advice is useful, because I already know the obvious stuff and hearing it again just makes me feel more stupid. If they’re only going to give me a surface-level answer, then it doesn’t feel safe to admit how scared I am or how much this is getting to me. I’ll keep it to myself and just keep trying on my own, even if I’m frustrated.

**raw_cot 前缀**:

```
<internal>
[Perception] It sounded like they were brushing past how bad this actually feels. “Don’t overthink” and “review your materials” made it seem like they were treating this like I just needed a generic study tip, not that I’ve already been doing everything I can and still keep bombing the tests. It hit the part of me that’s terrified this means I’m just not capable, and instead of helping, they sounded kind of dismissive—like maybe they don’t really get how hard I’m trying.

[Decision] So I’m going to shut down a little and not act like that advice is useful, because I already know the obvious stuff and hearing it again just makes me feel more stupid. If they’re only going to give me a surface-level answer, then it doesn’t feel safe to admit how scared I am or how much this is getting to me. I’ll keep it to myself and just keep trying on my own, even if I’m frustrated.
</internal>
```

---

### 7. `esconv_249` · turn_pos=1 · 合作 / `CBS2-认同`

- **cot_prompt_key**: `CBS2`
- **context（末若干轮节选）**:
  therapist: Salutations
- **therapist_turn**: Salutations
- **client_response**: Hi there!

**internal（解析后）**:

> [Perception] He just greeted me politely, so I took it as a low-pressure opening to start talking without needing to defend anything. It felt easy because this is just the beginning and I don’t have to get into the work stuff yet.
> [Decision] I decided to respond normally and keep it simple so I could ease into the conversation. Saying “Hi there” felt natural and safe.

**raw_cot 前缀**:

```
<internal>
[Perception] He just greeted me politely, so I took it as a low-pressure opening to start talking without needing to defend anything. It felt easy because this is just the beginning and I don’t have to get into the work stuff yet.
[Decision] I decided to respond normally and keep it simple so I could ease into the conversation. Saying “Hi there” felt natural and safe.
</internal>
```

---

### 8. `esconv_180` · turn_pos=1 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末若干轮节选）**:
  therapist: Hello! How are you tonight?
- **therapist_turn**: Hello! How are you tonight?
- **client_response**: Hey. It's the middle of the day where I am located and I'm well thanks. I have the day off work today.

**internal（解析后）**:

> [Perception] She opened with a generic “how are you tonight,” and I immediately noticed it didn’t fit my actual situation. It’s daytime for me, and I’m off work, so the important thing to me was setting the scene properly rather than just answering on autopilot. I wanted her to understand I’m not in some late-night emotional slump right then — I’m just here in my own routine, with a bit of time to talk.
> 
> [Decision] I decided to correct the timing and mention I have the day off because that’s the real context for where I’m at. I’m trying to be straightforward without making a big deal of it — just giving the facts so she can get a clearer picture of my life instead of assuming.

**raw_cot 前缀**:

```
<internal>
[Perception] She opened with a generic “how are you tonight,” and I immediately noticed it didn’t fit my actual situation. It’s daytime for me, and I’m off work, so the important thing to me was setting the scene properly rather than just answering on autopilot. I wanted her to understand I’m not in some late-night emotional slump right then — I’m just here in my own routine, with a bit of time to talk.

[Decision] I decided to correct the timing and mention I have the day off because that’s the real context for where I’m at. I’m trying to be straightforward without making a big deal of it — just giving the facts so she can get a clearer picture of my life instead of assuming. 
</internal>
```

---

