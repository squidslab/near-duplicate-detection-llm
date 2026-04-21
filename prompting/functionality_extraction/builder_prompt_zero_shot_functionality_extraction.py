from prompting.interfaces import PromptStrategy 

class ZeroShotPromptForFunctionalityExtraction(PromptStrategy): 

    def __init__(self, input_type="html"):
        self.input_type = input_type

    def uses_images(self):
        return self.input_type == "image"
    
        
    def build(self, input1, input2): 
        
        base_prompt = """  
You are an expert in analyzing web application functionality.

You are given two HTML pages.

Your task is to extract the FUNCTIONALITY of each page independently.

A functionality description must clearly describe:
- what the user can do
- what actions are available
- what the goal of the page is

Rules:

- Focus ONLY on user actions and purpose
- Do NOT describe layout, styling, or HTML structure
- Do NOT mention HTML tags or code
- Do NOT include specific values (names, ids, random strings)
- Generalize the content (e.g., "user can log in", not "user John logs in")
- Be precise and avoid vague sentences

VERY IMPORTANT:
- Highlight differences in functionality if they exist
- Do NOT over-generalize (avoid sentences like "user can manage things")
- Each sentence must describe a concrete action

Maximum 3 sentences per page

"""
        

        if self.input_type == "html":
            return base_prompt + f"""


Important:
Do NOT compare the two pages.
Describe each page independently.

Now describe the following pair:

Page 1:
<<<HTML START>>>
{input1}
<<<HTML END>>>

Page 2:
<<<HTML START>>>
{input2}
<<<HTML END>>>

Output format (STRICT):

PAGE 1:
- Main action: <one sentence>
- Secondary actions: <one sentence>
- Goal: <one sentence>

PAGE 2:
- Main action: <one sentence>
- Secondary actions: <one sentence>
- Goal: <one sentence>


/no_think
"""


        elif self.input_type == "image":
            return base_prompt + """

          
You are given two screenshots of web pages. 

The images may contain UI elements, layouts, and visual structure. 

IMPORTANT:
Focus on FUNCTIONALITY by analyzing visible UI elements.

Pay attention to:
- input fields (text boxes, search bars, login forms)
- buttons (submit, login, add to cart, navigation)
- links and menus
- forms and interactive components

Use these elements to infer what actions a user can perform.

If two pages contain the same functional UI elements and appear identical in structure, layout, and content, classify them as CLONE.

If two pages contain similar functional UI elements that enable the same user actions but differ in content, layout, or visual details, classify them as CLONE.

Use DISTINCT only if the pages clearly contain different types of interactive elements or support different user actions.

Ignore differences in colors, styles, text content, or layout if the core UI elements and functionality are the same.

Do not rely on overall layout similarity.
Focus on the presence and role of interactive elements.

Page 1: [IMAGE]
Page 2: [IMAGE]

Return ONLY one label (exactly one word):

CLONE
DISTINCT

Do not include any explanation, sentence, or formatting.
Output must be exactly one of these three words.

Do not explain your answer.

Always choose exactly one label based on functionality, even if the decision is difficult. 

/no_think
"""

        else:
            raise ValueError("Invalid input_type. Use 'html' or 'image'")