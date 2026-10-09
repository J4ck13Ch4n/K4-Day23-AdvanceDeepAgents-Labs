# Survey about LLM Agents and Tool Use

## TL;DR
- Recent research highlights predominant LLM agent frameworks such as Agents, Transformers Agents, AutoGPT, Gentopia, XLang, Meta-GPT, Camel, and AgentVerse, all of which support tool use. Some frameworks, like LangChain, AgentVerse, and Agents, further offer support for memory and multi-agent features as well as symbolic operating procedures for fine-grained tool invocation [1].
- Recent advancements in enabling tool use include sophisticated API graph datasets, multimodal agent architectures, and reinforcement learning for tool selection and execution [2][3][4][5][6].
- Key challenges involve robust interpretation of tool sequences, seamless combination of API and GUI approaches, and adaptation to unfamiliar or multimodal tasks [2][7][8][9][6].
- Evaluation and benchmarking for tool-using LLM agents are maturing, with notable benchmarks like UltraTool, AgentBench, AgentAudit, FHIR-AgentBench, and frameworks such as DeepEval and Inspect focusing on planning, lifecycle coverage, and real-world performance [10][11][12][13][14][15][16].

## Background
LLM agents, distinct from traditional language model deployments, refer to autonomous or semi-autonomous systems powered by large language models and augmented with planning, reasoning, and explicit tool-usage capabilities. Early agent approaches emphasized simple prompt engineering or code generation, but the evolution towards architectural modularity and real-world adaptability has led to highly complex frameworks prioritizing robust, multi-turn, asynchronous interaction [17][1]. A central motivation is enabling models to conduct API calls, access tools, and manage dynamic, unpredictable workflows—a shift with implications for both deployment efficiency and application reach [18][17][1]. Contemporary research introduces multi-modal interaction, symbolic procedures, and advanced memory mechanisms as foundational to the effectiveness of modern LLM agents [17][1][3].

## Predominant Frameworks and Architectures for LLM Agents
The landscape of LLM agent frameworks is characterized by fast evolution and diversification, driven by both research and practical application demands. Prominent frameworks such as Agents, Transformers Agents, AutoGPT, Gentopia, XLang, Meta-GPT, Camel, and AgentVerse offer support for agentic planning and tool integration. These frameworks support tool usage and agent planning, and some (LangChain, AgentVerse, Agents) also provide memory and multi-agent features as well as symbolic operating procedures (SOPs), which enable fine-grained control of agent behavior and tool invocation within agent state cycles [1].
- **Support for Asynchronous and Multi-Modal Interaction:** As recent analysis notes, modern frameworks have shifted to supporting asynchronous interaction patterns, including real-time voice, video, and multi-modal contexts. These architectures generalize approaches from specialized systems (e.g., for robots or voice agents) to a unified agent format capable of handling a diversity of inputs and tool usage demands [17].
- **Performance and Latency Considerations:** As LLM agents move beyond single-turn tasks, new architectural considerations focus on how per-token latency and hardware selection impact sequential tool use. Enterprise-grade frameworks must accommodate compute-intensive trajectories, tool calls, and adaptive agentic cycles [18].

## Methods and Challenges in Enabling Tool Use
Recent progress in equipping LLM agents with tool capabilities encompasses multiple techniques and recurring hurdles:

- **Structured API and Dataset Representation:** API graph datasets enable agents to parse documentation into actionable graphs, allowing advanced API orchestration and execution of complex multi-step workflows. This structuring improves interpretability and facilitates tool selection, but accurately mapping raw documentation to effective agent action remains a challenge [2].
- **Paradigm Integration (API vs. GUI):** Studies highlight the convergence and divergence between agents using APIs and those operating via GUI (graphical user interface) manipulation. While API-based agents often offer reliability and scalability, GUI-based ones can flexibly adapt to unfamiliar or dynamic interfaces. Research explores approaches mixing both paradigms according to task requirements, but selecting the best automation path is non-trivial [7].
- **Multi-Modal and Vision-Language Capabilities:** The addition of multimodal encoders, as seen in frameworks like MLLM-Tool and OneSearch-VL, allows LLM agents to process instructions containing text, images, or video, and choose optimal tools for each context. Techniques such as tuning with synthetic multimodal data and composing visually-grounded evidence graphs enhance real-world agent effectiveness, though reliably encoding spatial and state-action correspondences remains complex [3][4][9][6].
- **Learning and Adaptation:** Benchmarks like Learn2Play (for unfamiliar environments) and reinforcement learning approaches (MiMo-V2.6, ViSkill) push agents toward enhanced self-improvement and the efficient acquisition of new skills. Learn2Play specifically targets agents' ability to learn from experience rather than rely solely on prior (pretraining) knowledge—an area where current benchmarks are still evolving [8][5][6].

## Applications and Evaluation Benchmarks for LLM Agents Leveraging Tool Use
Tool-using LLM agents are rapidly being integrated into practical domains requiring complex planning, reliability, and high-performance task completion. Representative applications span:

