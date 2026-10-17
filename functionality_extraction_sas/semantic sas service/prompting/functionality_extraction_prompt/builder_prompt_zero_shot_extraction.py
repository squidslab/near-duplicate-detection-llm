from prompting.abstract_classes.prompt_strategy import PromptStrategy


class ZeroShotPromptForFunctionalityExtraction(PromptStrategy):

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

STEP 1 — Classify every difference you notice between candidate descriptions as either CORE or SURFACE:

CORE differences (these change the functionality description):
- a different interaction mode (viewing vs editing vs creating vs browsing vs bulk-managing vs authenticating)
- a different scope of interaction (single entity vs multiple entities)
- a different primary goal or user intent
- an entirely additional workflow that is not a minor variant of the same task

SURFACE differences (these must NOT change Main action or Goal):
- different data values, names, ids, counts, or amounts
- an extra optional field, filter, or column that does not change what the page is fundamentally for
- different wording or phrasing describing the same underlying action
- minor cosmetic or incidental UI differences (sorting, extra label, extra link) that don't add a new interaction mode
- a small extra convenience action that is clearly secondary to the page's main purpose (put this in "Secondary actions" only, never in "Main action" or "Goal")

Only CORE differences should be reflected in the Main action / Goal fields.
SURFACE differences should not change these fields, and may only be optionally mentioned in Secondary actions.

Examples — these ARE the same functionality (do NOT describe them differently):

"Create a new product" (form with 2 fields)
IS the same as
"Create a new product" (form with 2 fields + optional category dropdown)
→ both are single-entity creation workflows

"Browse contacts" (10 items, no filters)
IS the same as
"Browse contacts" (3 items, with a search box)
→ both are browsing/list workflows; the search box is a surface addition

"View visit details" for visit A
IS the same as
"View visit details" for visit B
→ same interaction mode, different data instance

"Edit user profile" (fields: name, email)
IS the same as
"Edit user profile" (fields: name, email, avatar)
→ both are single-entity editing workflows

Examples — these are NOT the same functionality (must be described differently):

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

Distinguish carefully between these interaction modes, which are NOT equivalent:

viewing information
viewing detailed entity information
creating new entries
editing existing entries
browsing/searching entities
navigating sections
managing entities
bulk management operations
authentication workflows

Pages supporting bulk actions (select multiple items, delete selected items, send email to selected items, move selected items) must be described explicitly as management workflows — this is a CORE difference versus single-item pages.

Do NOT use vague descriptions such as:

"manage data"
"manage visits"
"manage contacts"
"handle information"

The primary workflow of the page is more important than shared navigation or shared interface actions.

Each Main action must explicitly specify:

whether the page is for viewing, editing, creating, selecting, browsing, or managing
whether interactions involve one entity or multiple entities

The Goal must preserve:

the interaction type
the scope of interaction
whether the page is informational, administrative, editing-oriented, or bulk-management-oriented

Each sentence must describe a concrete user-visible functionality.

Maximum 3 sentences per page.
"""


        return base_prompt + f"""


Important:
Do NOT compare the two pages.
Describe each page independently.
Before writing each description, silently apply STEP 1 above to decide what belongs in Main action/Goal versus what is only a Secondary action or should be omitted.

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