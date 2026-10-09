# Survey about Video and Multimodal Generation

## TL;DR
- Video and multimodal generation research builds on evolving foundational models including GANs, diffusion models, and auto-regressive approaches, with diffusion methods dominating recent advancements [1][2].
- Recent multimodal generation advances pivot on agent-native frameworks, dual-path architectures, and latency-reduction techniques for scalable and high-fidelity content synthesis [3][4][5][6][7].
- Benchmarks like VBench have standardized evaluation for generative models, targeting alignment with human perception and multi-dimensional coverage of quality and semantic attributes [8].
- Specialized benchmarks and action-centric modular approaches are advancing domain-specific evaluation, with emphasis on accurate evidence integration and controlled comparative assessments [9][10].
- Major challenges across video and multimodal generation include computational efficiency, robust semantics, and scalable benchmarks that address temporal, spatial, and cross-modality consistency [1][9][10].

## Background
The field of generative modeling has seen substantial progress, especially with the introduction of foundational paradigms for video generation. Early approaches leveraging Generative Adversarial Networks (GANs) such as StyleGAN-V and MoCoGAN provided initial breakthroughs in video realism, but instability and limited mode coverage prompted the rapid adoption of diffusion models (e.g., SVD, VideoCrafter2) [1]. Diffusion models, with their stable log-likelihood training and evidence lower bound maximization, have since become the dominant approach for both image and video generation [1][2]. Auto-regressive models, particularly those combining VQ-VAE tokenization and transformers, offer scalable generation and have recently enabled exact likelihood estimation for high-resolution video, drawing parallels to the success of large language models [1].

Multimodal generation extends the scope to synthesis and analysis across video, image, text, and audio domains. Unified models like MM-DiT and FullDiT facilitate joint processing of modalities, enabling more complex and high-fidelity outputs. Specialist foundation models, such as nnFoundation for radiological imaging, underscore the increasing significance of scalable architectures that transfer across domains [2]. These developments have been driven in part by new agent-native frameworks and evaluation benchmarks that guide systematic progress and comparative assessment.

## Foundation Models and Approaches for Video Generation
Recent developments in video generation center on three main paradigms: GANs, diffusion models, and auto-regressive (AR) models [1]. GANs initially achieved realistic frame and sequence synthesis in models such as StyleGAN-V and MoCoGAN, but their limitations led to the exploration of diffusion-based architectures, which maximize log-likelihood and achieve greater mode coverage. Diffusion models like SVD, VideoCrafter2, and Diff-Transformers demonstrate robust training and improved quality, albeit with computationally intensive inference [1].

Auto-regressive models represent another core paradigm, especially those leveraging a two-stage framework—first, VQ-VAE compresses frames into tokens, followed by a transformer-AR architecture that generates sequences, closely mirroring natural language modeling techniques. This approach allows for scalable, high-resolution generation with exact likelihood estimation, a milestone for practical and reliable synthesis [1].

Unified multimodal models—MM-DiT, FullDiT, CogVideoX, and HunyuanVideo—further expand the generative landscape. These architectures process both text and video tokens together, advancing high-fidelity scene generation and complex content creation [1]. In specialized domains, 3D foundation models such as nnFoundation are designed for volumetric video generation, particularly in medical imaging, leveraging convolutional and transformer-based designs trained on millions of radiological images. They address generalization and robustness, emphasizing domain transferability and scalable foundational architectures [2].

## Advances and Trends in Multimodal Generation
The multimodal generation field has progressed rapidly, enabled by agent-native frameworks that optimize structured multi-agent tasks, persistent memory, and domain-specific skill integration. GEMS exemplifies this direction, offering improved context handling and structured optimization for multimodal synthesis and downstream tasks [3].

OmniGen2 introduces dual decoding pathways for text and images, supporting subject-driven multimodal generation while maintaining competitive benchmark performance and preserving text generative capabilities [4]. DuoGen combines multimodal data in a decoupled two-stage architecture, blending pretrained multimodal LLMs with diffusion transformers, achieving enhanced text-image alignment and general purpose interleaved output [5].

Unified research agents, such as OneSearch-VL, employ visually grounded evidence graphs to facilitate visual grounding, external retrieval, and task-level references for multimodal research tasks [6].

Efficiency optimizations are a current focus, with MC-Sparse reducing latency in diffusion transformers for long-sequence generation using Meta-Cached Sparse Attention, which mitigates performance degradation associated with sparse token grouping and selection [7].

