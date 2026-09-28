"""Build long-form reasoning prompts in several editorial styles."""

from __future__ import annotations

import random

FORMAT_LIST = ["educ","stor","tech","news","blog","wiki","maga"]
FORMAT_WEIGHTS =[2,2,2,2,2,2,2]
EXAMPLE_DICT = {
"educ": 
"""
Title: Unlocking Medical Logic: A Lesson in Deduction

Welcome! Today, we will analyze a clinical case to understand how doctors use deductive reasoning to reach a diagnosis. We won't just guess; we will build a logical chain based on evidence.

The Scenario:
A patient arrives at the clinic. We don't know the specific illness yet, but we have observed two critical premises based on the doctor's initial assessment and actions:
1. Premise A: The patient has been prescribed antibiotics.
2. Premise B: The patient is presenting with severe respiratory symptoms.

Let's break down the logical derivation step-by-step.

Step 1: Establishing the Treatment Logic (Implication)
First, we look at the medication. In medical practice, antibiotics are strictly used to treat bacterial infections, not viral ones (like the flu).
* Logical Rule: If a patient is prescribed antibiotics, then the doctor must suspect a non-viral (bacterial) cause.
* Deduction: Since Premise A is true (antibiotics were prescribed), we can infer that the infection is not viral.

> Logic Note: This is known as Modus Ponens. Given "If P implies Q" and "P is true", then "Q must be true".

Step 2: Analyzing the Symptoms (Elimination)
Now look at Premise B. "Respiratory symptoms" is a broad category. Typically, this means the patient has a Cough, a Fever, or Both.
Let's suppose for a moment that we rule out a cough (perhaps the patient's lungs sound clear). In that case, the "severe symptoms" must logically refer to the fever.
* Observation: In this specific case, the nurse confirms the patient does not have a dominant cough.
* Deduction: Therefore, the patient must have a fever.

Step 3: Synthesizing the Conclusion
We now combine our deductions:
1. The illness is bacterial (not viral).
2. The primary symptom is a fever.

Final Diagnosis Logic:
The patient is suffering from a bacterial fever. The prescription of antibiotics effectively ruled out a viral fever, guiding us to the correct classification of the illness.

Key Takeaway:
Medical reasoning often works backward from the treatment decision. By understanding why a doctor chooses a specific drug (antibiotics), we can logically deduce what conditions they have ruled out (viruses).
""",

"wiki":"""### Soil Nutrient Analysis in Farming Practices

Based on a logical analysis of agricultural methods, it is concluded that the soil is rich in nutrients. This derivation follows a sequence of inferences from documented farming events and logical rules.

#### Background
The following factual events are provided:
- The farmer uses organic fertilizers.
- The crop is planted in the spring.
- The crop yields a high harvest.
- The soil is rich in nutrients.
- The farmer rotates crops annually.
- The farmer uses a drip irrigation system.

#### Reasoning
- **Step 1**: Given that (a) crop rotation implies a high harvest, (b) either crop rotation occurs or drip irrigation is not used, and (c) if organic fertilizer use does not imply rich soil, then drip irrigation is used, it is deduced that either the harvest is high or organic fertilizer use implies rich soil.
- **Step 2**: From the previous deduction and the given that the harvest is not high, it follows that organic fertilizer use implies rich soil.
- **Step 3**: Given that spring planting implies organic fertilizer use and the fact that planting occurs in spring, it is deduced that organic fertilizers are used.
- **Step 4**: From the implication that organic fertilizer use implies rich soil and the fact that organic fertilizers are used, it is deduced that the soil is rich in nutrients.

#### Conclusion
Thus, the logical reasoning establishes that the soil is rich in nutrients.""",

"news":"""In a recent software development project, the team's strategic use of methodologies and tools played a pivotal role in navigating challenges and securing stakeholder approval. The initiative, which emphasized a clear project roadmap from the outset, seamlessly transitioned into adopting agile practices, fostering an environment of iterative progress and adaptability. This foundation, however, was tested when the final deliverable revealed inconsistencies in quality, ultimately impacting the timeline.

The linkage between deadline adherence and high-quality outcomes is well-established in software engineering. Here, the project's failure to meet quality standards pointed to missed deadlines, despite the team's agile framework. This disconnect raised questions about underlying factors, but the agile approach itself provided a crucial insight: such methodologies often act as a buffer, ensuring that projects remain viable even in the absence of key elements like version control or formal approval.

With deadlines not fully met, the logical progression pointed to the necessity of either robust version control or stakeholder endorsement. The team's consistent use of version control for code management—a practice that enhances collaboration and reduces errors—emerged as a stabilizing force. This, combined with the overarching project structure, paved the way for stakeholder approval, highlighting how integrated processes can offset setbacks and align with strategic goals.

Ultimately, the project's journey underscores the value of combining clear planning, agile execution, and reliable tools to achieve critical milestones. While quality and timing posed challenges, the cohesive approach demonstrated that even imperfect outcomes can gain endorsement when supported by transparent and methodical practices.""",

"maga":"""The hum of the server room was a constant, a low monastic chant for the digital age. Leo, the developer, sat back from his monitor, the final line of code committed. He was in that liminal space between building and release, a moment of quiet pride. His unit tests, a battalion of automated sentinels, had all returned a uniform green. All was well in the world he had built.

Yet, in the adjacent chamber of continuous integration, a different story unfolded. The build process, that meticulous assembler of fragments into a whole, had choked. A cascade of crimson failure messages pointed not to a logic flaw, but to a simple, almost childish syntax error—a missing semicolon, a stray bracket. It was a ghost from the machine, a reminder that completion is not always synonymous with correctness.

Anya, the project manager with a gaze that could calibrate a satellite, studied the report. The failure gave her pause, a logical knot to untangle. She knew two things with certainty: first, that a release had not been approved, and second, that if a developer had not finished coding, she would have no choice but to approve a release to meet the deadline. The inverse of this logic was inescapable. Since she had not granted approval, it could only mean that the developer was, in fact, done. Leo had truly completed the coding phase. This was the first anchor point, a foundational truth in the swirling digital fog.

This initial deduction led her to a second, more subtle connection. She considered the relationship between Leo’s completed code and the successful unit tests. The build failure was due to a syntax error, not a test failure. The system’s logic dictated that if the transition from completed code to passing tests was not a sure thing, then a build failure was inevitable. But the build had not failed for reasons of failed tests; it had failed on a technicality. Therefore, the link between completion and testing integrity had to be sound. The completed code did, logically and irrevocably, lead to passing tests. The unit tests were valid.

Now the pieces clicked into place with the satisfying finality of a magnetic lock. Leo had completed his work. And his completed work guaranteed functional, tested software. Therefore, the software had, beyond any doubt, passed all its unit tests. The syntax error was a superficial scar, not a deep wound.

The final step was one of confluence. Anya knew that reviewed and tested code is deployable code. The senior developer’s sign-off was already in the log, a digital seal of approval. And now, with the certainty of passing tests reaffirmed, the last barrier fell. The two prerequisites—tested code and reviewed code—were satisfied. The logical pathway to deployment was now clear and unobstructed.

Anya authorized the deployment. With a click, the software began its journey from the sterile staging environment to the vibrant, unpredictable world of production.

In the quiet that followed, Leo watched the deployment logs stream by. He reflected on the journey—not of the code, but of the reasoning that had carried it across the finish line. It was a testament to a deeper truth: that progress is often a dance between human intuition and irrefutable logic. The build had failed, yet that very failure became the catalyst for a chain of deductions that proved the software’s worth. It was a reminder that in the complex architecture of creation, sometimes you must first prove the foundation is solid before you can safely build upon it. The software was now live, not merely because it worked, but because they had proven, beyond all doubt, that it must.""",

"blog":"""Ever been in a situation where you’re trying to connect the dots, but the dots themselves seem scattered and unrelated? That’s often what navigating a complex health journey feels like—for both patients and their loved ones.

Today, I want to walk you through a story about a patient’s journey, not as a set of cold, clinical facts, but as a detective story where we piece together the clues. We’ll see how a series of events and test results can lead to a profoundly hopeful conclusion.

Let’s set the scene with what we know:
*   The patient is receiving chemotherapy.
*   They’re undergoing regular blood tests.
*   They have a history of their cancer coming back.
*   They’ve been prescribed a new medication.
*   And importantly, their immune system is currently functioning just fine.

Our big question, the one everyone is hoping to answer, is: Is the patient's cancer in remission?

Here’s how we can reason our way through it, step by step.

**Step 1: Reading Between the Lines of a Healthy Immune System**

We start with two key pieces of information. First, we know that if the patient did *not* have a history of recurrence, their immune system would be normal. But second, and this is crucial, we also know that their immune system is *not* currently normal.

Wait, that sounds like a contradiction, doesn't it? If their immune system isn't normal, then the condition for it being normal must be false. The condition was "no history of recurrence." So, if that condition isn't true, then its opposite must be. This leads us to our first solid clue: the patient must, in fact, have a history of cancer recurrence.

It’s a tough piece of the puzzle, but an important one to acknowledge upfront.

**Step 2: The Hidden Link Between History and Treatment**

Now we introduce another factor: a new medication. The logic here gets a little intricate, but stick with me. We know that if it were *not* true that a history of recurrence leads to chemotherapy, then a new medication would be prescribed. Think of it as a backup plan; if the standard protocol isn't in play, you bring in the reinforcements.

But here’s the thing—the patient is *not* taking a new medication.

So, if the "backup plan" isn't activated, it means the standard protocol must already be running. That allows us to connect the dots in a vital way: the patient's history of recurrence is directly linked to them receiving chemotherapy. It’s not a coincidence; it's the prescribed course of action.

**Step 3: Confirming the Course of Action**

This step is beautifully straightforward once we have the previous pieces. We've just established that a history of recurrence means the patient gets chemotherapy. And from our first step, we confirmed the patient has that exact history.

Put those two thoughts together, and it solidifies into a clear, undeniable fact: the patient is receiving chemotherapy. It’s the direct and logical response to their medical history.

**Step 4: The Final, Hopeful Leap**

Now we come to the final and most hopeful part of our reasoning. We have a well-established principle in this scenario: if a patient is receiving chemotherapy *and* undergoing regular blood tests, then the cancer will be in remission.

We’ve just firmly established that the patient is on chemotherapy. We also know from the very beginning that they are diligently getting their regular blood tests. They are doing everything they are supposed to be doing.

So, when you have both of those factors in place—the treatment and the monitoring—the outcome is almost a mathematical certainty. The logic leads us to one inescapable, wonderful conclusion.

**The Takeaway**

The patient's cancer is in remission.

Walking through this process shows us that even in the complex and often frightening world of medicine, there is a logical throughline. Each test, each treatment, and each piece of history is a clue. By putting them together carefully, we can move from fear and uncertainty to hope and clarity.

It’s a powerful reminder that behind every data point is a human story, and sometimes, the story has a happy ending.""",

"tech": """### Technical Analysis: Film Production Readiness and Logical Deductions

#### Background and Premise Events
The following events define the current state of the film production project:
- The film project is approved by the studio (denoted as Q0).
- The script has been finalized and reviewed (denoted as P1).
- The production team has secured all necessary permits (denoted as P2).
- The director has confirmed their availability (denoted as P3).
- The film is scheduled to start production (denoted as S0).

These premises establish the foundational facts for the logical analysis. The reasoning process will examine the logical relationships between these events to derive insights into the project's status, particularly in light of the observed fact that the film is not scheduled to start production (i.e., S0 is false). This analysis employs deductive reasoning to trace the implications through a series of logical steps.

#### Logical Deduction Process
The reasoning proceeds through a sequence of logical inferences, each building on the previous step to arrive at a conclusion. The steps are outlined below in natural language, avoiding symbolic notation for clarity.

**Step 1: Implication from Director Availability to Permit-Based Scheduling**  
Given that the director's availability (P3) implies that the securing of permits (P2) is a sufficient condition for the production to be scheduled (S0), and since the director has confirmed their availability (P3 is true), it follows that the securing of permits would lead to the production being scheduled. In other words, if permits are secured, then the production must be scheduled. This deduction is derived through the application of modus ponens, where the truth of the antecedent (P3) validates the consequent (P2 implies S0).

**Step 2: Contrapositive Inference from Scheduling Status to Permit Status**  
Given the previous deduction that securing permits implies the production is scheduled (P2 implies S0), and considering the observed fact that the production is not scheduled (S0 is false), it follows that the permits have not been secured (P2 is false). This step employs modus tollens, where the falsehood of the consequent (S0) necessitates the falsehood of the antecedent (P2). Thus, the absence of a scheduled production directly indicates that the necessary permits are lacking.

**Step 3: Implication from Script Finalization to Permit Securing**  
Given that the finalization and review of the script (P1) implies that the permits have been secured (P2), and since the permits have not been secured (P2 is false, as established in Step 2), it follows that the script has not been finalized and reviewed (P1 is false). This inference also uses modus tollens, where the falsehood of the consequent (P2) invalidates the antecedent (P1). Consequently, the lack of secured permits indicates a failure in script finalization.

**Step 4: Implication from Project Approval to Script Finalization**  
Given that the lack of project approval (not Q0) implies that the script has been finalized and reviewed (P1), and since the script has not been finalized (P1 is false, as established in Step 3), it follows that the project must be approved (Q0 is true). This step again applies modus tollens, where the falsehood of the consequent (P1) negates the antecedent (not Q0), thereby confirming the project's approval.

#### Conclusion
The logical analysis demonstrates that, based on the premise events and the observed absence of a production schedule, the project approval by the studio (Q0) is necessarily true. This conclusion is rigorously derived through a chain of deductive inferences, highlighting the dependencies between key project milestones. The reasoning confirms the consistency of the initial premises while providing a clear explanation for the project's status, underscoring the importance of script finalization and permit securing in the production timeline. This approach ensures a comprehensive understanding for experts involved in project management and decision-making processes.""",

"stor":"""Alex leaned back in his chair, staring at the computer screen where he had just logged the completion of his mandatory training module. He had also been assigned to the onboarding team, a move he hoped would advance his career. Yet, as he reflected, he knew his performance rating wasn't strong, and he hadn't been offered any leadership role. The question lingered in his mind: was he still eligible for a promotion? He decided to think it through systematically.

First, he considered the company's policy: if it weren't true that completing the training led to a strong performance rating, then he would have been given a leadership role. But since no leadership role had been assigned, he realized that completing the training must indeed imply a strong performance rating. This felt like a solid starting point—a link between his effort and expected outcomes.

Next, he recalled another guideline: being on the onboarding team meant that if he weren't eligible for a promotion, then he must have completed the training. Since he was definitely on the onboarding team, he concluded that if he weren't eligible, then he had completed the training. This seemed straightforward, but it tied his eligibility directly to his training completion.

Now, he pondered the first conclusion—that training completion should lead to a strong rating—against the reality that his rating was not strong. If that implication held true, but his rating was weak, then it must mean he hadn't actually completed the training. This gave him pause, as he knew he had finished the module, but he trusted the logical flow.

Finally, he connected the dots: if lack of eligibility required training completion, but he hadn't completed the training (based on his earlier deduction), then it must mean he was indeed eligible for a promotion. A sense of relief washed over him as he reached this conclusion, confident that the reasoning had led him to the truth.""",

"abst":"""This study employs a logical deduction framework to evaluate the accuracy of satellite data for environmental monitoring, based on established operational premises. The analysis begins by establishing that a stable orbit and properly functioning sensors imply that calibration for high-resolution imaging would lead to urban planning application. Given the satisfaction of these conditions, calibration necessitates such use. However, the data's lack of public accessibility, in conjunction with the logical disjunction indicating non-use in urban planning, leads to the conclusion that the images are not employed for this purpose. Consequently, the absence of urban planning application demonstrates that the satellite is not calibrated for high-resolution imaging. Since inaccuracy in environmental monitoring would require such calibration, its absence definitively confirms the data's accuracy for this application.""",

}

