# PKM Update and Obsidian Plugins

![Plugins page on Obsidian website showing the available plugins](/static/obsidian-plugins.png)

## After demonstrating last year [how I use Obsidian to manage my day-to-day activities](/2023-09-17_pkm) and longer term professional learnings, I wanted to take a step back while I was away from work and see what I could improve in my workflow. What resulted was a side project that produced [3 Obsidian plugins](https://obsidian.md/plugins?search=jamie%20hurst) that help to orchestrate the workflow, and are available for everyone to use in a similar way.

As I posted in an [earlier article](/2023-09-17_pkm), I've been using Obsidian as a tool to handle my personal knowledge management (PKM) at my day job. As I defined and refined my daily and weekly processes for keeping on top of things, including my TODO lists, I wanted to formalise the process a little and make it easier for me to operate, so I built a Python-based CLI wrapper for Obsidian that manipulated some of the vault files, such as copying over incomplete TODO items from day-to-day.

I've been on paternity leave for a few months now, and in the small spare time I had, I wanted to learn how to create plugins within Obsidian itself rather than relying on what I was increasingly believing to be a "hack". I devised a specific set of functionality I wanted to achieve, which included the following:

- Management of daily, weekly, monthly and quarterly notes
- Management of TODO lists in these periodic notes, and elsewhere such as in a project setting
- Tying in these TODOs to a Kanban board
- Picking up new notes automatically into an "inbox folder" to be organised later, so I don't need to think about that at the time

Obsidian has a huge amount of plugins already available, some of which I detailed in the previous article that I use extensively. In particular, there was a fair bit of overlap with some of these, so I didn't want to reinvent the wheel, and decided to expand the initial functionality these plugins have by adding a new layer on top of them.

The plugins I planned to use were:

