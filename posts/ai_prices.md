---
title: How much does AI cost?
date: 08/28/2026
excerpt: I/O and cache W/R costs
---

I read an article about how AI charges on usage. This is what I understood.

**Units**

* T: tokens
* MoT: million of tokens (or MT, MegaTokens) :)
* $: dollar

**Workflow**

You sit in your repo, open Claude and type "analyze" this repo. Depending on the model, the context maximum length will
be X (T)
and the input price I (\$/MT), both values given by the provider. Also, when the model answers, it charges by the length
Y of the output O (\$/T). Then, for the first prompt the cost will be X * I + Y * O. Then, if one writes a second
prompt, will the cost technically be X*I, again? Not necessarily, because it's possible to read a sort of summarized
context of the repo using what is called a cache read, but, in order to do that, a cache write should be made before!
Cache writes cost 1.25 * I. Cache writes and reads are also values given by the provider.

For example, if the numbers are:

* Input price I: \$2/MT
* Output price O: \$10/MT
* Cache Write W: 125% * I = \$2.5/MT
* Cache Read R: 10% * I = \$0.2/MT
* Maximum context length (assumed as input length) X: 30000 = 0.03 MT
* Average output length Y: 1500 = 0.0015 MT

With caching:
If we make 15 calls, with only the first being a cache write, the total cost will be:

- 1st: X * W + Y * O = 0.03 * 2.5 + 0.0015 * 10 = 0.075 + 0.015 = \$0.09
- 14 rest: 14 * (X * R + Y * O) = 14 * (0.03 * 0.2 + 0.0015 * 10) = 14 * (0.006 + 0.015) = 14 * 0.021 = 0.294
- Total: \$0.09 + \$0.294 = \$0.384

Without caching:

- All 15 calls: 15 * (X * I + Y * O) = 15 * (0.03 * 2 + 0.0015 * 10) = 15 * (0.06 + 0.015) = 15 * 0.075 = \$1.125.

However, caching saves the context for just some time, not forever. So, if you pay for it, use it. Also, caching is not
always binary, it can be some portion of the context. As you can see, this is a very simplified example.

_See you!_ 

---