PROMPT_TEMPLATE_DICT = {
"wiki":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a well-written encyclopedic entry.

## Inputs:
* `[Premise Events]`: A list of background facts (brief, factual statements).
* `[Reasoning Skeleton]`: A step-by-step symbolic logic chain that yields a final conclusion.

## Instructions:
- Learn from the language style and expression in the examples, but create original content rather than copying the example's scenarios.
- Produce a neutral, third-person encyclopedic entry with formal yet flowing prose. Avoid bullet points or rigid structural markers.
- Present the background facts as coherent narrative context.
- Translate the reasoning steps into clear, logical prose that flows naturally.
- Maintain strict adherence to the logical sequence while using varied sentence structures.
- Ensure the output is compact and reads as a unified, fluent entry.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",


"news":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a compelling news article.

## Inputs:
* `[Premise Events]`: Key factual elements and developments.
* `[Reasoning Skeleton]`: Ordered logical steps that explain how the final conclusion follows.

## Instructions:
- Learn from the journalistic style in the examples while developing your own narrative approach.
- Develop the story through flowing paragraphs that integrate facts and logical progression.
- Translate the reasoning chain into accessible journalistic prose, using natural transitions.
- Include contextual elements that explain why the conclusion matters.
- Maintain accuracy and neutrality while crafting engaging, readable content.
- Use varied sentence structures and avoid rigid section headings.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",



"maga":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a rich magazine feature.

## Inputs:
* `[Premise Events]`: Background facts for setting and characters.
* `[Reasoning Skeleton]`: A stepwise logic chain to be followed in order.

## Instructions:
- Learn from the narrative techniques in the examples while creating original storytelling.
- Weave the logical steps throughout the narrative using descriptive language, character development, and evocative settings.
- Blend analytical insights seamlessly into the narrative flow.
- Create smooth transitions between different stages of reasoning.
- Develop emotional and intellectual depth while maintaining logical accuracy.
- Craft a reflective conclusion that highlights the significance of the final outcome.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",



"blog":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into an engaging blog post.

## Inputs:
* `[Premise Events]`: Short factual items to set context.
* `[Reasoning Skeleton]`: Ordered logical steps.

## Instructions:
- Learn from the conversational tone in the examples while developing your own voice.
- Use an accessible, personal tone suitable for blog readers (first or second person as appropriate).
- Walk through the reasoning process using natural language, personal reflections, and relatable examples.
- Connect logical steps with smooth transitions and engaging prose.
- Include practical insights or takeaways woven naturally into the narrative.
- Maintain conversational flow while preserving logical accuracy.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",


"tech":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into professional technical documentation.

## Inputs:
* `[Premise Events]`: Precise facts, metrics, system states, or observations.
* `[Reasoning Skeleton]`: A sequence of logical inferences leading to a conclusion.

## Instructions:
- Learn from the technical precision in the examples while developing clear explanations.
- Use precise, unambiguous technical language suitable for experts.
- Present background information in clear, organized prose.
- Explain the logical rationale through coherent technical exposition.
- Maintain rigorous analytical tone while ensuring readability.
- Use technical terminology appropriately while avoiding unnecessary jargon.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",


"stor":
"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a natural, flowing reasoning story.

## Inputs:
* `[Premise Events]`: A list of background facts.
* `[Reasoning Skeleton]`: A step-by-step symbolic logic chain.

## Instructions:
- Learn from the storytelling approaches in the examples while creating original narratives.
- Follow the logical sequence exactly while developing it into a coherent story.
- For each reasoning step, create natural narrative progression using dialogue, character thoughts, actions, or descriptive elements.
- Ensure smooth transitions between different stages of reasoning.
- Develop the story toward a clear conclusion that reflects the final logical outcome.
- Use varied sentence structures and natural language flow.
- Maintain creative expression while preserving logical accuracy.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
""",
# """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a natural, flowing conversational dialogue.

# ## Inputs:
# * `[Premise Events]`: Key facts about the scenario, participants, and context.
# * `[Reasoning Skeleton]`: A step-by-step logic chain to be followed.

# ## Instructions:
# - Learn from the conversational style and expressions in the examples, but create original dialogue scenarios.
# - Produce a dialogue that mimics real-human interaction, with natural turn-taking, emotional tones (e.g., friendly, frustrated), and contextual relevance.
# - Begin by setting the scene based on the premises, ensuring participants' roles and motivations are clear.
# - For each step in the `[Reasoning Skeleton]`:
#   - Translate the logical inference into dialogue elements (e.g., questions, responses, reactions).
#   - Use informal language, interruptions, or pauses as needed to enhance realism.
# - Ensure smooth transitions between dialogue turns and logical steps.
# - Maintain consistency in character voices and resolve the conversation based on the final conclusion.
# - Avoid rigid sectioning; output as a continuous dialogue with speaker labels (e.g., "User:", "Agent:").

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
# """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into an engaging social media post.

# ## Inputs:
# * `[Premise Events]`: Key elements, events, or cultural context.
# * `[Reasoning Skeleton]`: A stepwise logic chain to be followed.

# ## Instructions:
# - Learn from the informal, conversational style in the examples, while creating original content tailored to platforms like Twitter or Facebook.
# - Use casual, relatable language with emojis, hashtags, or slang if appropriate, but ensure clarity.
# - Begin with a hook that grabs attention, summarizing the core situation or conclusion.
# - Weave the logical steps into the narrative using brief, punchy statements or rhetorical questions.
# - Incorporate personal reflections or calls-to-action to enhance engagement.
# - Ensure the post feels organic and culturally relevant, with smooth transitions between ideas.
# - Avoid structured lists; output as a unified, short text (1–3 paragraphs).

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
# """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a piece of creative poetry.

# ## Inputs:
# * `[Premise Events]`: Imagery, emotions, or thematic seeds.
# * `[Reasoning Skeleton]`: A logical sequence to be interpreted artistically.

# ## Instructions:
# - Learn from the poetic devices and expressive language in the examples, but produce original verses.
# - Use literary techniques like metaphor, rhyme, or rhythm to evoke emotions and imagery.
# - Start by establishing a mood or scene inspired by the premises.
# - For each reasoning step, translate the inference into poetic lines that reflect the logic without explicit explanation.
# - Focus on emotional resonance and thematic depth, allowing ambiguity where appropriate.
# - Connect stanzas smoothly to build toward the final conclusion.
# - Output in free verse or structured form, without adherence to specific sections.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
"educ":
"""
# Role
You are a master educational content creator and logic tutor. Your specialty is transforming abstract logical proofs into engaging, narrative-driven educational articles, textbooks, or tutorials.

# Task
Your input consists of:
1.  `[Premise Events]`: A dictionary of real-world events mapped to logical symbols (e.g., P: "The alarm rings").
2.  `[Reasoning Skeleton]`: A sequence of logical steps using these symbols.

Your goal is to write a self-contained **educational document** that teaches the reader how to reach the conclusion based on the premises.

# Critical Instructions
1.  **Narrative Flow**: Don't just translate symbols. Weave a story. If the step is `P -> Q`, explain the *mechanism* of why P leads to Q in the real world.
2.  **Explicit Logic Teaching**:
    * Explain the logical rule being used (e.g., Modus Ponens, Disjunctive Syllogism) in natural language.
    * Use **Blockquotes (>)** or **Callout Boxes** to highlight abstract logical rules or "Pro Tips" separate from the main story.
3.  **Handling Premises**: You do not need to list all premises at the very beginning if it ruins the suspense. You can introduce them as the narrative unfolds (e.g., "Wait, we just received new data...").
4. **Format Diversity**: Strictly vary the structure for each output to ensure creativity. Choose a specific archetype such as **"Case Study"**, **"Detective's Notebook"**, **"Professor's Lecture"**, or **"Field Guide"** (or invent a similar high-quality format).

# Reference Style (For Tone Quality Only)
A good example is like this:
{examples_block}

# Input Data
[Premise Events]:
{premise_events}

[Reasoning Skeleton]:
{reasoning_skeleton}

# Output:

""",


"abst":"""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a concise, formal academic abstract.

## Inputs:
* `[Premise Events]`: Factual statements, data points, or research context.
* `[Reasoning Skeleton]`: Ordered logical steps leading to a conclusion.

## Instructions:
- Learn from the academic tone and structure in the examples, but develop original content.
- Use formal, precise language suitable for scholarly communication, with a focus on objectivity and clarity.
- Translate the reasoning steps into coherent academic prose, highlighting methods, findings, and implications without narrative flourishes.
- Emphasize logical flow through connective phrases (e.g., "Consequently," "Thus").
- Keep the output compact and avoid bullet points or explicit section headers.
- Do not include any symbols in the final context.

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
"""

}

