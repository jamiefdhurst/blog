# The Dangers of Hype

![Skynet Logo](/static/skynet-logo.png)

## The last few months have seen a huge shift in the developer community: the advent of generative AI and the huge focus it now has within the technology industry. Everything now has "AI" in the title, and there are wild claims about agents replacing developers and performing the same tasks. But what is some of the reality behind it, and is it all just a load of hype?

I jokingly put up the Skynet logo, not very original I admit, to illustrate what "AI" has meant to me in the past. I grew up watching far too many sci-fi films where the narrative around AI showed its ability to learn, often dangerously, and surpass humanity's combined intelligence rather quickly, usually to our final detriment.

What arrived under the initial AI moniker instead is very different, and is an evolution of combined efforts in both machine learning and natural language processing. The current offerings of AI are not something that is going to pass the Turing Test, or something that will (at least currently) endanger our lives; it uses models and freely available information on the web to decide how to interpret and present answers back to you. It's very good at some aspects which it's clearly been trained for (such as software engineering), but terrible at others such as calculations and numeric operations. It has its limits, but it's a very interesting and useful piece of technology.

Coming back to work over the last few months and focusing on GenAI specifically has given me an opportunity to explore new tools, processes and thinking, and specifically how this can impact engineering practices and teams. Other industries are adopting AI in what is perceived to be a fast way, but it's nothing compared to the development community. There are two aspects right now that are affecting the teams I work with the most:

- **Developer Experience**: primarily through IDEs and associated tools, these have rapidly evolved and are now heralding a new era of "vibe-coding"
- **Large-scale Refactoring**: building workflows to assist or automate the refactoring of code, from library updates to language and tool migrations

### Developer Experience

There are multiple large language models (LLMs) out there in the wild today from the big players including Meta (Llama), Google (Gemini) and Microsoft/OpenAI. Once we'd all started building the hype from the initial releases of ChatGPT, it wasn't long before the initial wave of developer tools arrived with GitHub CoPilot. Developers had access to chat with models from within IDEs and receive suggestions and auto-completions as they coded. Soon we received code generation with new classes, unit tests and small-scale refactoring from within the IDEs. Companies and models specific to software engineering such as Anthropic with Claude 3.5 and recently 3.7 Sonnet honed in and improved exponentially on the results given.

The next generation of IDEs and tools have now arrived. Cursor, Windsurf and more have switched the dynamic of how the majority of developers will approach the use of GenAI within their workflow: instead of using the tools as a helper or a prompt, the roles are reversed with the tool now performing the edits, and the developer reviewing and directing the AI in where and why its making these changes. It feels akin to a pair programming dynamic, which is not unfamiliar to a lot of coders, but requires a different set of skills to get the most from the tools themselves.

Tools are now evolving into "agents", where the AI has the ability to learn, reason and make its own decisions based on the human input. This has precipitated the use of "agentic" workflows, which are the latest must-have in the AI landscape: if you're not building something agentic, then frankly what are you doing? It's also created the new term of "vibe-coding", which I personally cannot abide due to the implications it suggests: that suddenly coding is unlocked and anyone can build anything with agentic AI.

This is not the case - it can help with prototyping and getting something built reasonably quickly such as a React app with a simple API and some frontend styling, but its limited in what it can do as it goes further and further ahead. AI does not consider reusability, security, scalability and more: it can get you started, but it requires direction to ensure its making the best decisions along the way. There are too many memes and jokes around LinkedIn and Mastodon of a startup creating its app without engineers, releasing it into the wild and struggling with bugs, security issues and customer dissatisfaction.

This brings an important question: how do we measure the success of these tools and new ways of working? Over the last few months I've seen us move from time saved (which relies heavily on a distorted sense of reality where engineers are _always_ coding), percentage code written (which is closer to reality, but still requires investigation) and there still isn't a one-size-fits-all way to do this beyond looking at developer satisfaction and happiness scores. Businesses are investing in GenAI prompted mostly by the hype, but will soon require how to justify this cost, which is only going to increase as these tools and practices become the norm.

### Large-scale Refactoring

Alongside using LLMs within their IDEs, developers are building out custom tools and workflows using LLM calls. I've always observed in my career that the best engineers always try to automate away as much of their repetitive tasks as they can so they can spend time where they add their value the most. With the advent of AI, there are new possibilities to address the ever-present threat of technical debt. It's always a struggle to balance the need for new features with the need to maintain the existing stack and stay up-to-date, AI presents a new opportunity to build out custom tooling and workflows to look to address some of these common tasks.

I've observed developers start by building simple tools that take in a set of code as context and operate on it to produce some output, then moving towards resource augmented generation (RAG) to inject even more context into the tool, and convert these into multi-step deterministic workflows that can start to make a huge difference on larger and more complex codebases.

There are some inherent challenges in building out these tools:

- **Context**: the context windows for newer models are much larger than in the past, but even with larger contexts models will still lose more precision and awareness as the amount of information they are given increases
- **Iteration**: building out a precise set of prompts to drive these workflows requires a lot of iteration over different scenarios and inputs to ensure the output from the LLM remains consistent and relevant, preventing hallucinations and errors
- **Testing**: there is no easy way to build automated tests for LLM calls today, so even unit testing can be difficult to conduct within these tools and can rely on more flexible end-to-end approaches

As with developer experience, agentic is making its way into this level of automation now. Newer generations of workflows build out and connect a set of agents rather than LLM calls. Each agent has a core responsibility and is able to think, reason and decide the best way for it to perform its own task by accessing its own information through connected tools (using model context protocol, MCP) and even having a set of shared memory between tasks. It's very early days for these tools and new developments are arriving every week, with agent-2-agent protocol being a recent addition to the agentic workflow.

There are now a swathe of tools available to help build out these custom agents and workflows. From visual tools such as LangFlow to more fundamental orchestration frameworks like CrewAI, a platform space is rapidly appearing for developers to easily build, run and maintain a new generation of agentic services to both automate aspects of their own tasks, and the ones needed by their customers.

### What's Next?

Staying up to speed in this rapidly-evolving world is very tricky. One week will see the advent of a new model with a huge context window that opens possibilities on how you can build out your tools, and the next will showcase an acquisition of your chosen IDE by one of the industry leaders. I'm sure that by the end of this year (I'm writing this in May 2025) we'll have a bunch of new terminology and agentic will be old-hat.

One thing I can see both from the developer experience and workflow aspect is the increase of code fungibility. Where once a company's code was tightly protected as IP and small incremental changes were encouraged, GenAI tends to favour writing what is needed at the time only and is not yet in a position to make judgements based on maintainability and ease of readability. The amount of changes per pull request that are driven from AI tooling will increase, and is going to make the act of reviewing code a lot more challenging for developers.

There is a ton of hype around developer jobs and AI's ability to replace them, with some companies claiming AI can now perform the tasks of a junior or mid-level developer. Aspects of the job, yes, but nowhere near all of it. Developer jobs are changing and the skills needed are tilting more towards prompt engineering and being able to make the best use of their tools, but this has always been the case historically. It's an evolution rather than a revolution, and although I can see a developer's core responsibilities changing slightly over the coming months and years, the need for developers is not going away. There are too many unsolved problems and the GenAI industry is moving too fast to solve them all.

I'll leave you with some links I've found helpful recently when trying to stay abreast of the ever-changing GenAI world. I'm not a huge fan of podcasts, so prefer to keep my news and information a little more digestible:

- [Prompt Engineering](https://www.promptingguide.ai/)
- [GenAI Awesome List](https://github.com/steven2358/awesome-generative-ai)
- [Developer News](https://www.developer-tech.com/categories/developer-ai/)
