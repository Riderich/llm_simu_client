# MESC COT：缺口说明 + 随机抽检

## 一、为何有 fine 对话却不在 COT 里

当前 `cot_pipeline` 只对 **`binary_label` 非空的来访者轮** 建 COT（见 `cot_pipeline/dialogue.py::collect_eligible_units`）。

在 `mesc_fine_labeled.json` 中，**无任何可采样来访者轮** 的对话共 **6** 条：

- **`mesc_102`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False
- **`mesc_184`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False
- **`mesc_346`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False
- **`mesc_5`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False
- **`mesc_534`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False
- **`mesc_665`** — no client turn with binary_label (COT pipeline skips); client_turns=1, labeled_client=0, 已出现在 cot 文件: False

> 这 **不是** API 漏跑：即使用 `--merge-existing` 再跑，也会得到 **0 条新样本**。若要「补上」，需先在 fine 数据里为对应来访者轮打上 `binary_label`/`fine_label`（或放宽 COT 采样规则）。

---

## 二、从已有 COT 随机抽检（每条一段）

自 `mesc_cot.json` 随机 **8** 条（seed=42）。

### 1. `mesc_816` · turn_pos=4 · 合作 / `CBS5-认知探索`

- **cot_prompt_key**: `CBS5`
- **context（末几轮节选）**:
  client: Look... I lost Izzy a long time ago. But Russell, that... That was a bit of a shock.
  therapist: When did you separate?
  client: Two years ago. He had an affair.
  therapist: Yes, you said, with one of his students.
- **therapist_turn**: Yes, you said, with one of his students.
- **client_response**: Oh God, what a cliché, huh? I was faithful. I had a lot of jobs out of town. Many opportunities, but I resisted. He had to go and piss all over everything. Can I tell you something that I haven't told anyone?

**internal（解析后独白）**:

> [Perception] He keeps it plain, almost clinical: “two years ago,” “an affair,” “with one of his students.” It lands on the part of me that wants this to be simple, one clean explanation, because then I can keep standing on the high ground. I was faithful. I resisted. I did what I was supposed to do, even when I was away a lot. And yet here I am, two years later, still feeling like the whole thing was torn apart by something cheap and obvious. What I’m circling around is this: if I was the one who did everything “right,” then why does it still feel like I lost something I don’t know how to replace? And why am I suddenly thinking of telling him something I’ve never said out loud?
> 
> [Decision] I decided to say there’s something I haven’t told anyone because I want to test whether there’s more to this than just his betrayal and my outrage. If I say it out loud, maybe I can figure out whether I’m talking about the marriage, or the loneliness after it, or the fact that I’ve been acting as if I don’t need anything anymore. I’m still protecting myself by sounding sarcastic and in control, but underneath that I’m wondering if there’s a reason I’m bringing this up now — whether I’m looking for a way to explain why I’ve stayed shut down for so long, and whether I can admit that without giving up my dignity.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] He keeps it plain, almost clinical: “two years ago,” “an affair,” “with one of his students.” It lands on the part of me that wants this to be simple, one clean explanation, because then I can keep standing on the high ground. I was faithful. I resisted. I did what I was supposed to do, even when I was away a lot. And yet here I am, two years later, still feeling like the whole thing was torn apart by something cheap and obvious. What I’m circling around is this: if I was the one who did everything “right,” then why does it still feel like I lost something I don’t know how to replace? And why am I suddenly thinking of telling him something I’ve never said out loud?

