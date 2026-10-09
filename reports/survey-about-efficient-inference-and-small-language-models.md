# Survey about Efficient Inference and Small Language Models

## TL;DR
- Small language models (SLMs) are rapidly closing the performance gap with larger LMs through cutting-edge innovations in quantization, knowledge distillation, speculative and token routing systems, offering up to 3.5× improved latency and significant resource savings in real-world applications [1][2][3].
- Hardware and system-level breakthroughs, such as deploying SLMs on GPUs/FPGAs/ASICs and system-architecture co-designs, are essential for maximizing throughput, reducing costs, and enabling robust edge and on-device applications [1][4].
- Model compression, distillation, and routing unlock SLM deployments in industry and on mobile/edge hardware, with studies reporting SLMs rivaling or outperforming larger LMs for specific tasks [5][6][7][8].
- Despite efficiency gains, open challenges remain in standardized evaluation benchmarks, cross-domain generalization, and dynamic adaptation to deployment hardware [5][4].

## Background
The rapid growth of large language models (LLMs) has accelerated concurrent research into small language models (SLMs) optimized for efficient inference. Foundational advancements, such as quantization, pruning, and knowledge distillation, have enabled smaller models to approach or match the functionality of LLMs for targeted tasks while requiring fewer computational and memory resources [4][5]. Benchmarking studies and large deployments increasingly highlight the efficiency, versatility, and industrial applicability of these optimized SLMs, which excel when paired with innovative inference strategies, such as shape-adaptive architectures and token routing [1][3][6].

Quantization, reducing model weights to fewer bits (e.g., INT8, mixed precision), remains a cornerstone for deploying SLMs, drastically decreasing memory footprint and boosting inference speed [1][4]. Pruning less critical model components complements these gains. Distillation, where small models are trained to mimic larger ones, further allows SLMs to provide high accuracy at reduced cost, particularly in mobile and edge settings [5][7][8].

## Innovations for Efficient Inference
Recent advancements in efficient inference techniques underpin the success of SLM deployment. DynaCore introduces a shape-adaptive system that dynamically optimizes for the prefill and decoding phases using disaggregated quantization—dual-side for prefill and weight-only for decoding. This system achieves a 3.5× lower time-to-first-token (TTFT) and over 36× improvement in throughput compared to classical quantization methods, illustrating the value of hardware/software co-design [1].

BitNest represents another leap, merging bit-nested speculative decoding with shared model weights: a low-precision draft is embedded within the full-precision weights, achieving a speculative acceptance rate of up to 95.2% and delivering 1.48–1.61× end-to-end speedup over conventional FP16 inference across multiple 7B–8B “edge-friendly” models [2]. SketchSSM further showcases how low-rank basis approximations within state memory access can allow full-state updates while cutting recurrent-state access by a factor of ten and delivering over 2.7× higher decoding throughput with zero accuracy loss [9].

On the system side, token-level routing—like TokenRouter—schedules inference workloads across model sizes, increasing both throughput and result quality [3]. Systems like SketchSSM enable supporting much larger batch sizes for decoding by capping KV-cache growth, optimizing for both linear and hybrid attention jobs [9].

## Comparative Analysis of Recent Small Language Models
SLMs are increasingly practical for real-world applications, especially as task- and application-specific fine-tuning unlocks efficiency advantages. Surveys and studies show SLMs outperforming larger LMs in both accuracy and running time for niche tasks—cloud supply chain applications are a strong example [5][6]. Model compression methods, especially distillation, deliver large drops in inference cost and latency while maintaining robust performance, which has made SLMs attractive for industry tasks like recommendation systems [5][7].

Knowledge distillation and aggressive quantization compress large models into deployable SLMs capable of running on-device and in the absence of GPUs, as shown in recent studies where small language models are able to run retrieval-augmented generation tasks directly on edge and mobile devices without GPU acceleration [8]. Architecture- and system-aware taxonomies highlight that SLMs now support industrial-scale applications, providing strong accuracy, fast inference, and minimal overhead [5][7][8].

