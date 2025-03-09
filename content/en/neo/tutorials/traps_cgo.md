---
title: Traps of CGO
type: docs
weight: 1000
---

> The title "Traps" was chosen with a twist in the conclusion, and although it may be a bit difficult, this is a summary of the analysis of the issue where RSS (resident) memory significantly increases and does not decrease or continues to increase when simultaneous user requests are concentrated, as experienced by a recent customer.

The development language of machbase-neo, Go, has a low possibility of causing memory leaks unless there are specific programming mistakes, and it is equipped with good profiling tools, making it relatively easy to find the cause when there is a problem. However, in this issue, the cause was not intuitive, and despite repeated profiling and analysis, the question was not easily resolved.

machbase-neo runs by calling the machbase-engine written in C through a special method called CGO from the Go code that constitutes user APIs and convenience functions. This memory-related controversy arises in the process of calling C functions through CGO.

All operations of Go are maintained with high concurrency [1][5] through lightweight threads called Go routines. When calling C functions, the calling Go routine is allocated a native thread through the Go runtime and calls the C function in a blocking (synchronous) manner through this thread. At this time, the Go runtime allocates the stack to be used by the native thread in a separate memory area called the system stack, which is not subject to Go's famous Garbage Collector. This memory area can only be returned to the OS when the native thread terminates.[2][3]

When the Go routine calls the C function, the Go runtime checks if there are any idle native threads in its list of native threads. If all native threads are busy, it creates a new thread, allocates the system stack, and assigns it to the requesting Go routine.

The important point is that once a native thread is created, it is maintained and reused until the process ends. If the native thread does not terminate, the memory area of the system stack allocated to the thread is also maintained.[2] The reason for creating new native threads and not terminating them during the process is that it is more advantageous to keep them rather than repeatedly creating and terminating them, and if they were created due to idle thread shortage during peak time, it is assumed that they will be needed soon.

When machbase-neo receives HTTP requests accompanied by hundreds of query executions per second, each request causes at least tens to thousands of C function calls, rapidly increasing the number of native threads and the system stack connected to the threads, ultimately maintaining the increased RSS (resident) memory. In the case of the customer, machbase-neo engine uses less than 10-15GB of memory, and the Go heap memory uses only tens to 200MB, but RSS uses multiple times more than the sum of these numbers. Seeing such a large difference in numbers, anyone would first suspect a memory leak.

The difficulty in ruling out suspecting a memory leak and accurately diagnosing the issue stemmed from the initial assumption that the RSS (resident) memory increase was due to a memory leak, leading to a focus solely on the heap memory area. The actual cause was the interplay between *CGO and native threads*, the *lifespan of native threads*, the relationship between *native threads and system stack memory*, and the fact that *system stack memory is excluded from Garbage Collection*.

The usage of RSS (resident) memory is ultimately determined by the maximum number of concurrently executed native threads during peak time and the High-Water Mark of stack usage. It is not practical to terminate idle threads and reduce memory occupancy during off-peak time because it is usually necessary to (re)use that amount or more next time. The Go runtime uses a policy of maintaining them because it cannot predict how quickly the next peak time will arrive.

From another perspective, the relationship between maintaining vs. terminating threads can be explained by the relationship between service response latency and memory usage. It is a trade-off between minimizing response latency by maintaining threads and returning memory by terminating idle threads. Since both cannot be chosen simultaneously, the Go compiler development team decided to maintain threads (memory) as much as possible to minimize service response latency.[6]

If it is necessary to limit memory usage even at the increment of service response latency, you can control the maximum concurrent calls of machbase engine using the --max-open-conn option[4] provided by machbase-neo. Additionally, there is a way to terminate native threads using the API[7] provided by the Go runtime and some tricks, but considering the trade-off relationship explained earlier, it is judged that the disadvantages outweigh the advantages. The fundamental solution is presented in the roadmap below.

The issue being addressed is ultimately a phenomenon caused by the high demand for native threads due to multiple simultaneous requests, so it is not actually a problem with CGO, which is criticized in the title. Broadly speaking, any server written in any development language will show high memory usage if there are many tasks to be processed simultaneously, as each thread requires stack memory. The difference between development languages is whether to return resources during idle periods or maintain them for the next use. Developers with negative opinions about Go language may have them because they do not have the authority to decide which policy to follow, and it is up to the Go compiler development team.

**Roadmap**

Based on the above conclusion, the conditions under which machbase-neo can be applied when high concurrency is required are limited due to native threads and the necessary memory. It only supports single-node installation, so horizontal expansion is not possible. However, when the *head-only*, *headles*s mode [8] currently under development (beta) is completed, it will be possible to overcome the required resources for high concurrency by distributing them into small node units. Multiple *head-only* nodes can distribute threads for user APIs and convenience functions, and *headless* nodes can handle only the DBMS's original tasks, allowing flexible deployment according to the situation. Furthermore, the completion of *head-only* mode means that multiple machbase-neo nodes can support machbase clusters. In other words, developer convenience features including TQL and web UI will be possible in machbase cluster edition.

{{< figure src="../../operations/img/head-only-1.png" width="400px" >}}
{{< figure src="../../operations/img/head-only-2.png" width="400px" >}}

---

[1] [concurrency vs. parallelism](https://techdifferences.com/difference-between-concurrency-and-parallelism.html)<br/>
[2] https://github.com/golang/go/issues/71150<br/>
[3] https://pkg.go.dev/runtime#MemStats comment on the `StackSys` field.<br/>
[4] https://docs.machbase.com/neo/operations/command-line/ `--max-open-conn` flag<br/>
[5] [Amdahl’s law](https://en.wikipedia.org/wiki/Amdahl%27s_law)<br/>
[6] It may change in the future, but the version, Go 1.23, that builds machbase-neo, and the latest 1.24 keeps the native thread to the end.<br/>
[7] https://pkg.go.dev/runtime#LockOSThread<br/>
[8] https://docs.machbase.com/neo/operations/command-line/#head-only-mode
