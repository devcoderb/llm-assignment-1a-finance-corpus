import sys, ast, nbformat
v4 = nbformat.read("v4-after-kube.ipynb", as_version=4)
v3 = nbformat.read("Assignment-1a-v3.ipynb", as_version=4)
S = lambda c: c.source
def first(c):
    s = S(c).strip()
    return s.splitlines()[0].strip() if s else ""
def idx(nb, prefix, kind=None):
    for i, c in enumerate(nb.cells):
        if (kind is None or c.cell_type == kind) and first(c).startswith(prefix):
            return i
    raise SystemExit("not found: " + prefix)
log = []

# 1. Stage 5C heading wrongly stored as a code cell
i = idx(v4, "### Stage 5C: Model Architecture", "code")
v4.cells[i] = nbformat.v4.new_markdown_cell(S(v4.cells[i]).strip()); log.append("5C heading -> markdown")

# 2. stray character in Stage 10A
i = idx(v4, "# Stage 10A:", "code")
v4.cells[i].source = v4.cells[i].source.replace("qlora_outputs = []a", "qlora_outputs = []"); log.append("10A stray 'a' removed")

# 3. restore validation lines in 4C / 4D from v3
for p in ("# Stage 4C:", "# Stage 4D:"):
    v4.cells[idx(v4, p, "code")].source = S(v3.cells[idx(v3, p, "code")]); log.append(p + " restored from v3")

# 4. move the CPT perplexity observation to just after the 7B code cell
o = idx(v4, "#### CPT Perplexity Observation", "markdown")
cell = v4.cells.pop(o)
v4.cells.insert(idx(v4, "# Stage 7B:", "code") + 1, cell); log.append("7B observation moved")

# 5. missing headings for 9B and 9I (taken from v3)
for head, code in (("#### Stage 9B:", "# Stage 9B:"), ("#### Stage 9I:", "# Stage 9I:")):
    h = v3.cells[idx(v3, head, "markdown")]
    v4.cells.insert(idx(v4, code, "code"), nbformat.v4.new_markdown_cell(S(h).strip())); log.append("heading added: " + head)

# 6. stale / placeholder text
def set_md(prefix, text):
    v4.cells[idx(v4, prefix, "markdown")] = nbformat.v4.new_markdown_cell(text.strip())
set_md("#### SFT Configuration Observation", """
#### SFT Configuration Observation

QLoRA fine-tuning runs for 5 epochs on 23 examples (effective batch 4, 25 optimizer steps) at a learning rate of 2e-4, with a maximum sequence length of 512 tokens. The adapter weights are kept in fp32, with the 4-bit base model computing in fp16, which gives stable training. The 6 evaluation examples are held out to monitor evaluation loss and to check for overfitting on such a small training set.
""")
set_md("#### QLoRA Training Observation", """
#### QLoRA Training Observation

QLoRA instruction fine-tuning ran for 5 epochs (25 optimizer steps) with a mean training loss of 2.9333 and a final logged training loss of 2.8564.

Validation loss was recorded at 4 evaluation points and decreased at each one, from 2.8972 to 2.7781 (about 4%). The final value is the lowest observed, and no divergence appeared. The decrease is steady but modest, and with only 6 evaluation examples it should be read as an indication, not a precise measure. Batch-level training loss is noisier because each logged value averages only a few small updates. Mean token accuracy was not available in the training log.

The loss is higher than during CPT (about 1.5) because the model is learning a new question-answer format from 23 short examples, not continuing long documents.
""")
set_md("### Final Model Comparison", """
### Final Model Comparison

| | Base | After CPT | After CPT + QLoRA |
|---|---|---|---|
| Held-out perplexity | 7.97 | 6.63 | not measured |
| "Explain..." prompts | Direct, fluent answers | Continues as exam-style questions | Direct start, but does not stop |
| Domain facts | Several errors (e.g. UPI "open-source") | Errors remain; invents statistics and sources | Errors remain; invents a person and a source |
| Buy-back definition | Correct | Incorrect (called an IPO) | Incorrect (called an IPO) |
| General knowledge | Intact | Mostly retained; one instruction-style prompt regressed | Not separately tested |

CPT adapted the model's language statistics to the corpus (held-out perplexity down 16.8%) but did not make it a reliable source of domain facts. QLoRA on 23 examples partly repaired the answer format but not the stopping behaviour or the factual errors. With 0.43M CPT tokens and a very small instruction set, the main measurable result is the perplexity improvement. A larger corpus and a larger set of grounded instruction examples would be needed for reliable domain question answering.
""")
log.append("stale text fixed (104, 107, final comparison)")

# check: every code cell parses
bad = 0
for i, c in enumerate(v4.cells):
    if c.cell_type == "code":
        s = "\n".join(l for l in c.source.splitlines() if not l.lstrip().startswith(("%", "!")))
        try: ast.parse(s)
        except SyntaxError as e: bad += 1; print("SYNTAX", i, first(c)[:50], e.msg)
for c in v4.cells:
    if c.cell_type == "code": c.outputs = []; c.execution_count = None
nbformat.validate(v4)
nbformat.write(v4, "Assignment-1a-v4.ipynb")
print(len(v4.cells), "cells,", bad, "syntax errors ->", "Assignment-1a-v4.ipynb")
for l in log: print(" -", l)