# prompt_template_list = ["""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a concise, neutral, encyclopedic wiki-style entry.

# ## Inputs:
# * `[Premise Events]`: A list of background facts (brief, factual statements).
# * `[Reasoning Skeleton]`: A step-by-step symbolic logic chain that yields a final conclusion.

# ## Instructions:
# 1. Article Tone & Style: Produce a neutral, third-person encyclopedic entry suitable for a reference site. Avoid first-person, dramatic language, or speculative claims beyond the logic.
# 2. Structure:
#    * Lead paragraph: one or two sentences summarizing the situation and the final conclusion derived from the reasoning skeleton.
#    * Background section: present the `[Premise Events]` as factual context (concise bullet or short paragraphs).
#    * Reasoning section: translate each step of the `[Reasoning Skeleton]` into clear, formal prose. For each step:
#      - Restate the logical inference succinctly.
#      - Explain (briefly) how the premises lead to the inference without narrative embellishment.
# 3. References & Neutrality: If the logic mentions interventions or observations, present them as reported facts (e.g., “It was observed that…”). Do **not** invent external sources or dates.
# 4. Conclusion: End with a short concluding sentence that states the final derived claim.
# 5. Key Rule: Follow the `[Reasoning Skeleton]` in exact order and never contradict the provided logic. Keep overall length compact (roughly 120–300 words for a typical entry).

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
# """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a news article in the inverted-pyramid journalistic style.

