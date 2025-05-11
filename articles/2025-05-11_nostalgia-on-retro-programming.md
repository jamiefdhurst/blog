# Nostalgia on Retro Programming

![PHP Code in Notepad++ Running in Windows XP](/static/notepad-pp-banner.png)

## Remember the days of table-based layouts, FTP deployments, and coding PHP in Notepad++? Before Git workflows, containerization, and AI-assisted coding, there was a simpler era of web development that shaped many of us. I've been a developer now for almost 20 years, but back when I was learning and practising my new skills, I was coding things in PHP on Windows machines—something I haven't done for a very long time, but remember very fondly. Given how dramatically the developer experience has transformed over the last few months with generative AI tools, never mind the past two decades, I wanted to revisit a slightly simpler time and see what development was really like back in 2005.

Although I have a Computer Science degree, I'm originally a self-taught developer who started exploring HTML, CSS and PHP as early as 2005, back when I was in school and college. I built a bunch of over-complicated and unnecessary websites that weren't seen by anyone, and have now been lost to the winds of time. I was very fortunate back in late 2007 to get a job working as a part-time developer while studying at [LINGsCARS](https://www.lingscars.com) where I spent the next five years learning an absolute ton and having a bunch of fun.

These days I spent my days alternating between writing business cases, building quick proof of concepts, solving some very difficult organisational-wide engineering problems and mentoring developers across the organisation. I'm very passionate about developer experience and how we can made a developer's life easier day-to-day, while ensuring that building secure, scalable and maintainable code is so easy that its second nature. The last few months in particular has seen a huge surge in generative AI tooling for developers that is continuing to transform what they're using and affecting the fundamental software development lifecycle (SDLC). I wanted to take a step back and see how far we've come, right from where I first started building commercially. This was partially to see if I still remembered everything and could do it, but also because I felt myself getting a bit misty-eyed and nostalgic about times past, and that's something that I'd prefer to stamp out now.

My plan was to setup a machine similar to one I was using back in 2005: with Windows XP and only tools available from that time, so I could see what the development lifecycle looked like. A Windows XP machine is not something that's safe to expose to the internet these days, so I refrained from giving it any access beyond my local network to transfer files. Unfortunately since originally trying this out I've now upgraded to a Silicon-based Macbook Pro, and can no longer run the original VirtualBox machine as it requires an x86-based architecture, not an arm one, but I helpfully recorded everything before.

### VirtualBox Setup

Windows XP is now abandonware, so you can download an ISO and get a working product key from [Archive.org](https://archive.org/details/WinXPProSP3x86). I used [VirtualBox](https://www.virtualbox.org/), a free virtualisation tool from Oracle, to run the machine and get things set-up. Windows XP back then didn't need much, and I only downloaded the 32-bit version anyway, so my settings for VirtualBox were as follows:

![Screenshot showing VirtualBox settings for Windows XP VM](/static/xp-virtualbox-settings.png)

- 1x CPU only
- 1GB RAM
- 10GB of storage
- No networking

Virtualbox handled the setup and the install was much quicker than the last time I tried it on real hardware.

![Windows XP installation process](/static/xp-installation.png)

I mounted a couple of folders within XP using VirtualBox's guest additions onto drive letters, meaning I could easily transfer files in and out of the machine as I was building things.

As soon as I heard the familiar startup jingle, I was in and staring at the familiar wallpaper, instantly taking me back to all those years ago...

![Windows XP initial desktop](/static/xp-desktop.png)

Now that the operating system was installed, I needed to set up my full development environment, 2005-style.

### Tools

I wanted to build a fully-functional website that needed a database and a local server, and a way to edit this all. There were a few ways to do this back in late 2005, but I distinctly remember using WAMP as my environment of choice: it came with an Apache server (Apache was _only_ an http server back then), a MySQL database server and PHP ready to integrate into Apache. I didn't need to configure anything or set up any virtualisation or containerisation, it ran (on my machine admittedly) straight out of the box.

![WAMP startup screen](/static/wamp-5.png)

Specifically, given I opted for the late 2005 installation setup, it came with:

- Apache server 1.3
- MySQL 5.0
- PHP 5.1

Helpfully, WAMP came pre-installed with phpMyAdmin so I could easily create a database and setup some tables as needed.

![phpMyAdmin](/static/phpmyadmin.png)

I also installed Mozilla Firefox, which was a brand-new browser back in 2005, because I simply couldn't face using Internet Explorer - unfortunately I still have horrible memories of losing entire days to CSS tweaks and bugs across that suite of browser back in the late 2000s. I'm not ready to relive all of my experiences from back then.

PHP IDEs weren't as extensively used back in 2005, with standard syntax-highlighting text editors being enough for most folks to get on with. My editor of choice back then was Notepad++, so I promptly installed it and got started.

### Developing

I'd originally started building websites in PHP 4, way back before object-oriented support was fully available in the language. 5.0 introduced classes, interfaces and standard OO features that were still very new to most developers back in 2005. I wanted to keep things as simple as possible, just to prove I can still make PHP work, so I opted not to build out a full MVC framework this time, and to go back to the old ways of using `require_once` with PHP template files.

I decided to build something that I could continue if I wanted, so a car leasing website was an easy go-to. I could start by building out the initial listings on the homepage and decide if I wanted to dive a bit deeper later by building out the deal detail pages and maybe even a simple ordering system.

Firstly, I needed some database tables to store out the fundamentals - I overcomplicated this slightly at this stage, building out a set of make, model, trim and deal tables. There's a function file that is required by other files and requires a connection to the database, providing helper functions to get a set of deals in the correct order and a set of makes and models to provide deeper links to at a later time.

```
CREATE TABLE `deals` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `trim_id` int(11) unsigned NOT NULL,
  `profile` varchar(5) NOT NULL,
  `mileage` varchar(3) NOT NULL,
  `initial` decimal(8,2) NOT NULL,
  `payment` decimal(8,2) NOT NULL,
  `special` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `ordering` (`special`,`payment`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
```

```
$db = mysql_connect('localhost', 'cars', '*********');
if (!$db) {
	die('ERROR: Could not connect to MySQL: ' . mysql_error());
}
mysql_select_db('cars', $db) or die('ERROR: Could not select correct DB.');
```

There was no need to complicate things at this stage with any objects, DTOs or database abstraction layers, so a simple integration using the now very old and very deprecated `mysql_` extension functions was the easiest way.

```
function get_listings() {
	global $db;
	$query = "
		SELECT
			d.id, d.profile, d.initial, d.payment, d.mileage,
			t.description AS trim,
			m2.name AS model, m2.image,
			m1.name AS make
		FROM deals d
		INNER JOIN trims t ON d.trim_id = t.id
		INNER JOIN models m2 ON t.model_id = m2.id
		INNER JOIN makes m1 ON m2.make_id = m1.id
		WHERE d.special = 1
		ORDER BY d.payment
	";
	$result = mysql_query($query, $db);
	if (!$result) {
		die('ERROR: Could not fetch listings: ' . mysql_error());
	}
	$rows = array();
	while ($row = mysql_fetch_assoc($result)) {
		$rows[] = $row;
	}
	
	return $rows;
}
```

I added a `head` and `foot` include to produce the header and footer of the main template files, which will make it easier to add additional pages at a later date. Finally, the `index` file doesn't have much to do: it loads the functions, head and foot files and pulls the listings, iterating over them to build a set of listings, building out a very simple PHP index as follows:

```
<?php
require_once('includes/functions.php');

$listings = get_listings();
$listings_rows = ceil(count($listings) / 4);

require_once('includes/head.php');
?>
...HTML...
<?php
require_once('includes/foot.php');
```

For the HTML and CSS I also decided on a traditional approach: 2005 was smack-bang in the era of table-based layouts and way before we used divs, positioning and when something like flexbox was a pipe-dream. The CSS is deliberately simplistic and works well in Mozilla Firefox 1.0, I don't have any intention of testing it in Internet Explorer.

After pulling and modifying some CC licenced images and designing an era-appropriate logo, my experiment was complete.

![Finished Jamie's Cars Homepage](/static/jamies-cars.png)

[All the code is available in GitHub](https://github.com/jamiefdhurst/jamiescars), where if I decide to continue my experiment at a later date I'll publish any changes to.

### Conclusions

Stepping back in time was a mixed experience all-in-all. It was nice to look back on how things were and to give something a little simpler a try again, but if anything it made me reflect on how far we've come in terms of developer experience over the last 20 years.

While Notepad++ was more than sufficient back in the day, I've been spoilt by access to IDEs over the last few years. Having to navigate between different the editor and Windows Explorer to open and create files was a bit of a pain, there was no linting behind basic syntax highlighting, and no way to check definitions of libraries and functions on the fly. I needed a browser tab with an archived version of PHP.net open on my laptop to check whether I was using the functions in the right way, and the simplest way to check whether the script was correct was to save and refresh the browser. Xdebug was an extension available for PHP to generate stack traces within the browser, but was not installed by default within my WAMP installation, so I had access to basic error messages instead.

Then we get on to testing, or the lack of. The culture of PHP back in 2005 was not one of unit testing, and I knew very few people who used PHPUnit or anything remotely close to automated end-to-end testing. It was completely possible to do, but not a mature practice. It feels completely alien to me now to build something and not consider how I'm going to verify this before I hand it over to my colleagues.

I haven't dived into how this would originally have been shipped and deployed, either. Back in 2005, I'm ashamed to say that there were a couple of methods of deployment for me: either rsync the files up periodically to a remote server, or simply FTP them into the right place. There was no git, no version control, no tracking, no history and no build. If I wanted to ensure I was preserving the state of a file before a change, I would copy it and keep a few of those around. This translated into my day job too, although I did eventually learn the error of my ways and implement a git workflow with an actual build and automated deployment, including a staging environment.

Finally, I'm getting more and more used to the generative AI workflow now when I approach coding. I open a new tab and tell the AI what I'm building and what I want from it, and decide whether I want to lead or whether I want it to, and go from there. I don't leave the IDE as much and tend to ask anything I need directly to the interface, instead of jumping between browser windows. To put it simply, I stay in the "flow". This is something that's very recent for me in the last few months, and something that still doesn't feel completely natural, but I'm getting there.

Looking back at the journey from simple table-based layouts and FTP deployments to more containerised environments and AI-assisted coding, I can reflect a little on not just by how far our tools have evolved, but how fundamentally our entire approach to software development has transformed. Where we were once familiar with isolated and manual processes with minimal safety nets, we've moved to collaborative, automated workflows designed for reliability and scale. While I appreciate the simplicity of the past, it does mean that I'm also grateful for the capabilities and practices we now take for granted.

### Next Steps

I'm not done with the fun that I've had here, and there are several aspects I haven't had a chance to explore just yet that I want to continue in the near future:

- **Deployment**: I want to set up an older Linux server to deploy into, maybe with similar versions of Apache and MySQL. If there's a safe way that I can expose this over the internet with a proxy in the way, I'll do it. This might give me a chance to introduce a simple rsync or download-based workflow
- **Migrate to PHP5**: One tradition I don't miss is when every marketing agency and local business had their own custom framework or CMS, as obviously they could write a better one than an open-source entry like Wordpress or Joomla. Even without going full MVC, I'd like to implement a very basic router and template abstraction so I can make it easier to expand and test in the future, and to avoid repetition as I build out more features
- **Testing**: I'd like to explore how PHPUnit was back in 2005 as it wasn't something I ever used, and how I'd be expected to write unit tests with the simple setup I have, especially if I can somehow integrate this with a CI workflow to check things automatically
- **More features**: Finally, there are a few more features I want to build. I'd love an old-fashioned admin panel, some more frontend pages and perhaps an order system to try and open things up a little. As I expand I might look into some of the early frontend changes I used back then with initial Ajax asynchronous requests and how they worked in different browsers. I may finally have to try the different IE versions to check things are working well

In the meantime, I need to see whether I can get VirtualBox to spin up my x86 machine on my Silicon MBP, or whether I need to find a completely different approach to running older machines on my new hardware.
