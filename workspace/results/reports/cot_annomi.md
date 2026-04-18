# AnnoMI · COT 抽检与全量简析

## 一、全量统计（整份 JSON）

- **样本条数**（按轮/按任务一行）: **583**
- **不同 `character_id`（对话）数**: **133**
- **`internal` 为空或仅空白**: **0** （0.0%）
- **`raw_cot` 以 `ERROR:` 开头**: **0**
- **`internal` 字符数**: 均值 **722.4**, 中位数 **783**

**`cot_prompt_key` 频次（Top 15）** — 反映模板路由分布：

- `CBS2`: 136（23.3%）
- `C1`: 136（23.3%）
- `CBS4`: 83（14.2%）
- `A1`: 67（11.5%）
- `B7`: 38（6.5%）
- `B4`: 22（3.8%）
- `CBS5`: 20（3.4%）
- `B3`: 18（3.1%）
- `CBS3`: 15（2.6%）
- `B6`: 11（1.9%）
- `B1`: 10（1.7%）
- `C2`: 8（1.4%）
- `CBS6`: 6（1.0%）
- `B2`: 3（0.5%）
- `B5`: 3（0.5%）

## 二、简析（基于统计 + 下方随机条）

- 未见 `ERROR:` 前缀的失败行（粗检）。
- 空 `internal` 占比较低，解析整体可用。
- 路由以 **`CBS2`** 为主（23.3%），抽检时可重点看该键下独白是否与「合作/阻抗」任务一致。

下方随机条用于**质性**判断：是否贴咨询师上一句、是否编造对话中未出现的事实、英文/中文风格是否与数据集一致。

---

## 三、随机抽检

自 `workspace/results/cot/annomi.json` 随机 **8** 条（`--sample-size=8`, `seed=42`）。

### 1. `annomi_120` · turn_pos=4 · 阻抗 / `A1`

- **cot_prompt_key**: `A1`
- **context（末若干轮节选）**:
  client: Yeah, I suppose. I know my weight is a problem, but every time I try to take it off, I end up gaining it back. I don't know what to do.
  therapist: I know how you feel. Managing weight can be frustrating. Maybe we can just start trying to figure it out together and I'll be here to help you through the challenges.
  client: Okay, thank you doctor, but I'm just concerned about how I can possibly lose weight now since work is so busy and the kids take up so much of my time.
  therapist: Yeah, that's certainly understandable. We both know that there's a lot that plays into weight management, but there's no need to figure it all out today, especially since things are so busy for you right now. Maybe we co
  client: Okay, that sounds great. So, what should I do?
  therapist: Well, let's see. One of the things that's involved in managing weight and health is being active. Physical activity benefits the whole body. It's healthy for our joints, our stress levels, and especially for weight manag
- **therapist_turn**: Well, let's see. One of the things that's involved in managing weight and health is being active. Physical activity benefits the whole body. It's healthy for our joints, our stress levels, and especially for weight management. Perhaps we could talk about some ways of adding activity that fit into your life.
- **client_response**: I knew you were gonna say that, but I don't have time in my schedule. I can't afford to take an hour to go to the gym every day.

**internal（解析后）**:

> [Perception] He’s basically saying “just be more active,” like that’s the obvious fix, and it landed like he doesn’t really get what my life is actually like. I’m not refusing to do anything — I’m saying I already have a packed schedule with work and the kids, so the idea of carving out an hour for the gym every day feels unrealistic. What bothered me was the assumption that exercise means a big, separate block of time, because that makes it sound simple when it isn’t.
> 
> [Decision] I need to push back on that before it turns into another generic weight-loss lecture. I want him to understand that time is the barrier, not motivation, and that if this is supposed to be helpful it has to fit into real life. So I’m going to challenge the “just add activity” idea and make it clear that a gym plan won’t work for me.

**raw_cot 前缀**:

```
<internal>
[Perception] He’s basically saying “just be more active,” like that’s the obvious fix, and it landed like he doesn’t really get what my life is actually like. I’m not refusing to do anything — I’m saying I already have a packed schedule with work and the kids, so the idea of carving out an hour for the gym every day feels unrealistic. What bothered me was the assumption that exercise means a big, separate block of time, because that makes it sound simple when it isn’t.

[Decision] I need to push back on that before it turns into another generic weight-loss lecture. I want him to understand that time is the barrier, not motivation, and that if this is supposed to be helpful it has to fit into real life. So I’m going to challenge the “just add activity” idea and make it clear that a gym plan won’t work for me.
</internal>
```