# ## Inputs:
# * `[Premise Events]`: Key factual elements and developments.
# * `[Reasoning Skeleton]`: Ordered logical steps that explain how the final conclusion follows.

# ## Instructions:
# 1. Lead (lede): Begin with a strong first paragraph (1–2 sentences) that reports the most newsworthy fact — the final conclusion derived from the skeleton — and the essential who/what/when/where/why if present in the premises.
# 2. Important Details: Follow with 2–3 paragraphs that unpack the immediate supporting facts from `[Premise Events]`.
# 3. Logical Explanation: Then present a section that explains the logical chain. For each step in the `[Reasoning Skeleton]`:
#    * Translate the symbolic step into plain journalistic prose: state the inference, then provide the premise(s) that support it.
#    * If appropriate, include a short quote-style sentence (e.g., “Officials said…,” said Dr. X.) framed as a paraphrase of the reasoning—do not invent real names or organizations unless provided.
# 4. Context & Background: Add a short contextual paragraph situating why this conclusion matters.
# 5. Conclusion/Next Steps: Close with a paragraph on implications or what will happen next.
# 6. Key Rule: Maintain accuracy and neutrality; obey the logic order exactly and do not contradict any premises.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
# """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a magazine-style feature that blends narrative description, character/scene detail, and analytic explanation.