- **Complex, Multi-step Task Planning:** Frameworks like UltraTool evaluate LLM agents on their ability to not only select and invoke tools but to plan intricate multi-step operations and adapt to complex, real-world scenarios. Unlike previous benchmarks focused solely on tool invocation, UltraTool independently assesses agents' planning phases and tool application, reflecting realistic automation challenges [11].
- **Healthcare and Specialized Benchmarks:** FHIR-AgentBench is a benchmark for tool-calling agents in healthcare, focusing on multi-step reasoning across electronic health records graphs and robust agent abilities for clinical queries [13]. Agents are also evaluated in unfamiliar, dynamic, or safety-critical domains requiring advanced multi-modal and adaptive tool capabilities.
- **Lifecycle and Trust Evaluation:** The AgentAudit framework introduces a full-lifecycle perspective, measuring agent reliability, memory, planning, tool selection, invocation, and execution faithfulness across ten qualitative and quantitative dimensions. This comprehensive approach integrates prior benchmarks but aims to highlight failures and trust-relevant events across the agent’s entire operational span [12].
- **Hierarchical and Capability-Aligned Tasks:** Hierarchical learning frameworks and benchmarks focus on both global planning and precise tool execution. Misalignment between planners and executors within agent architectures is identified as a significant challenge, underscoring the need for benchmarks that can distinguish failure sources in complex tool-augmented agents [14].
- **Evaluation Frameworks:** Frameworks like DeepEval provide evaluation metrics including task completion, tool correctness, goal accuracy, step efficiency, and plan adherence, enabling granular unit tests and analysis of agentic tool use. Inspect offers over 200 evaluation types focusing on tool-use scenarios, safety, and robustness [15][16].

## Trends and Open Problems
The LLM agent and tool-use ecosystem is progressing rapidly but faces persistent challenges and open questions:

- **Benchmark Realism and Scale:** Many current benchmarks (especially in research) are starting to better reflect real-world challenge diversity, but issues remain with coverage and fidelity for broader deployment environments [8][11][13].
- **Dealing with Unfamiliarity and Adaptation:** True open-ended agent evaluation—especially with novel or unseen APIs, domains, or interfaces—remains limited. Benchmarks like Learn2Play provide valuable insights, but methods for robust generalization are still in their infancy [8].
- **Integration of Multi-modal and Symbolic Reasoning:** Effective fusion of vision, language, structured data, and symbolic planning tools is ongoing. While some multimodal agents (MLLM-Tool, OneSearch-VL, ViSkill) demonstrate progress, scaling reliably remains hard [3][9][6].
- **Tool Control, Security, and Alignment:** Frameworks like AgentAudit and hierarchical capability learning point to the need for finer alignment between agent planning, tool invocation, and feedback cycles—especially for tasks where correctness and safety are paramount [12][14].
- **Performance Efficiency and Infrastructure:** Enterprises face the challenge of engineering for latency, hardware efficiency, and real-time operation as agent capabilities grow. Adapting both software and underlying infrastructure (frameworks, hardware, scheduling) is becoming a decisive factor in agent effectiveness [18][17].

Ongoing improvements, new open-source releases, and partnerships between academia and industry are expected to push LLM agents closer to safely and reliably handling the open-world tasks they are designed for—even as state-of-the-art benchmarks and frameworks continue to redefine the landscape.

## References
[1] Agents: An Open-source Framework for Autonomous Language Agents. web. https://arxiv.org/abs/2309.07870 (n.d.)
[2] In-N-Out: A Parameter-Level API Graph Dataset for Tool Agents. hf-search. https://huggingface.co/papers/2509.01560 (2025-12-30)
[3] MLLM-Tool: A Multimodal Large Language Model For Tool Agent Learning. hf-search. https://huggingface.co/papers/2401.10727 (2024-01-19)
[4] Multi-modal Agent Tuning: Building a VLM-Driven Agent for Efficient Tool Usage. hf-search. https://huggingface.co/papers/2412.15606 (2024-12-20)
[5] MiMo-V2.6: Scaling Reinforcement Learning Towards Self-Improvement. hf-daily. https://huggingface.co/papers/2610.11959 (2026-10-08)
[6] ViSkill: Reinforcing VLM Agents with Evolving Visual-Native Skills. hf-daily. https://huggingface.co/papers/2610.12403 (2026-10-08)
[7] API Agents vs. GUI Agents: Divergence and Convergence. hf-search. https://huggingface.co/papers/2503.11069 (2025-03-14)
[8] Learn2Play Bench: How Well Do LLM Agents Learn from Experience in Unfamiliar Environments?. hf-daily. https://huggingface.co/papers/2610.08215 (2026-10-08)
[9] OneSearch-VL: Unified Multimodal Deep Research Agent for Image and Video. hf-daily. https://huggingface.co/papers/2610.12421 (2026-10-08)
[10] Evaluation and Benchmarking of LLM Agents: A Survey. web. https://dl.acm.org/doi/10.1145/3711896.3736570 (2025-08-03)
[11] UltraTool: Benchmarking LLMs for Comprehensive Tool Utilization in Real-World Complex Scenarios. web. https://aclanthology.org/2024.findings-acl.259.pdf (2024-08-11)
[12] AgentAudit: An Open, Extensible Framework for Full-Lifecycle Trust Evaluation of AI Agents. arxiv. https://arxiv.org/abs/2609.09875 (2026-09-09)
[13] Reinforcement Learning for Tool-Calling Agents in Fast Healthcare Interoperability Resources (FHIR). arxiv. https://arxiv.org/abs/2605.14126 (2026-05-13)
[14] Capability-Aligned Hierarchical Learning for Tool-Augmented LLMs. arxiv. https://arxiv.org/abs/2606.09371 (2026-06-08)
[15] DeepEval: The LLM Evaluation Framework. web. https://github.com/confident-ai/deepeval (n.d.)
[16] Inspect: A Framework for Large Language Model Evaluations. web. https://github.com/UKGovernmentBEIS/inspect_ai (n.d.)
[17] LLMs are General Asynchronous Agents. arxiv. https://arxiv.org/abs/2609.35427 (2026-09-28)
[18] Evaluating Inference Compute for Generative AI: A Framework for Enterprise Workloads. arxiv. https://arxiv.org/abs/2610.07094 (2026-10-05)