---

### 2. `annomi_102` · turn_pos=0 · 合作 / `CBS2-认同`

- **cot_prompt_key**: `CBS2`
- **context（末若干轮节选）**:
  therapist: Hi, Liz. Well, thanks for meeting with me today.
- **therapist_turn**: Hi, Liz. Well, thanks for meeting with me today.
- **client_response**: Sure.

**internal（解析后）**:

> [Perception] She’s just greeting me and keeping things low-key, so this feels like a normal start rather than anything demanding.  
> [Decision] I can say sure and go along with it because there’s no pressure yet, and it’s easier to just be polite and see what she wants to talk about.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s just greeting me and keeping things low-key, so this feels like a normal start rather than anything demanding.  
[Decision] I can say sure and go along with it because there’s no pressure yet, and it’s easier to just be polite and see what she wants to talk about.
</internal>
```

---

### 3. `annomi_34` · turn_pos=16 · 阻抗 / `B7`

- **cot_prompt_key**: `B7`
- **context（末若干轮节选）**:
  client: Yeah.
  therapist: And then there's this other part of you that's- was thinking maybe it's not okay.
  client: Yeah, like, I should probably have trusted my gut.
  therapist: So, your gut is telling you what? Tell me about that.
  client: It's telling me that what I'm doing is wrong and it's probably hurting my kid and that- that I'm gonna really regret that once I actually get my kid.
  therapist: And you really wanna do what's best for your babe. And kind of wondering, um, how to move forward from here, is that where you wanna, you know, kind of focus in on, or what are your thoughts about giving up drinking alto
- **therapist_turn**: And you really wanna do what's best for your babe. And kind of wondering, um, how to move forward from here, is that where you wanna, you know, kind of focus in on, or what are your thoughts about giving up drinking altogether?
- **client_response**: Um, I'm definitely it's not-- I think I could probably do it. It's just- it-it comes hard when you're, like, in that moment. You're around your friends and they're drinking and you don't wanna be- you don't wanna be the mom at that moment. You wanna be yourself. You wanna be who you were before.

**internal（解析后）**:

> [Perception] She’s pushing me toward quitting drinking like it’s simple, like I should just accept being “the mom” now and leave my old life behind. That hits the part I’m scared of the most: if I change this, I’m not just giving up alcohol, I’m giving up my friends, my fun, and the version of me that still feels like me. It makes it sound like I have to become some totally different person, and I don’t want that. I can hear the judgment in my own head too, like if I don’t do this perfectly now then I’m already failing my baby.
> 
> [Decision] I’m not going to fully go there right now. I’m not ready to say I’m done with drinking or that I have to cut off that part of my life, because that feels like losing too much at once. I need to keep some piece of myself and my social life intact. If I’m forced to choose between being “the mom” and being myself, I’m drawing the line there — I’m not giving up who I am just because I’m pregnant.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s pushing me toward quitting drinking like it’s simple, like I should just accept being “the mom” now and leave my old life behind. That hits the part I’m scared of the most: if I change this, I’m not just giving up alcohol, I’m giving up my friends, my fun, and the version of me that still feels like me. It makes it sound like I have to become some totally different person, and I don’t want that. I can hear the judgment in my own head too, like if I don’t do this perfectly now then I’m already failing my baby.

[Decision] I’m not going to fully go there right now. I’m not ready to say I’m done with drinking or that I have to cut off that part of my life, because that feels like losing too much at once. I need to keep some piece of myself and my social life intact. If I’m forced to choose between being “the mom” and being myself, I’m drawing the line there — I’m not giving up who I am just because I’m pregnant.
</internal>
```

---

### 4. `annomi_28` · turn_pos=25 · 阻抗 / `C1`

- **cot_prompt_key**: `C1`
- **context（末若干轮节选）**:
  client: I would get a, um, a new prescription refilled thinking, "Oh I could try it this time."
  therapist: Mm-hmm.
  client: And I had friends that it worked for-
  therapist: Mm-hmm.
  client: Um, and there is a support group that they have that you can go online or call-
  therapist: Okay.
- **therapist_turn**: Okay.
- **client_response**: -but of course I didn't do either but-

**internal（解析后）**:

