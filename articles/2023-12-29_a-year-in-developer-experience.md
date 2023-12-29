# A Year (Almost) in Developer Experience

![Seeing Code Clearer Through Glasses](/static/developer-experience.jpg)

## Almost a year ago, I started a new role as a Principal Software Engineer in Developer Experience, a role that while I'm passionate about, definitely started with some misconceptions. This is a short article about some of my initial experiences over the last year and the important takeaways I have, and how I'm going to use this to go forward in 2024.

Like many, I've had a relatively varied career. I started as a PHP web engineer, moved into more systems development, co-founded a startup, moved back into software but branching out into Python, Java and Go, then into DevOps specialising in Docker workflows, then Kubernetes and AWS, leading a team of multi-disciplined engineers running a set of applications and software, then a set of lead developers looking after cloud-based workloads. Now I'm back to being an ["IC" (Individual Contributor)](https://srihariblogs.medium.com/individual-contributor-role-vs-manager-role-78649f91ddff), I'm enjoying applying some of my skills and experience onto something a little different, trying to help other developers contribute more value, quickly.

I've been in my current role now for almost 12 months, so this is my check-in of what I've learned so far, and what I plan to work on (personally) in 2024.

I'm not going to describe what Developer Experience is, [many others](https://medium.com/swlh/what-is-dx-developer-experience-401a0e44a9d9) have done a fantastic job of covering this in other articles. This is more about my experiences over my time in the role and what I try to bring to the table.

### Your Platform is a Product

Most engineers build a product for a company's end customers, but platform engineers build for other engineers. What doesn't change is that your platform is still a product, just one for your own internal customers.

Thinking in product terms puts you in a customer-focused mindset and aligns your goals:

- **Delivering in Sprints** - Break your features down into epics and stories, and think about your acceptance criteria from the perspective of your customer personas: wat are you building and why? Ensure you deliver your features incrementally and demonstrate these directly to your customers.
- **Release Early, Release Often** - Don't wait until your platform is perfect to ship, there is huge value in shipping features as soon as you can and iterating on them to ship even more as often as you can - your customers will appreciate your rapid development cycles.
- **Customer Feedback** - Get your customers using your platforms as soon as they can, even if that's only in their development environments. Their feedback is vital to understanding if you're improving their experience and improving their ability to deliver end customer value, so listen early and listen often.
- **Support and Uptime** - Finally, things are going to go wrong. Being able to respond promptly and set appropriate guidelines and SLAs for your platforms is imperative so your customers understand what to expect from you when the inevitable happens.

Ultimately, providing a similar experience that a company would for its end customers will deliver a better Developer Experience for your teams.

### Documentation is not an After-thought

Once your platform is built, your customers will want to use it. You'll be catering for all sorts of developers within your business - well-established folks with a lot of domain and business-specific knowledge, all the way to new starters who have a lot of experience elsewhere, but are not used to the naunces and specifics of your company. Documentation is the key to providing a common understanding to all.

There's a lot I've learned about docs over my time:

- **Consistency** - Across your platform, there may be many teams, products and tools. Each of these should establish the same quality of documentation and provide a consistent way to present similar information, whether that is how your documents are outlined, indexed, or the writing style itself, try and make your documents as consistent as possible.
- **Searchable** - A good title is a start, but really your documents should be easily searchable for anyone trying to find the information. Think about all the terms your customers may use to search for this information and if you need to, tag it.
- **Predictable** - Your documentation should be consistent in its tone, but also in how its linked and ordered. Ensure that documentation that may be related is easily linked from multiple areas across the organisation so that customers can easily find relevant information when they're close by.
- **Timely** - Your documentation must be kept up-to-date. An article that refers to a process that no longer exists or a tool that is out of support is performing a worse duty than no documentation at all. Try and hold reviews on older documentation and ensure you have a process to easily feedback when something doesn't look right.
- **Packaged** - Release your documentation alongside any new features, don't think of it as an afterthought. Your customers will want to know how to make the best use of their new platform, be it through examples or through careful explanation, so don't think of this as an optional or process you can delay till later.

I'm not saying I practice all of the above day-to-day - I'd certainly like to, but this is certainly a good way to ensure you're on the right track.

### The "Golden Path"

Since [Spotify refined the idea of a Golden Path](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem/) for Developer Experience, this has been the go-to term for establishing what a platform team chooses to support and how they make that journey clear to their customers. Some use a fully-integrated [Backstage](https://backstage.io/) experience to deliver this, but most importantly, these paths should be defined and scoped by the needs of your customers, not just the needs of the platform teams.

Some things I've learned to consider over the last year include:

- **API Lifecycle** - How your end-customers use APIs is one thing, but how your internal customers interact between each others' services helps to set expectations and common understanding between teams. Making it easy for your teams to provide a predictable lifecycle and manage their API specifications should inherently be part of any backend service path.
- **Multiple Languages and Frameworks** - Having one choice for backend and frontend is not always appropriate - you may have teams with different levels of experience and different requirements, so be prepared to be flexible and understanding when it comes to what you support.
- **Build Tooling and Ecosystems** - Integrating all of this with a common CI/CD platform can become a real challenge, but that's part of the platform's responsibilities - the reality is that most developers don't care how their software is built, and just want to be able to deliver faster. If you need to support some complex build tooling, think about how you can make it easy for your customers to get the most from this.
- **Infrastructure** - How your software fits into your infrastructure and how customers can easily build out the platforms they need should be part of your paths too - if they need a data store or a queue, think about how you can make it easy for them to achieve this and deliver it all the way through your environments.

### Always Be Learning

Naturally, the technology landscape changes so much year-on-year that it can be hard to keep up with emerging trends and what to focus on next (ChatGPT, anyone?) - but taking some time to try and stay ahead of the curve and keep reading on what others are doing helps me to think about where I could shift focus to better support customers and developers in our organisation. Like many others, I use some of my personal time to explore a few projects (e.g. my [Journal in Go](https://github.com/jamiefdhurst/journal), this [Blog](https://github.com/jamiefdhurst/blog), some [infrastructure automation](https://github.com/jamiefdhurst/jenkins) and more) but I try and find PoCs and projects to get involved in during work hours that allow me to do the same.

In any case, a few of the newsletters I try and make some time to read each week right now include:

- [Software Lead Weekly](https://softwareleadweekly.com/)
- [DevOps Weekly](https://www.devopsweekly.com/)
- [Programming Digest](https://programmingdigest.net/)
- [Leadership in Tech](https://leadershipintech.com/)
- [SRE Weekly](https://sreweekly.com/)

I do need to find more time to listen to more podcasts instead of simply reading newsletters, but I find this medium of information is easier for me to digest.

In 2024, I'm planning to use a lot of what I've observed and learned to try and make an impact on the teams I work with; hopefully this article has given you a few tips and pointers to be able to do the same.