- [Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes)
- [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks)
- [Kanban](https://github.com/mgmeyers/obsidian-kanban)

These also gave me a fantastic basis for how I could develop the functionality I wanted. Rather than build one overarching plugin that would only fit me and my needs, I decided to split the functionality a little:

1. A way to automatically create and manage periodic notes, pinning these to your tabs if you want
2. Management of TODOs in periodic notes and elsewhere, including Kanban board support
3. Capturing new notes into an inbox folder and way to easily organise them

I'm pleased to say that I successfully managed to get the three plugins developed over the last few months, and have already quite a few downloads of each of them from the Obsidian website, where they are all published and available to download from along with the Obsidian client directly.

### [Auto Periodic Notes](https://github.com/jamiefdhurst/obsidian-auto-periodic-notes)

The first plugin is an extension to the excellent Periodic Notes by Liam Cain. It creates new periodic notes automatically in the background for daily, weekly, quarterly, monthly and yearly entries, and optionally opens and pins them into your open tabs. It uses the [Daily Notes Interface](https://github.com/liamcain/obsidian-daily-notes-interface) to provide a consistent bridge between the surrounding plugin.

![Auto Periodic Notes: Example of notice in Obsidian, showing creation of today's daily note](/static/obsidian-auto-periodic-notes-notice-example.png)

![Auto Periodic Notes: Example of Settings screen within Obsidian](/static/obsidian-auto-periodic-notes-settings.png)

### [Auto Tasks](https://github.com/jamiefdhurst/obsidian-auto-tasks)

The largest entry provides a few functions relating to TODOs:

- Reads tasks from previous periodic notes and carries over any incomplete ones
- Adds the header for tasks when creating the note
- Searches all or specific headers within the periodic note so you can separate a daily list from other areas
- Adds a due date to copied tasks so they can be appropriately tracked in the Tasks plugin
- Collects tasks from the whole vault and adds them to a central Kanban board automatically

It works with the Periodic Notes plugin too, along with, optionally, the Tasks and Kanban plugins. 

![Auto Tasks: Example of tasks in a daily note within Obsidian](/static/obsidian-auto-tasks.png)

![Auto Tasks: Example of tasks shown in a Kanban board within Obsidian](/static/obsidian-auto-tasks-kanban.png)

![Auto Tasks: Example of Settings screen within Obsidian](/static/obsidian-auto-tasks-settings.png)

### [Inbox Organiser](https://github.com/jamiefdhurst/obsidian-inbox-organiser)

Finally, the last plugin simply collects all new notes created within the root of the vault, and offers an interface to migrate these into appropriate folders.

![Inbox Organiser: Example of organiser modal](/static/obsidian-inbox-organiser-modal.png)

### Development

Each plugin is completely standalone, written in TypeScript and has its own GitHub repo and package requirements; however they are built in a very similar way. They each require the Obsidian API and provide a `src/` folder that contains the main plugin class, along with separated functionality into a logical make-up. Each plugin was developed with Node.js v20.

If you wish to trial development or make adjustments, the simplest way is to symlink the cloned directory to your Obsidian vault's plugin folder, e.g.:

```bash
ln -s obsidian-inbox-organiser ~/.obsidian/plugins/
```

This then allows you to compile reactively when any changes are made and see the changes in Obsidian once a "Force Reload" has been triggered from the View menu:

```bash
npm run dev
```

The plugins were developed using existing plugins as a basis, especially the Periodic Notes plugin, together with documentation from the [Obsidian API](https://docs.obsidian.md/Reference/TypeScript+API/AbstractInputSuggest/(constructor)) and the [community pages](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Community+Talks/Plugin+Testing+for+Developers), which dive into a lot deeper topics on some aspects. Unfortunately, while the Obsidian docs have some excellent resources for getting started, trying to find how to operate and manipulate some of the functionality that is exposed can be a bit of a challenge, especially when you only have the types exposed through the API and not the actual functionality - I always find reading through the source-code of a dependency the easiest way to figure out what it's trying to do. In some cases, a GitHub search was required to find some examples of some of the classes, such as AbstractInputSuggest.

### Testing the Plugins

Building tests for Obsidian plugins is a little more tricky. There are no official examples on how to put this together, but a few plugins that are out there have started to build tests for themselves. They mostly use Jest, so I followed even though it's not the fastest testing framework these days. Even so, steering away from the Obsidian API by decoupling and wrapping certain functionality is essential, and I ended up creating more than a few mocks of the core classes and objects in order to prove my custom functionality.

There are a few sets of examples and information that were especially helpful when I was developing my extensions:

- [Obsidian Community on Testing](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Community+Talks/Plugin+Testing+for+Developers) - this section of the community pages contains a fair bit of information on some of the example plugins that have some tests in place, although the coverage can be a little spotty, and there are still no UI tests in place for any of these
- [Obsidian Discord on Testing](https://discord.com/channels/686053708261228577/962362830642905148) - the Discord is extremely helpful, and has a thread dedicated to information on testing, where a few experienced individuals share knowledge, especially Clare Macrae of the [Obsidian Task Group](https://github.com/obsidian-tasks-group).
- [Jest Environment](https://github.com/obsidian-community/jest-environment-obsidian) - one of the more helpful aspects is the Obsidian environment for Jest, which mimics a lot of the functionality from the core library of Obsidian that's required for testing. It's not complete and there were still some gaps I needed to mock, but the HTMLElement extensions in particular were extremely useful.

### Contributions

There are some users of the plugins who have already submitted issues and ideas onto the GitHub plugin pages. I welcome this as I really want to improve and get this in a position where others can make use of it. I would especially welcome contributions from other parties who want to help collaborate on the current state and make these even more useful.

This has been a wonderful side project over the last few months to reimagine something that I used internally at work to something that can help others to cultivate similar workflows.

### Usage

To install the plugins, simply search for the names above within the Community Plugins section in your Obsidian app, or visit the [Obsidian plugins website, searching for my name](https://obsidian.md/plugins?search=jamie%20hurst).

_Note: Inbox Organiser is not published just yet, it's awaiting a final review from Obsidian developers._