# ## Inputs:
# * `[Premise Events]`: Background facts for setting and characters.
# * `[Reasoning Skeleton]`: A stepwise logic chain to be followed in order.

# ## Instructions:
# 1. Opening Scene: Begin with an engaging hook or scene built from the `[Premise Events]` to draw the reader in.
# 2. Narrative + Reasoning: For each logic step in the `[Reasoning Skeleton]` (in exact order):
#    * Preface with a one-sentence, plain-language restatement of the inference (this restatement should be fully consistent with the skeleton).
#    * Then expand that step into 2–4 richly detailed paragraphs that make the logical move part of a narrative: include character thoughts, dialogue snippets, descriptive action, and evocative setting that illustrate why the inference is plausible.
#    * Interleave short analytic paragraphs that explicitly explain the logic behind the narrative moment—these analytic paragraphs should be clearly separable from the scene (e.g., “Why this matters:” or an italicized aside).
# 3. Flow & Pacing: Smoothly connect transitions between steps; ensure emotional and intellectual build toward the final conclusion.
# 4. Length & Tone: Aim for a readable, magazine voice—stylish but evidence-grounded. Length typically 600–1,200 words depending on complexity.
# 5. End with a reflective conclusion that states the final logical result and its broader significance.
# 6. Key Rule: Be creative in storytelling but never contradict or alter the logical chain.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# ""","""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a blog post with an accessible, reflective voice.

