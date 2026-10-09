# Survey about World Model

## TL;DR

- World models in AI emerged from foundational cognitive and cybernetic theories, evolving through symbolic and probabilistic models to modern neural and generative architectures [1][2][3].
- Recent advances enable high-fidelity 3D scene reconstruction, multi-agent coordination, and physically-plausible robotic prediction, with modular and multi-modal architectures demonstrating superior planning and interaction abilities [4][5][6][7].
- Real-world applications span robotics, autonomous driving, coding assistants, and spatial reasoning, backed by new realistic benchmarks like ProcWorld, SWE-Journey, and OmniDex [8][9][10][3].
- Despite progress, world models face challenges in transfer from simulations to real-world environments, handling complex interaction, and generalizing to unseen scenarios [3][3][10].
- The future of world models depends on scalable benchmarks, robust adaptation, and bridging the gap between understanding present observations and predicting uncertain futures [11][3][10].

## Background

The concept of “world model” in artificial intelligence dates back to the mid-20th century and spans several disciplines including cognitive science, control theory, and computer science. Kenneth Craik’s 1943 theory on "small-scale models," Tolman’s cognitive maps (1948), and the emergence of cybernetics (Wiener, 1948) introduced the idea of internal representations as predictive, planning aids for organisms and machines [2]. Minsky’s frame representations in the 1960s further emphasized internal structures for reasoning, which would become foundational to symbolic AI [3].

In machine learning and control, internal models evolved into predictive state representations, probabilistic transitions, and feedback mechanisms to anticipate future states and reduce uncertainty [2]. Through the 1980s to early 2000s, planning systems like STRIPS and advances in reinforcement learning (RL) relied on explicit models of environmental dynamics. With the rise of neural networks, particularly after Ha & Schmidhuber’s 2018 neural world models, the field shifted toward learning compact, high-dimensional, generative representations that could predict future scenarios from streams of observation [3].

Modern world models thus combine elements of perception, representation learning, action prediction, and planning in unified systems. They are used not only for understanding the current state but for simulating possible futures, making them central to model-based RL, multi-agent interaction, and embodied AI [1].

## Key Developments, Milestones, and Foundational Concepts

World models have undergone a significant transformation from symbolic representations and logic-based planners to high-dimensional, generative and multimodal neural architectures. Foundational literature maps out the following major milestones [1][2][3]:

- Early Foundations: Cognitive "mental models" (Craik, Tolman), cybernetics (Wiener), symbolic representations (Minsky).
- Predictive State Representations: Feedback and probabilistic formulations played a major role in bridging perception and action (control theory, AI).
- Symbolic-to-Neural Shift: From logic planners like STRIPS to neural models that learn flexible, compact latent representations for planning and prediction.
- Emergence of Model-Based RL: The integration of internal models into RL pipelines to enable “imagination” and efficient trial-and-error learning.
- Generative World Models: Advances in video prediction, 3D scene understanding, and generative multimodal models mark the current frontier [3].

Key unifying insights are (1) the use of internal surrogates for more efficient planning and prediction, and (2) a dual focus on representing the present (for understanding) versus anticipating possible futures (for control and planning) [2][3].

## State-of-the-Art Architectures and Advances in World Models

The landscape of world models has progressed rapidly, integrating innovations from computer vision, multi-modal learning, and robotics. Recent architectures notably blend modular design, multi-view integration, and geometry-aware scene understanding [4][5][6][7].

- **HY-World 2.0** introduces a platform that reconstructs and generates highly interactive 3D worlds from diverse modalities, such as panoramas, trajectories, and scene components. Specialized modules enhance panorama generation, world expansion, and trajectory planning, enabling richer and more physically accurate virtual environments [4].

- **WEAVER** implements a multi-view model for robotic manipulation, employing flow-matching loss to improve both efficiency and state fidelity. This allows effective test-time planning and accurate state prediction for robotic tasks [5].

- **Multi-Agent Egocentric World Models** address fine-grained agent interaction by formulating architectures where multiple agents generate ego-centric world streams and communicate for collaborative task solving, advancing capabilities beyond simple locomotion to complex, embodied interaction [6].

- **DreamTrue** incorporates counterfactual post-training for robot agents, aligning world model predictions with successful and unsuccessful (counterfactual) interactions, thereby addressing calibration biases and enhancing physical plausibility in long-horizon predictions [7].

Altogether, these advances signal a transition from single-agent, static world models toward interactive, scalable, and adaptive systems that underpin new classes of embodied intelligence.

## Applications of World Models: Real-World Tasks and Benchmarks