## Benchmarks and Challenges for Video and Multimodal Generation
Comprehensive benchmarks like VBench have pioneered hierarchical and multi-dimensional evaluation for video generative models, decomposing quality into dimensions such as subject/background consistency, temporal flickering, motion smoothness, dynamic degree, and frame-wise qualities like aesthetics and imaging quality. VBench evaluates performance using tailored prompts and objective pipelines for each dimension, including human preference annotation, as well as semantic and style consistency with prompts, object class detection, human action evaluation, spatial relationships, and style similarity. Existing metrics such as IS, FID, FVD, and CLIPSIM frequently do not align with human judgment and can miss artifacts unique to generative video models, thus new benchmarks like VBench are crucial for better alignment with human perception [8].

LMMs-Eval is a standardized suite for evaluating large multimodal models, covering over 50 tasks with more than 10 models. It confronts an 'Evaluation Trilemma': wide coverage, low cost, and zero contamination are difficult to achieve simultaneously. Solutions such as LMMS-EVAL Lite allow for efficient evaluation, and LiveBench provides dynamic, zero-shot evaluation on current data to avoid contamination. Challenges persist, including lack of unified protocols, custom evaluation pipelines adding excessive overhead, and risks of model overfitting or contamination from static datasets.

Robotic multimodal generation models (Vision-Language-Action) face additional benchmarking challenges due to insufficient physical dynamics priors, with current benchmarks documenting semantic understanding or dynamics separately. Modular benchmarks are proposed for disentangling and integrating semantic, dynamic, and control aspects across scenes and actions. DataVista is the first benchmark dedicated to animated chart/video narrative understanding, emphasizing evaluation across modalities and time for domains like news and business analysis. The need remains for integrated, multi-dimensional benchmarks, accurate evidence integration across modal and temporal frames, and coverage for specialized video formats [9][10].

## Trends and Open Problems
Video and multimodal generation continue to grapple with achieving scalable inference (especially in diffusion models), integrating robust semantic and visual grounding, and ensuring consistency across modalities and temporal dimensions [1][7]. Unified models and agent-native frameworks represent a promising path toward adaptable, high-fidelity multimodal content, but benchmarking lag, protocol fragmentation, and limited domain coverage pose ongoing obstacles [9][10].

Data contamination, protocol fragmentation, and model overfitting are critical risks, particularly in dynamic or real-world evaluation scenarios [9]. Domain-specialized models (medical, robotics) highlight the need for benchmarks that target integrated reasoning, evidence aggregation, and scenario-driven evaluation [2][9][10]. As multimodal generation scales, addressing these open problems will be essential for reliable, generalizable progress across diverse domains.

## References
[1] Evolution of Video Generative Foundations. web. https://arxiv.org/html/2604.06339v1 (n.d.)
[2] nnFoundation: 3D Foundation Models for Radiology. arxiv. https://arxiv.org/abs/2609.26924 (2026-09-22)
[3] GEMS: Agent-Native Multimodal Generation with Memory and Skills. hf-search. https://huggingface.co/papers/2603.28088 (2026-03-30)
[4] OmniGen2: Exploration to Advanced Multimodal Generation. hf-search. https://huggingface.co/papers/2506.18871 (2025-06-23)
[5] DuoGen: Towards General Purpose Interleaved Multimodal Generation. hf-search. https://huggingface.co/papers/2602.00508 (2026-01-31)
[6] OneSearch-VL: Unified Multimodal Deep Research Agent for Image and Video. hf-daily. https://huggingface.co/papers/2610.12419 (2026-10-08)
[7] MC-Sparse: Deconstructing and Closing the Dense-Sparse Attention Gap in Diffusion Transformers. hf-daily. https://huggingface.co/papers/2610.06801 (2026-10-05)
[8] VBench: Comprehensive Benchmark Suite for Video Generative Models. web. https://openaccess.thecvf.com/content/CVPR2024/papers/Huang_VBench_Comprehensive_Benchmark_Suite_for_Video_Generative_Models_CVPR_2024_paper.pdf (n.d.)
[9] Rewiring Semantics, Dynamics, and Control: A Simple yet Effective Action-Centric Tri-Stream Transformer. arxiv. https://arxiv.org/abs/2610.11416 (2026-10-08)
[10] DataVista: Diagnosing Multimodal LLMs on Data Video Understanding. arxiv. https://arxiv.org/abs/2610.11993 (2026-10-08)
