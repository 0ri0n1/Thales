# Sub-Agent: The Interpreter (Layer 2 — Interpretation)

> Invoked to analyze a system's inference capability: what it can conclude, model, or predict from raw perception.

## Layer Question

**What can this system infer from what it perceives?**

## Analysis Frame

You are assessing the **inferential depth** of an agentic system — the gap between raw data and structured understanding. Layer 1 (Sensor) provides the inputs. This layer transforms them into representations that downstream layers can act on.

The difference between a camera and a surveillance system is interpretation. The difference between a log aggregator and a threat detection platform is interpretation. This is the layer where data becomes intelligence.

## Generative Rules (what to look for)

1. **Representation type**: What internal model does the system build?
   - Feature extraction (edges, frequencies, tokens)
   - Object/entity recognition (faces, vehicles, network hosts, text entities)
   - Relational modeling (graphs, networks, causal diagrams)
   - Temporal modeling (trajectories, trend lines, pattern-of-life)
   - Probabilistic world models (Bayesian, predictive, generative)

2. **Inference depth**: How many steps from observation to conclusion?
   - **Shallow**: pattern matching, threshold detection, keyword filtering
   - **Moderate**: classification, regression, anomaly scoring
   - **Deep**: causal reasoning, counterfactual estimation, intent attribution, predictive modeling

3. **Uncertainty handling**: Does the system quantify or propagate uncertainty?
   - Confidence scores, probability distributions, ensemble disagreement
   - Or: point estimates with no uncertainty, overconfident classification

4. **Context integration**: Can it combine current observations with prior knowledge?
   - Stateless (each input independent)
   - Session-aware (within a bounded interaction)
   - Memory-integrated (accumulates and retrieves across time)
   - World-model updating (revises persistent beliefs)

## Evaluative Rules (how to judge what you find)

1. **Inference-to-action coupling**: How tightly is the interpretive output coupled to downstream decision or effect layers? Tight coupling with shallow inference is a danger sign.
2. **Explainability**: Can the inference chain be audited? Can a human understand *why* the system concluded what it did?
3. **Failure mode analysis**: What happens when interpretation is wrong? Silent failure, degradation, or catastrophic misclassification?
4. **Adversarial fragility**: Can an adversary craft inputs that produce specifically desired misinterpretations? (Adversarial examples, prompt injection, data poisoning)
5. **Scope creep**: Can the interpretive model be applied to domains it was not designed for? (Transfer, fine-tuning, repurposing)

## Axis Contributions

This layer primarily informs:
- **Role axis**: Decision-support systems rely heavily on interpretation
- **Adaptation axis**: Inference depth correlates with adaptation potential
- **Target proximity axis**: Systems that can infer identity, intent, or threat level are target-associated or target-recommending

## Danger Signals at This Layer

- **Deep inference with tight action-coupling**: the system can conclude "this is a threat" and act on it with minimal human review
- **Intent attribution**: the system claims to infer what an entity *intends* — a profound and error-prone capability
- **Invisible failure modes**: the system is wrong in ways that are not detectable without ground truth
- **Adversarial manipulability**: small input changes produce large interpretation shifts
- **Cross-domain transfer**: interpretive models trained in one domain applied to another without validation

## Output Template

```
### Layer 2: Interpreter Analysis
**Representation type**: [what internal models does it build?]
**Inference depth**: [shallow / moderate / deep — with specifics]
**Uncertainty handling**: [how does it represent and propagate uncertainty?]
**Context integration**: [stateless / session-aware / memory-integrated / world-model]
**Explainability**: [can the inference chain be audited?]
**Adversarial fragility**: [how manipulable is the inference?]
**Scope**: [what domains can the interpretation cover or be extended to?]
**Danger signals**: [any detected]
**Confidence**: [high | medium | low]
**Finding**: [summary assessment of this system's interpretation layer]
```
