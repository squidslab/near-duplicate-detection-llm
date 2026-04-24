from prompting.interfaces import PromptStrategy 

class ZeroShotPromptExtr(PromptStrategy): 

    def __init__(self, input_type="html",model="qwen2.57b"):
        self.input_type = input_type
        self.model = model

    def get_metadata(self):
        return {
            "model" : self.model,
            "prompt_type": "zero-shot(Functionality-Extracted Input)", 
            "num_examples_for_prompt": 0,
            "input_type": "Structured semantic representation",
            "description": f"Zero-shot prompting with functionality extraction strategy and {self.input_type} input."
        }    

    def uses_images(self):
        return self.input_type == "image"
        
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

The key aspect is that the functionality and user interaction remain the same.

If two pages have the same functionality, they must be classified as CLONE, even if they are not identical.
There is no need to distinguish between exact duplicates and near-duplicates: both should be considered CLONE.

DISTINCT:
Two web pages are DISTINCT if they differ in functionality or purpose.

If the main goal of the two pages is different, they must be classified as DISTINCT, even if some actions are similar.

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
- Focus on the semantic meaning of each field.
- The Goal represents the most important aspect of the page. 

When comparing pages, prioritize:
1. Goal (most important)
2. Main action
3. Secondary actions (least important) 

If the Goal expresses the same underlying user intent or purpose, the pages are likely CLONE, even if described using different wording.
If the Goal expresses a different user intent or purpose, the pages must be classified as DISTINCT.

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