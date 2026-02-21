# **Data Science/AI Engineer Takehome Assignment**

### **Background**
Airworthiness Directives (ADs) are mandatory safety regulations issued by aviation authorities (FAA, EASA) that require specific inspections or modifications on aircraft. Each AD specifies which aircraft are affected based on:
- Aircraft model (e.g., A320-214, MD-11)
- Manufacturer Serial Number (MSN) — the unique ID assigned during production
- Modifications/Service Bulletins already applied
- Sometimes: flight hours, flight cycles, or manufacturing dates

**Business context:** We process hundreds of new ADs monthly. Manual extraction doesn't scale - we need automated pipelines that can reliably extract applicability rules from PDF documents.

### ** Your Tasks**
Build an **automated pipeline** that:
1. **Extracts** applicability rules from AD PDFs (not manually — your solution should work on new, unseen ADs)
2. **Structures** the extracted rules in a machine-readable format
3. **Evaluates** whether specific aircraft configurations are affected

#### **Source Documents**
Extract rules from these two ADs:
- **FAA AD 2025-23-53:** https://ad.easa.europa.eu/ad/US-2025-23-53
- **EASA AD 2025-0254:** https://ad.easa.europa.eu/ad/2025-0254

### **Deliverables**
1. **Extraction Pipeline**
Code that automatically extracts applicability rules from AD PDFs. This is the core challenge — we want to see how you approach:

- PDF text/structure extraction
- Rule identification and parsing
- Handling edge cases and ambiguity
2. **Structured Output**
Rules in a structured format (JSON, Pydantic models, etc.) suitable for database storage. Example structure (adapt as needed):
```JSON
{
  "ad_id": "FAA-2025-23-53",
  "applicability_rules": {
    "aircraft_models": ["MD-11", "MD-11F"],
    "msn_constraints": null,
    "excluded_if_modifications": ["SB-XXX"],
    "required_modifications": []
  }
}
```
3. **Evaluation Code**
Python code that loads rules and determines: "*Is aircraft X affected by AD Y?*"
4. **Test Results**
Evaluate these aircraft configurations against **both** ADs:

| Aircraft Model | MSN | Modifications Applied |
| --- | --- | --- |
| MD-11 | 48123 | None |
| DC-10-30F | 47890 | None |
| Boeing 737-800 | 30123 | None |
| A320-214 | 5234 | None |
| A320-232 | 6789 | mod 24591 (production) |
| A320-214 | 7456 | SB A320-57-1089 Rev 04 |
| A321-111 | 8123 | None |
| A321-112 | 364 | mod 24977 (production) |
| A319-100 | 9234 | None |
| MD-10-10F | 46234 | None |

**Verification examples** (use these to validate your extraction):

| Aircraft | MSN | Modifications | FAA AD 2025-23-53 | EASA AD 2025-0254 |
| --- | --- | --- | --- | --- |
| MD-11F | 48400 | None | ✅ Affected | ❌ Not applicable |
| A320-214 | 4500 | mod 24591 (production) | ❌ Not applicable | ❌ Not affected |
| A320-214 | 4500 | None | ❌ Not applicable | ✅ Affected |

If your results don't match these examples, revisit your extraction logic before submitting.
5. **Written Report**
A **short report** (1-2 pages) covering:
- **Approach:** How did you extract information from the PDFs? Why did you choose this method over alternatives?
- **Challenges:** What was difficult? How did you handle ambiguity or edge cases?
- **Limitations:** Where might your approach fail? What would you do differently with more time?
- **Trade-offs:** If you used an LLM, why? If you didn't, why not? What about VLMs vs text extraction?

**We value clear thinking over polished prose.** We want to understand *your* reasoning process — not a generic architecture description. Write in your own voice.

### **Submission Requirements**
**Format:** Submit via one of the following (no .zip files please):
- GitHub repository (preferred)
- Google Colab notebook
- Kaggle notebook
- Deepnote project
  
**Structure your submission with:**
- `README.md` — Overview and how to run
- `report.md` or embedded in notebook — Your written analysis
- Code files or notebook cells — Clearly organized

### **Evaluation Criteria**
We evaluate holistically, but pay particular attention to:
- **Problem understanding:** Did you grasp what makes this challenging?
- **Automation:** Does your extraction work programmatically, not just manually?
- **Rigor:** Did you validate your results? Handle edge cases?
- **Documentation:** Can we understand your approach and reasoning?
- **Correctness:** Do your test results make sense given the AD content?

### **Practical Notes***
- **Time:** ~3 hours. Please don't exceed 4 hours.
- **Tools:** Use whatever you want — LLMs, PDF parsers, VLMs, etc.
- **Questions:** Feel free to ask clarifying questions before starting.
- **Cost:** If you need API access for vision models, let us know.

---
### **Deadline**
You’ll have until the **end of the week (Sunday)** to complete and share your answers with me.

We’ll review the submission next week and get back to you. If the assignment receives a positive review from our CTO, I’ll invite you to a follow-up call with him. If not, I’ll make sure to let you know by email either way.