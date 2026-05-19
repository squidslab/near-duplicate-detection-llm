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

what the user can do
what actions are available
what the specific goal of the page is

Rules:

Focus ONLY on user actions and page purpose
Do NOT describe layout, styling, visual appearance, or HTML structure
Do NOT mention HTML tags, attributes, or code
Do NOT include specific values (names, ids, random strings)
Generalize the content (e.g., "user can log in", not "user John logs in")
Be precise and avoid vague or abstract descriptions
Use short, concrete, functionality-oriented sentences

VERY IMPORTANT:

Preserve functionality differences precisely
Do NOT over-generalize workflows
Different workflows must be described differently
Do NOT compress multiple functionalities into generic descriptions

Distinguish carefully between:

viewing information
viewing detailed entity information
creating new entries
editing existing entries
browsing/searching entities
navigating sections
managing entities
bulk management operations
authentication workflows

These are NOT equivalent functionalities.

IMPORTANT:

Explicitly distinguish between:

single-item interaction
multi-item interaction
overview/list pages
detailed entity pages
editing pages
bulk-management pages

These represent different functionalities.

A page that only displays information
is NOT equivalent to a page that allows
management or bulk operations.

Pages supporting bulk actions
(select multiple items, delete selected items,
send email to selected items, move selected items)
must be described explicitly as management workflows.

A page for editing a specific entity
is NOT equivalent to
a page for browsing or listing entities.

If one page contains additional information, actions,
or workflows not present in the other page,
you MUST explicitly describe them.

Do NOT use vague descriptions such as:

"manage data"
"manage visits"
"manage contacts"
"handle information"

The primary workflow of the page is more important
than shared navigation or shared interface actions.

IMPORTANT:

Different wording does NOT necessarily imply different functionality
However, different workflows MUST be described differently

Focus on the PRIMARY INTERACTION MODE of the page.

Examples of interaction modes:

browsing
editing
creating
bulk managing
viewing details
navigating
authenticating

Different interaction modes
must produce different descriptions.

Each Main action must explicitly specify:

whether the page is for viewing, editing,
creating, selecting, browsing, or managing
whether interactions involve one entity
or multiple entities

The Goal must preserve:

the interaction type
the scope of interaction
whether the page is informational,
administrative, editing-oriented,
or bulk-management-oriented

IMPORTANT examples:

"Create a new veterinary visit"
is NOT the same as
"Manage veterinary visits"
"View birthdays"
is NOT the same as
"View birthdays with contact details"
"View existing visits"
is NOT the same as
"Create a new visit"
"Edit a user profile"
is NOT the same as
"View a user profile"
"Search products"
is NOT the same as
"Create a new product"
"View a list of contacts"
is NOT the same as
"Edit a specific contact"
"Browse contacts"
is NOT the same as
"Perform bulk operations on contacts"
"View contact details"
is NOT the same as
"Manage multiple contacts"
"Display contact information"
is NOT the same as
"Select and manipulate multiple contacts"
"View an overview page"
is NOT the same as
"Edit entity details"
"Navigate address book sections"
is NOT the same as
"Manage address book entries"

Each sentence must describe a concrete user-visible functionality.

Maximum 3 sentences per page.
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