[Decision] I decided to say there’s something I haven’t told anyone because I want to test whether there’s more to this than just his betrayal and my outrage. If I say it out loud, maybe I can figure out whether I’m talking about the marriage, or the loneliness after it, or the fact that I’ve been acting as if I don’t need anything anymore. I’m still protecting myself by sounding sarcastic and in control, but underneath that I’m wondering if there’s a reason I’m bringing this up now — whether I’m
```

---

### 2. `mesc_150` · turn_pos=2 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末几轮节选）**:
  client: I'm jealous of him, Cause he doesn't need anybody. He's got his own world. He's got his movies and books and computer games and chess. And the kid was born without a competitive bone in his body. Even
  therapist: haha..
- **therapist_turn**: haha..
- **client_response**: Don't you feel sorry for them? I swear, I don't know where he got those genes. Certainly not from me.

**internal（解析后独白）**:

> [Perception] The therapist’s little laugh landed like they were seeing the absurdity of it the way I do — this kid of mine, so unlike me, so calm inside himself, so impossible to push into my kind of world. What I was trying to lay out was the whole shape of it: I’ve tried to reach him in the ways I know how, I’ve tried to make something lively and competitive and father-son out of it, and he just stands there with this completely different logic. It feels less like a disagreement and more like he came out of a different branch of the species. So when I said I don’t know where he got those genes, I was trying to make that distance plain — to show it isn’t just me being difficult or him being ungrateful. It’s that he seems built around values I don’t understand.
> 
> [Decision] I decided to say it plainly instead of hiding the jealousy, because I wanted the therapist to finally see how much this hurts my pride and my sense of being his father. If I keep talking around it, it just sounds like a story about my son being “special.” What I actually mean is: he has something I don’t, and it makes me feel left out and inferior. And I don’t know what to do with that except point to the genes and hope that explains why I can’t get through to him.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] The therapist’s little laugh landed like they were seeing the absurdity of it the way I do — this kid of mine, so unlike me, so calm inside himself, so impossible to push into my kind of world. What I was trying to lay out was the whole shape of it: I’ve tried to reach him in the ways I know how, I’ve tried to make something lively and competitive and father-son out of it, and he just stands there with this completely different logic. It feels less like a disagreement and more like he came out of a different branch of the species. So when I said I don’t know where he got those genes, I was trying to make that distance plain — to show it isn’t just me being difficult or him being ungrateful. It’s that he seems built around values I don’t understand.

[Decision] I decided to say it plainly instead of hiding the jealousy, because I wanted the therapist to finally see how much this hurts my pride and my sense of being his father. If I keep talking around it, it just sounds like a story about my son being “special.” What I actually mean is: he has something I don’t, and it makes me feel left out and inferior. And I don’t know what to do with that except point to 
```

---

### 3. `mesc_36` · turn_pos=4 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末几轮节选）**:
  client: She started Asking me all sorts of annoying questions. She was really annoying So i refused to talk to her. She started talking to me like She knew me or something, so I refused to talk. And, That did
  therapist: Okay. So what happened at the accident That requires a-- A psychiatric opinion?
  client: I really don't remember what happened. I was on my bicycle and a car ran into me And i don't remember what happened next.
  therapist: What did they tell you afterwards?
- **therapist_turn**: What did they tell you afterwards?
- **client_response**: That i flew my bike right into the street.

**internal（解析后独白）**:

> [Perception] She was still pushing for some kind of explanation, like I’m supposed to supply a neat story about why I’m here and what’s wrong with me. That hit the part of this that annoys me most: people acting like they know what happened or what it means, when I don’t even remember the whole thing. So I laid out the basic facts instead — bike, car, then blank — and then what they told me after, because that’s all I’ve got. I wanted it to be clear that I’m not hiding some dramatic story; I literally don’t know.
> 
> [Decision] I decided to answer in the plainest way possible, just enough to stop the pointless digging and make her see the situation for what it is. If there’s a “psychiatric opinion” needed, fine, but I’m not going to pretend I remember something I don’t. I’m trying to keep control of the story by sticking to the facts other people told me, not by letting her put words in my mouth.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] She was still pushing for some kind of explanation, like I’m supposed to supply a neat story about why I’m here and what’s wrong with me. That hit the part of this that annoys me most: people acting like they know what happened or what it means, when I don’t even remember the whole thing. So I laid out the basic facts instead — bike, car, then blank — and then what they told me after, because that’s all I’ve got. I wanted it to be clear that I’m not hiding some dramatic story; I literally don’t know.