# ## Inputs:
# * `[Premise Events]`: Short factual items to set context.
# * `[Reasoning Skeleton]`: Ordered logical steps.

# ## Instructions:
# 1. Voice & Perspective: Use first or second person optionally (e.g., “I noticed…”, “You might see that…”) and a conversational tone suitable for a technical or personal blog.
# 2. Structure:
#    * Intro: Briefly summarize the situation and state the final conclusion in plain language.
#    * Walkthrough: For each step in the `[Reasoning Skeleton]`:
#      - Start by restating the logical step in simple terms.
#      - Then write 1–3 paragraphs with personal reflections, informal examples, and short anecdotes that make the logical step relatable.
#      - Optionally include a short “Tip” or “Takeaway” after each step that extracts the practical insight.
# 3. Practicalization: If the premises suggest actions or implications, add a short actionable section (“What to do next” or “When this applies”).
# 4. Closing: End with a concise personal takeaway and an invitation for reader comments or thought.
# 5. Key Rule: Preserve strict logical order and accuracy; do not invent contradictory facts.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# ""","""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a piece of technical documentation or engineering analysis (design rationale, incident report, or troubleshooting note).

# ## Inputs:
# * `[Premise Events]`: Precise facts, metrics, system states, or observations.
# * `[Reasoning Skeleton]`: A sequence of logical inferences leading to a conclusion.