> [Perception] She’s pointing toward another possible way to quit, but it lands right on the spot I already feel exposed about: I keep saying I want to stop, and then I don’t really use the help that’s offered. It makes me sound half-committed, like maybe I’m just collecting ideas instead of actually changing. That’s uncomfortable because it touches the part where I know this isn’t just nicotine — it’s my routine, my stress relief, my comfort.
> 
> [Decision] So I kept it short and kind of vague. “Of course I didn’t do either” lets me admit the obvious without having to explain why I didn’t follow through or sit with the shame of it. If I stay brief, I don’t have to look too closely at how much I’m avoiding, and I don’t have to defend myself or get into the messy truth that I’m scared of failing again.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s pointing toward another possible way to quit, but it lands right on the spot I already feel exposed about: I keep saying I want to stop, and then I don’t really use the help that’s offered. It makes me sound half-committed, like maybe I’m just collecting ideas instead of actually changing. That’s uncomfortable because it touches the part where I know this isn’t just nicotine — it’s my routine, my stress relief, my comfort.

[Decision] So I kept it short and kind of vague. “Of course I didn’t do either” lets me admit the obvious without having to explain why I didn’t follow through or sit with the shame of it. If I stay brief, I don’t have to look too closely at how much I’m avoiding, and I don’t have to defend myself or get into the messy truth that I’m scared of failing again.
</internal>
```

---

### 5. `annomi_23` · turn_pos=0 · 合作 / `CBS2-认同`

- **cot_prompt_key**: `CBS2`
- **context（末若干轮节选）**:
  therapist: Hi, Hannah. Nice to meet you.
- **therapist_turn**: Hi, Hannah. Nice to meet you.
- **client_response**: Hi.

**internal（解析后）**:

> [Perception] She just greeted me normally and sounded calm, like this isn’t going to be a big thing right away. That makes it feel a little less scary to be here.
> [Decision] I can at least say hi back and go along with it for now, because I want help and I don’t need to make this harder than it is.

**raw_cot 前缀**:

```
<internal>
[Perception] She just greeted me normally and sounded calm, like this isn’t going to be a big thing right away. That makes it feel a little less scary to be here.
[Decision] I can at least say hi back and go along with it for now, because I want help and I don’t need to make this harder than it is.
</internal>
```

---

### 6. `annomi_127` · turn_pos=16 · 阻抗 / `C1`

- **cot_prompt_key**: `C1`
- **context（末若干轮节选）**:
  client: Mm-hmm, what's next, yeah, yeah.
  therapist: -what's next. Right. Okay. So, I mean, there is certainly a lot of evidence that pets in the home and the dander from their fur can make asthma worse.
  client: Mm-hmm.
  therapist: -but I wonder what are your experiences with Oscar, you know, when he's in the house or-or maybe sleeping near you or you're around him, what happens with your asthma symptoms?
  client: Well, we keep them clean, like he's cleaned. So, all the dander doesn't really make sense, but I have been noticing that sometimes when he comes on the bed or just beside, I wheeze a little bit, but I think it has to do 
  therapist: Okay.
- **therapist_turn**: Okay.
- **client_response**: So, I don't know if it's that-that's where I'm confused. I don't know how this could be happening.

**internal（解析后）**:

> [Perception] She’s still circling back to Oscar and acting like the dog could actually be part of the asthma problem. That hits the part of me that doesn’t want to believe it, because Oscar’s been around forever and he’s family. I can hear that she’s asking about my real experience, but all I feel is how much this would mean if it’s true — like I’d have to face the idea that something I love might be making me worse. That’s confusing and upsetting, especially with everything else I’m already trying to change.
> 
> [Decision] I’m going to keep it short and sort of half-agree without really committing, because if I go deeper I might have to admit I don’t know what to do and start thinking about giving Oscar up. I’m not ready to say that out loud. Saying “I don’t know how this could be happening” lets me stay in the confusion instead of making a choice I’m not ready for. It feels safer to keep it vague than to deal with the guilt, the loss, and the pressure of having to decide right now.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s still circling back to Oscar and acting like the dog could actually be part of the asthma problem. That hits the part of me that doesn’t want to believe it, because Oscar’s been around forever and he’s family. I can hear that she’s asking about my real experience, but all I feel is how much this would mean if it’s true — like I’d have to face the idea that something I love might be making me worse. That’s confusing and upsetting, especially with everything else I’m already trying to change.

[Decision] I’m going to keep it short and sort of half-agree without really committing, because if I go deeper I might have to admit I don’t know what to do and start thinking about giving Oscar up. I’m not ready to say that out loud. Saying “I don’t know how this could be happening” lets me stay in the confusion instead of making a choice I’m not ready for. It feels safer to keep it vague than to deal with the guilt, the loss, and the pressure of having to decide right now.
</internal>
```