[Decision] I decided to answer in the plainest way possible, just enough to stop the pointless digging and make her see the situation for what it is. If there’s a “psychiatric opinion” needed, fine, but I’m not going to pretend I remember something I don’t. I’m trying to keep control of the story by sticking to the facts other people told me, not by letting her put words in my mouth.
</internal>
```

---

### 4. `mesc_947` · turn_pos=4 · 合作 / `CBS7-领悟`

- **cot_prompt_key**: `CBS7`
- **context（末几轮节选）**:
  client: I can't believe they married each other.
  therapist: Yeah.
  client: I can't believe I have a whole other set of parents out there somewhere. What do you think their house is like?
  therapist: I don't know. Anyway, I think that we should... we should talk about it next week. Let's both think about how you want to respond to your birth parent's letter, if that's what you decide to do.
- **therapist_turn**: I don't know. Anyway, I think that we should... we should talk about it next week. Let's both think about how you want to respond to your birth parent's letter, if that's what you decide to do.
- **client_response**: Okay. You know, I kind of feel like it's all gonna be okay for some reason. I don't know why.

**internal（解析后独白）**:

> [Perception] When they said we should talk next week about how I want to respond, it landed that they weren’t asking me to solve everything right now. I was stuck imagining this whole other family, their house, their lives, like if I could picture them enough it would make the letter less real. But what hit me was that the real thing in front of me is my choice — whether I answer — not me having to suddenly understand who they are or what they mean. It made the whole thing feel less like a shock I have to swallow all at once.
> 
> [Decision] So I decided I don’t have to force myself into certainty tonight. I can let it be unfinished and still be okay. I think that’s why it felt like it’s all gonna be okay — because maybe I don’t have to panic about the whole second set of parents right now. I can just take one step, and even if I don’t know what that step is yet, I’m not already ruined by this.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] When they said we should talk next week about how I want to respond, it landed that they weren’t asking me to solve everything right now. I was stuck imagining this whole other family, their house, their lives, like if I could picture them enough it would make the letter less real. But what hit me was that the real thing in front of me is my choice — whether I answer — not me having to suddenly understand who they are or what they mean. It made the whole thing feel less like a shock I have to swallow all at once.

[Decision] So I decided I don’t have to force myself into certainty tonight. I can let it be unfinished and still be okay. I think that’s why it felt like it’s all gonna be okay — because maybe I don’t have to panic about the whole second set of parents right now. I can just take one step, and even if I don’t know what that step is yet, I’m not already ruined by this.
</internal>
```

---

### 5. `mesc_375` · turn_pos=2 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末几轮节选）**:
  client: I just remembered how easily she could chip away at me and lure me back in. So I jumped in my car and I got the fuck out of there.
  therapist: In the middle of the night?
- **therapist_turn**: In the middle of the night?
- **client_response**: That's right.

**internal（解析后独白）**:

> [Perception] He was zeroing in on the part that made it sound extreme — leaving in the middle of the night — and that hit because it was exactly the point I was trying to make. It wasn’t some casual argument where I could just cool off. It felt like I could already feel her pulling me back into it, like I’d get sucked into the same thing all over again if I stayed one more minute. I wanted him to see that it wasn’t random or dramatic to me; it felt like the only way to stop myself from getting worn down and losing my footing.
> 
> [Decision] So I got in the car and left because I trusted that instinct more than staying and talking it out. I didn’t want to be lured back in, manipulated, or talked out of what I was feeling. Getting out of there was me trying to protect myself and keep some control over the situation, even if it looked impulsive from the outside.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] He was zeroing in on the part that made it sound extreme — leaving in the middle of the night — and that hit because it was exactly the point I was trying to make. It wasn’t some casual argument where I could just cool off. It felt like I could already feel her pulling me back into it, like I’d get sucked into the same thing all over again if I stayed one more minute. I wanted him to see that it wasn’t random or dramatic to me; it felt like the only way to stop myself from getting worn down and losing my footing.