# ## Instructions:
# 1. Audience & Tone: Use precise, unambiguous, technical prose aimed at engineers or domain experts. Use active voice and formal register.
# 2. Structure:
#    * Summary: One-paragraph executive summary that states the final conclusion and its impact.
#    * Preconditions / Observations: List the `[Premise Events]` as enumerated points (use bullet list).
#    * Logical Rationale: For each step in the `[Reasoning Skeleton]` (in order):
#      - Restate the inference in formal terms.
#      - Provide a short technical justification: data points, conditions required, and consequences.
#      - If applicable, include a small pseudo-table or numbered checklist of inputs → inference → validation steps.
# 3. Actionable Output: Provide recommended next steps, mitigations, or test cases derived from the final conclusion.
# 4. Formal Constraints: Use precise terminology, avoid narrative flourishes, and include short code/pseudocode snippets only if they help demonstrate the logic flow.
# 5. Key Rule: Stringently follow the provided skeleton; do not introduce unsupported assumptions.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# ""","""Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a book-style chapter or extended vignette that integrates detailed narrative and thematic depth.

# ## Inputs:
# * `[Premise Events]`: Character, setting, or factual seeds.
# * `[Reasoning Skeleton]`: Ordered logical steps to be dramatized.

# ## Instructions:
# 1. Chapter Format: Write an opening hook, 3–6 substantive sections (each tied to steps in the skeleton), and a closing section that states the final conclusion and thematic resonance.
# 2. For each step in the `[Reasoning Skeleton]` (in order):
#    * Begin the section with a short epigraph or line that captures the logical move.
#    * Develop a 2–4 paragraph scene that dramatizes the inference (dialogue, inner monologue, sensory detail).
#    * Follow with a 1-paragraph reflective passage that explicitly connects the scene to the logical inference—this serves as the chapter’s internal analysis.
# 3. Character & Arc: Ensure that actions and changes align with characters’ motivations implied by the `[Premise Events]`. Use the reasoning chain to drive a small emotional or intellectual arc through the chapter.
# 4. Style & Length: Prose may be literary; aim for 800–2,500 words depending on complexity. Keep consistency in tense and narrative voice.
# 5. Key Rule: Creativity is encouraged but never override or contradict the logical skeleton; every scene must support a step in the reasoning chain.

