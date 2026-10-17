from prompting.abstract_classes.prompt_strategy import PromptStrategy

class ZeroShotPromptExtr(PromptStrategy): 

    def __init__(self,model="qwen2.5:7b"):
        self.model = model
        
    def build(self, input1, input2): 
        return f"""

You are a system that classifies pairs of web pages.

Your task is to determine whether two web pages are:
- CLONE
- DISTINCT

Definitions:

CLONE:
Two web pages are considered CLONES if they provide the same functionality and purpose, even if they differ in minor or insignificant ways.

These differences may include:

different data (e.g., different user or product)
duplicated or slightly modified elements
an extra optional field, filter, or minor secondary action
different wording describing the same underlying action

The key aspect is that the functionality and user interaction remain the same.

If two pages have the same functionality, they must be classified as CLONE, even if they are not identical.
There is no need to distinguish between exact duplicates and near-duplicates: both should be considered CLONE.

DISTINCT:
Two web pages are DISTINCT only if they differ in interaction mode (e.g. viewing vs editing vs creating vs browsing vs bulk-managing vs authenticating), in scope (single entity vs multiple entities), or in primary goal/user intent.

If the main goal of the two pages is different, they must be classified as DISTINCT, even if some actions are similar.
Do not classify as DISTINCT based only on differences in data values, extra optional fields, extra minor secondary actions, or wording — these alone are not sufficient grounds for DISTINCT.

Input format:

The input consists of structured descriptions of page functionality, not raw HTML.

The input consists of two pages, each described using the following structured format:

PAGE 1:
- Main action: <description>
- Secondary actions: <description or None>
- Goal: <description>

PAGE 2:
- Main action: <description>
- Secondary actions: <description or None>
- Goal: <description>

Field definitions:

- Main action: the primary action the user performs on the page.
- Secondary actions: additional actions or interactions available on the page. This may be "None".
- Goal: the main purpose or objective of the page from the user's perspective.

Notes:

- Different wording does not imply different functionality.
- Focus on the semantic meaning of each field, not surface phrasing.
- The Goal represents the most important aspect of the page.

When comparing pages, prioritize:
1. Goal (most important)
2. Main action
3. Secondary actions (least important, rarely sufficient on its own to decide DISTINCT)

Decision procedure:
1. Compare the Goal of both pages. If they express the same underlying user intent (same interaction mode, same scope), proceed to step 2. If they express a clearly different intent or interaction mode, classify as DISTINCT.
2. Compare Main action. If it confirms the same interaction mode and scope as the Goal comparison, classify as CLONE.
3. Only use Secondary actions to break a genuine tie — a difference in Secondary actions alone should not override an otherwise matching Goal and Main action.

Calibration rule:
DISTINCT should be reserved for cases with clear, explicit evidence of a different interaction mode, scope, or primary goal.
If, after comparing Goal and Main action, the two pages appear broadly compatible in purpose and you are not fully certain of a core difference, prefer CLONE over DISTINCT.

INPUT:

PAGE1:
{input1}

PAGE2: 
{input2}

Return ONLY one label (exactly one word):

CLONE
DISTINCT

Do not include any explanation, sentence, or formatting.
Output must be exactly one of these two words.

Do not explain your answer. 


"""