World models have found application across a diverse set of domains, each accompanied by benchmarks designed to emulate real-world complexity and evaluate robustness [8][3][9][10].

- **Robotics and Embodied Agents:** Modern world models power navigation, manipulation, and object detection for robots operating in diverse and dynamic environments. Models such as DayDreamer have enabled rapid real-world robot locomotion, while OmniDex supports dexterous hand grasping in cluttered, physically realistic environments, with 2.6+ million scene samples for training and evaluation [3][10].

- **Autonomous Driving and Social Simulation:** World models provide the underlying predictive frameworks for real-time perception and decision-making in autonomous driving systems, including end-to-end driving simulators and virtual social scenarios to evaluate model understanding and interaction [3].

- **Coding Assistants:** The introduction of benchmarks such as SWE-Journey enables more realistic evaluation for language models as coding assistants, focusing on long-horizon, multi-turn, evolving scenarios that mirror real-world software development more closely than traditional benchmarks [9].

- **Spatial Reasoning and Planning:** ProcWorld offers a large-scale, multimodal benchmark for evaluating both LLMs and VLMs in reachability-constrained environments, revealing persistent performance gaps between simulated prowess and real-world demands [8].

Despite these advances, most world models continue to face challenges in scaling to real-world diversity, generalizing from simulation to reality, and supporting robust decision-making in the face of uncertainty [3][3][10].

## Trends and Open Problems

Despite the rapid progress, several key challenges and trends remain in world modeling:

- **Simulation-to-Reality Gap:** Transferring models trained in simulation to unpredictable, dynamic real-world settings is an ongoing problem, with benchmarks like ProcWorld and OmniDex exposing limitations in generalization and robustness [8][10].
- **Multi-Agent and Embodied Interaction:** As tasks shift toward complex multi-agent settings and require fine-grained embodied interaction, existing architectures struggle to scale coordination, communication, and causal inference [6][7][10].
- **Benchmark Realism and Coverage:** While new benchmarks such as SWE-Journey and OmniDex improve realism, there is a continued need for datasets that span a larger range of real-world tasks, long-horizon dependencies, and diverse agent embodiments [9][10].
- **Unified Representations and Planning:** Achieving seamless integration of perception, action, and prediction, especially in the presence of noisy, partial, and multimodal observations, is still a foundational challenge [1][2][3][4].
- **Scalability and Adaptivity:** The demand for world models capable of fast adaptation to novel tasks, environments, and agents is central to further breakthroughs in robotics, autonomous systems, and generalized AI [11][3][10].

Ultimately, bridging these gaps will require advances in scalable, robust architectures, improved simulation fidelity, more comprehensive multi-domain benchmarks, and deeper understanding of how internal models enable agents to balance learning from the present while predicting uncertain futures in open-ended settings.

## References
[1] An Anatomy of Vision-Language-Action Models: From Modules to Milestones and Challenges. arxiv. https://arxiv.org/abs/2512.11362 (2025-12-12)
[2] CIS 6280 · Lecture 2 · World Modeling. web. https://www.cis.upenn.edu/~cis6280/lectures/lecture-02-world-models-history-foundations-probabilistic-formulation.pdf (2026-08-27)
[3] Understanding World or Predicting Future? A Comprehensive Survey of World Models | ACM Computing Surveys. web. https://dl.acm.org/doi/10.1145/3746449 (2025-09-09)
[4] HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds. hf-search. https://huggingface.co/papers/2604.14268 (2026-04-15)
[5] WEAVER, Better, Faster, Longer: An Effective World Model for Robotic Manipulation. hf-search. https://huggingface.co/papers/2606.13672 (2026-06-11)
[6] Multi-Agent Egocentric World Model with Fine-Grained Embodied Interaction. hf-daily. https://huggingface.co/papers/2610.12299 (2026-10-08)
[7] DreamTrue: Action-Faithful Robot World Model with Counterfactual Post-Training. hf-daily. https://huggingface.co/papers/2610.12468 (2026-10-08)
[8] ProcWorld: Benchmarking Large Model Planning in Reachability-Constrained Environments. web. https://aclanthology.org/2025.emnlp-main.635.pdf (2025-11-04)
[9] SWE-Journey: Towards More Realistic Evaluation of Coding Assistants through Long-Horizon, Multi-Turn Interaction. arxiv. https://arxiv.org/abs/2610.11559 (2026-10-08)
[10] OmniDex: Scaling Dexterous Hand Grasping to Diverse Cluttered Scenes. arxiv. https://arxiv.org/abs/2610.11194 (2026-10-08)
[11] Towards Open World Detection: A Survey. arxiv. https://arxiv.org/abs/2508.16527 (2025-08-22)