TokenRouter demonstrates cutting-edge workload scheduling, efficiently balancing jobs between SLMs and larger peer models to maximize user experience and system utilization [3]. The system addresses the challenge of efficiently scheduling inference workloads among small and large models, and has demonstrated substantial efficiency and quality improvements in live studies.

The practical deployment of SLMs on edge, mobile, and constrained infrastructure is now common, supported by efficient inference pathways and robust system-level optimizations [8][3][7].

## System and Hardware Strategies for Maximizing Inference Efficiency
System and hardware strategies are the backbone of high-performance SLM inference. Quantization and pruning are standard compression techniques: INT8 and hybrid/mixed-precision reduce computational load and allow transformer SLMs to run faster on GPUs, ASICs, and FPGAs. Pruning targets redundant model paths, further shrinking inference times [4].

Operator and system-level improvements—such as custom deployment frameworks and hardware-optimized compilers—are crucial. These methods optimize transformer block execution for each hardware class (GPU tensor core utilization, FPGA mapping, ASIC logic design), and deployment frameworks recommend matched pairs of models and hardware for maximum throughput [4]. Novel frameworks like DynaCore adjust batch scheduling and execution blocks dynamically to match workload (prefill versus decoding) and underlying silicon [1].

Hardware-guided design is a rising trend: frameworks like SketchSSM and DynaCore allow models to maintain high throughput even as batch sizes grow, using advanced KV-cache and scheduling innovations [1][9]. Surveys show that best-in-class SLMs consistently achieve top throughput, lowest TTFT, and high energy efficiency when tightly co-designed with deployment hardware [4].

## Trends and Open Problems
Despite significant progress, open issues challenge the next era of SLM development. A major obstacle is the lack of universally robust benchmarks: as SLM deployment grows, standardized, resource-aware, and multi-task benchmarks are needed to accurately compare models [5]. Domain-specific tuning can obscure head-to-head measurement, complicating the development of generalizable SLMs.

Systems innovation remains a hotbed for advancement, with token-level routing, hybrid scheduling, and adaptable hardware/software stacks emerging as trends likely to define real-time and edge SLM deployment [3]. The continued growth in hardware diversity intensifies the need for model-hardware co-design. Runtime scheduling, speculative decoding, and batch-aware systems, as showcased in BitNest and DynaCore, point to a future where SLM efficiency is maximized at all levels [1][2].

Ongoing research is tackling deployment challenges, from minimizing performance loss in compression to robustly generalizing across tasks, data shifts, and operating hardware [5][4]. As the field matures, seamless integration of efficient inference with evolving hardware and diverse application domains will remain the central open problem.

## References
[1] A Shape-Adaptive Architecture with Disaggregated Quantization for Efficient LLM Serving. arxiv. https://arxiv.org/abs/2610.07443 (2026-10-05)
[2] BitNest: Bit-Nested Speculative Decoding for Memory-Efficient LLM Inference Acceleration. arxiv. https://arxiv.org/abs/2610.02800 (2026-10-02)
[3] TokenRouter: Efficient Serving System for Token-Level LLM Routing. hf-daily. https://huggingface.co/papers/2610.12242 (2026-10-08)
[4] Accelerating language giants: A survey of optimization strategies for LLM inference on hardware platforms. web. https://www.sciencedirect.com/science/article/abs/pii/S1383762126000081 (2026-03-01)
[5] A Survey of Small Language Models. hf-search. https://huggingface.co/papers/2410.20011 (2024-10-25)
[6] Small Language Models for Application Interactions: A Case Study. hf-search. https://huggingface.co/papers/2405.20347 (2024-05-23)
[7] Scaling Down, Serving Fast: Compressing and Deploying Efficient LLMs for Recommendation Systems. hf-search. https://huggingface.co/papers/2502.14305 (2025-10-26)
[8] Little Brains, Big Feats: Exploring Compact Language Models. hf-daily. https://huggingface.co/papers/2606.30062 (2026-06-29)
[9] SketchSSM: Write to the Full State, Read from a Compact Sketch. web. https://searcharxiv.com/abs/2609.33051 (2026-10-06)