---

### 7. `annomi_119` · turn_pos=27 · 阻抗 / `B6`

- **cot_prompt_key**: `B6`
- **context（末若干轮节选）**:
  client: - um, you know, I just, it, as soon as I asked about it, I just feel just like I'm not good enough-
  therapist: Okay.
  client: - since I don't have that.
  therapist: Yeah, so if you had something on your resume that was around education training, maybe a certificate of some kind of a field that you're interested in, that you would feel proud of yourself.
  client: Yeah. Well, something I could talk about in the interview too. You know, even if I was some type of certification where I could say, I could, you know, with confidence talk about- about that.
  therapist: Mm-hmm. Okay. What-- do you have any ideas as to what fields you might be interested in getting some more education, more training?
- **therapist_turn**: Mm-hmm. Okay. What-- do you have any ideas as to what fields you might be interested in getting some more education, more training?
- **client_response**: I mean, I guess, I just don't really know what it's gonna be because I need to have a job now so I'm not really sure.

**internal（解析后）**:

> [Perception] She’s asking me to think about education or training like I can just pick a direction, but I hear: “What do you want to do?” and all I can think is I need income now. It hits that sore spot of not knowing enough, not having a real path, and feeling like if I pick the wrong thing it’ll just prove I’m behind. I do like the idea of having something to say in an interview, something that makes me sound capable, but right now that feels far away from the immediate pressure of needing a job to keep things going.
> 
> [Decision] So I’m not saying no, because maybe training could help someday, and I do want to feel confident. But I’m not ready to commit to a field because I’m trying to protect myself from getting stuck in another thing I can’t finish or that won’t pay off soon enough. I need to keep the focus on finding work fast, because that feels more real and less risky than choosing a program when I already feel behind.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s asking me to think about education or training like I can just pick a direction, but I hear: “What do you want to do?” and all I can think is I need income now. It hits that sore spot of not knowing enough, not having a real path, and feeling like if I pick the wrong thing it’ll just prove I’m behind. I do like the idea of having something to say in an interview, something that makes me sound capable, but right now that feels far away from the immediate pressure of needing a job to keep things going.

[Decision] So I’m not saying no, because maybe training could help someday, and I do want to feel confident. But I’m not ready to commit to a field because I’m trying to protect myself from getting stuck in another thing I can’t finish or that won’t pay off soon enough. I need to keep the focus on finding work fast, because that feels more real and less risky than choosing a program when I already feel behind.
</internal>
```

---

### 8. `annomi_95` · turn_pos=0 · 阻抗 / `B7`

- **cot_prompt_key**: `B7`
- **context（末若干轮节选）**:
  therapist: Right. Hi, Ruth, thank you for coming today. How are you?
- **therapist_turn**: Right. Hi, Ruth, thank you for coming today. How are you?
- **client_response**: Um, okay. Just, I don't even know why I'm doing this anymore. I'm-I'm just so stupid. I'm such an idiot. I didn't know what the point of-of this is. I just- I just keep doing the same thing over and over, even though I know it can kill me. I just, I don't have any more willpower, ma'am. Yeah, [foreign language].

**internal（解析后）**:

> [Perception] She’s asking me to keep talking like this is something I can just choose my way out of, like I’m supposed to believe there’s some better option than the one I already know works. It hits the part where I feel like a burden and like I’m failing my mom every day. If I admit there’s another way, then I have to face all this pain and all this mess without the one “solution” that makes sense to me.
> 
> [Decision] I’m not going there. I’m not going to pretend I can do something different when I know I’ll just end up back here. I don’t want to argue about it or be pushed to hope for something I don’t believe in. I already decided what this means: I can’t fix this, and I won’t act like I can.

**raw_cot 前缀**:

```
<internal>
[Perception] She’s asking me to keep talking like this is something I can just choose my way out of, like I’m supposed to believe there’s some better option than the one I already know works. It hits the part where I feel like a burden and like I’m failing my mom every day. If I admit there’s another way, then I have to face all this pain and all this mess without the one “solution” that makes sense to me.

[Decision] I’m not going there. I’m not going to pretend I can do something different when I know I’ll just end up back here. I don’t want to argue about it or be pushed to hope for something I don’t believe in. I already decided what this means: I can’t fix this, and I won’t act like I can. 
</internal>
```

---