# A good example is like this:
# {examples_block}
# [Premise Events]:
# {entities}
# [Reasoning Skeleton]:
# {reasoning}
# ## Output:
# """,
# "Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into a detailed, natural-language reasoning story."
#         "##Inputs:"
#         " * [Premise Events]: A list of background facts."
#         " * [Reasoning Skeleton]: A step-by-step symbolic logic chain."
#         "##Instructions:"
#         "1.  Set the Scene: Start by using the `[Premise Events]` to create an engaging introduction to the setting and problem."
#         "2.  Follow the Skeleton: You must follow the `[Reasoning Skeleton]` in the exact order given."
#         "3.  Flesh Out Each Step: For each logic step in the skeleton:"
#         "    * First, state the reasoning in simple, natural language (Do not include this explanation in final output)."
#         "    * Then, **add details** to make it part of a story. Include dialogue, character thoughts, actions, or scene descriptions that lead to this logical conclusion."
#         "4.  Ensure Flow: Make the transitions between reasoning steps feel smooth and natural."
#         "5.  Conclude: End the story by stating the final conclusion from the skeleton."
#         "6.  Key Rule: Be detailed and creative, but do **not** contradict the provided logic."
#         #f"----example1----\n{example2}"
#         "A good examples is like this:\n{examples_block}\n"
#         "[Premise Events]:\n{entities}\n"  
#         "[Reasoning Skeleton]:\n{reasoning}\n"
#         "##Output:"] # wiki, 新闻，杂志故事（文章），博客，技术文档，书籍, 推理story

prompt_template1 = (
    """Your task is to convert a list of `[Premise Events]` and a `[Reasoning Skeleton]` into an educational tutorial.

## Inputs:
* `[Premise Events]`: Foundational concepts, steps, or examples.
* `[Reasoning Skeleton]`: A logical progression of ideas or procedures.

## Instructions:
- Learn from the instructive tone and clarity in the examples, while developing original educational material.
- Use clear, accessible language aimed at learners, with analogies or practical examples to illustrate points.
- Begin with an overview of the topic based on the premises.
- Explain each reasoning step in a step-by-step manner, using natural transitions (e.g., "Next," "As a result").
- Include actionable insights or tips to reinforce learning, but avoid rigid numbering or bullet lists.
- Conclude with a summary that highlights the key takeaway from the final conclusion.
- Ensure the output is self-contained and easy to follow (300–600 words).

A good example is like this:
{examples_block}
[Premise Events]:
{entities}
[Reasoning Skeleton]:
{reasoning}
## Output:
"""

)

def sample_format(format_list, weights=None):
    if not format_list:
        return ""
    return random.choices(format_list, weights=weights, k=1)[0]


prompt_template2 = ()
def prepare_data(data):
    res = []
    num = 0
    for d in data:
        try:
            # 检查必需的键是否存在
            if 'rules' not in d or 'options' not in d or 'num' not in d:
                print(f"跳过数据项 {num}: 缺少必需的键")
                continue
                
            item = d
            # 安全地构建context
            context_parts = []
            if 'rules' in item and isinstance(item['rules'], list):
                for i, s in enumerate(item['rules']):
                    if isinstance(s, dict) and 'explanation' in s:
                        context_parts.append(f'{i+1}. {s["explanation"]}')
                    else:
                        print(f"跳过数据项 {num}: 规则 {i} 格式不正确")
                        continue
            else:
                print(f"跳过数据项 {num}: rules 格式不正确")
                continue
                
            context = "\n".join(context_parts)
            
            # 安全地构建conclusions
            conclusions = []
            if 'options' in item and isinstance(item['options'], list):
                for i, o in enumerate(item['options']):
                    if isinstance(o, dict) and 'explanation' in o:
                        conclusions.append({
                            "conclusion": o['explanation'],
                            "num": i
                        })
                    else:
                        print(f"跳过数据项 {num}: 选项 {i} 格式不正确")
                        continue
            else:
                print(f"跳过数据项 {num}: options 格式不正确")
                continue
                
            res.append(
            {
                "num":d['num'],
                "entities":item['entities'],
                "reasoning_steps":item['reasoning_steps'], 
                "context":context,
                "conclusions":conclusions,
            })
            num += 1
            
        except KeyError as e:
            print(f"跳过数据项 {num}: KeyError - {e}")
            continue
        except Exception as e:
            print(f"跳过数据项 {num}: 其他错误 - {e}")
            continue
            
    return res

def generate_reasoning_prompt(data, seed=None):
    """Create one style-conditioned story prompt per prepared example."""

    if seed is not None:
        random.seed(seed)
    res = []
    for item in data:
        reasoning = item['reasoning_steps']
        entities = item['entities']
        output_format = sample_format(FORMAT_LIST, FORMAT_WEIGHTS)
        example = EXAMPLE_DICT[output_format]
        prompt_template = PROMPT_TEMPLATE_DICT[output_format]
        prompt = prompt_template.format(
            reasoning=reasoning,
            entities=entities,
            reasoning_skeleton=reasoning,
            premise_events=entities,
            examples_block=example
        )
        tmp = {
            "num":item['num'],
            "instruction":prompt,
            "format":output_format
        }
        res.append(tmp)
    return res