[Decision] So I got in the car and left because I trusted that instinct more than staying and talking it out. I didn’t want to be lured back in, manipulated, or talked out of what I was feeling. Getting out of there was me trying to protect myself and keep some control over the situation, even if it looked impulsive from the outside.
</internal>
```

---

### 6. `mesc_332` · turn_pos=5 · 阻抗 / `B4`

- **cot_prompt_key**: `B4`
- **context（末几轮节选）**:
  client: He's an artist. It was his job. Besides, nudity was totally normal in my house. I got used to it.
  therapist: Nudity?
  client: Nude models. The female form. It's like drawing class 101, Paul. An artist must work from the purest inspiration. His studio was at home, so there were a lot of models walking around naked. It wasn't 
  therapist: So this was normal for you, to be exposed to adults being naked, yeah?
- **therapist_turn**: So this was normal for you, to be exposed to adults being naked, yeah?
- **client_response**: Exposed. Ooh, nudity. How scary. Breasts... Terrifying!

**internal（解析后独白）**:

> [Perception] He’s making it sound like this was some huge, damaging thing — like I was living in some creepy, sexually charged circus and should be messed up by it. That lands on the part of me that wants to protect my dad and my own memory of home. If I let it get inflated into “a major risk,” then suddenly my whole childhood gets recast as pathological, and I’m not okay with that. It was just nude models. Art stuff. Normal in that context. Not some catastrophic exposure.
> 
> [Decision] So I’m going to keep it small. I’m going to act like he’s overreading it, because if I admit it was serious, I have to start questioning my dad, my upbringing, and whether I’m supposed to be traumatized now. I don’t need to go there. It was weird to him maybe, but not to me. I can handle it. It’s not a big deal.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] He’s making it sound like this was some huge, damaging thing — like I was living in some creepy, sexually charged circus and should be messed up by it. That lands on the part of me that wants to protect my dad and my own memory of home. If I let it get inflated into “a major risk,” then suddenly my whole childhood gets recast as pathological, and I’m not okay with that. It was just nude models. Art stuff. Normal in that context. Not some catastrophic exposure.

[Decision] So I’m going to keep it small. I’m going to act like he’s overreading it, because if I admit it was serious, I have to start questioning my dad, my upbringing, and whether I’m supposed to be traumatized now. I don’t need to go there. It was weird to him maybe, but not to me. I can handle it. It’s not a big deal.
</internal>
```

---

### 7. `mesc_300` · turn_pos=6 · 合作 / `CBS4-叙述`

- **cot_prompt_key**: `CBS4`
- **context（末几轮节选）**:
  client: It was just so...
  therapist: So... So what, Amy? Is it worse than whispering I'm gonna kill you in your ear?
  client: Much worse. God, all that tenderness.
  therapist: Not your cup of tea. Why not?
- **therapist_turn**: Not your cup of tea. Why not?
- **client_response**: You know what? Sex like that is terrible. What we need is angry sex. That's what we had, it held us together. Even when we wanted to kill each other, we had that, maybe because we wanted to kill each other. This touchy-feely sex wasn't the deal. You know, the kind of sex we used to have, I couldn't even tell my girlfriends. They wouldn't have believed me, or else they'd call social services and ha

**internal（解析后独白）**:

> [Perception] He was making me explain it, like if he kept pressing, I’d have to admit something softer or more vulnerable than “it was a turnoff.” But what I wanted him to see was the whole shape of it: Jake has changed the terms completely. The sex is no longer this charged, rough, mutual collision that felt like us. Now it feels polite and careful and weirdly clinical, like he’s trying to handle me instead of meet me. And that makes me feel embarrassed, bored, and kind of cut off from the version of our relationship that actually felt alive.
> 
> [Decision] So I decided to spell it out in the most blunt way I could, because “touchy-feely” sounds too small for how wrong it feels. I wanted the therapist to understand that this isn’t just picky preferences or me being difficult — it feels like the thing that used to bind us together is gone, and what’s left is this unbearable tenderness that I can’t pretend to like. If I say it sharply enough, maybe he’ll finally hear that I’m not just rejecting sex; I’m reacting to losing the only kind of connection that ever made sense to me.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] He was making me explain it, like if he kept pressing, I’d have to admit something softer or more vulnerable than “it was a turnoff.” But what I wanted him to see was the whole shape of it: Jake has changed the terms completely. The sex is no longer this charged, rough, mutual collision that felt like us. Now it feels polite and careful and weirdly clinical, like he’s trying to handle me instead of meet me. And that makes me feel embarrassed, bored, and kind of cut off from the version of our relationship that actually felt alive.

[Decision] So I decided to spell it out in the most blunt way I could, because “touchy-feely” sounds too small for how wrong it feels. I wanted the therapist to understand that this isn’t just picky preferences or me being difficult — it feels like the thing that used to bind us together is gone, and what’s left is this unbearable tenderness that I can’t pretend to like. If I say it sharply enough, maybe he’ll finally hear that I’m not just rejecting sex; I’m reacting to losing the only kind of connection that ever made sense to me.
</internal>
```

---

### 8. `mesc_192` · turn_pos=10 · 阻抗 / `B7-不愿改变`

- **cot_prompt_key**: `B7`
- **context（末几轮节选）**:
  client: Rosie didn't come home on Tuesday. Said she'd be back late, but... In the morning, she wasn't there. She said she slept over at some friend's. Ian had a week off from college. He didn't even call, did
  therapist: How is it for the best?
  client: It's not for the best. It's a nightmare.
  therapist: It's painful. But in a way, you're free... to go through... whatever it is with Laura.
- **therapist_turn**: It's painful. But in a way, you're free... to go through... whatever it is with Laura.
- **client_response**: I wanted my wife to leave me for a salesman?

**internal（解析后独白）**:

> [Perception] He’s trying to turn my life into some kind of clean, therapeutic story — like because Kate is leaving, I should see this as “freedom” and maybe I should be okay moving on with Laura. That lands right on the worst part of it: the humiliation. Not just that my wife cheated, but that I’m supposed to calmly accept being left for some salesman and then act like this is some opportunity. It makes it sound like the problem is my attitude, not what she did.
> 
> [Decision] No. I’m not going to call this freedom, and I’m not going to pretend I want any part of it. I’m not going to rewrite being betrayed into some neat next step just because that’s easier to talk about in here. My line is simple: I will not participate in making this okay. I won’t dress it up, and I won’t go along with the idea that I should be grateful for it or move toward Laura like that’s the natural answer. It’s not. It’s a nightmare, and I’m not turning that into progress.

**raw_cot 前缀**（便于查 hallucination）:

```
<internal>
[Perception] He’s trying to turn my life into some kind of clean, therapeutic story — like because Kate is leaving, I should see this as “freedom” and maybe I should be okay moving on with Laura. That lands right on the worst part of it: the humiliation. Not just that my wife cheated, but that I’m supposed to calmly accept being left for some salesman and then act like this is some opportunity. It makes it sound like the problem is my attitude, not what she did.

[Decision] No. I’m not going to call this freedom, and I’m not going to pretend I want any part of it. I’m not going to rewrite being betrayed into some neat next step just because that’s easier to talk about in here. My line is simple: I will not participate in making this okay. I won’t dress it up, and I won’t go along with the idea that I should be grateful for it or move toward Laura like that’s the natural answer. It’s not. It’s a nightmare, and I’m not turning that into progress.
</internal>
```

---

