# Automated Version Releases

![Example of Semantic Versioning](/static/semantic-versioning.png)

## Choosing the next version for your application or side-project can be a tricky process - when you do increase your major version, and what if your patch number is getting a little high? v1.0.0 looks a lot better than v0.1.567 but what's the best approach? I wanted a way of calculating the version automatically using commit messages and built some generic Groovy scripts that can be used in Jenkins builds to increment a version automatically when I merge a PR or push straight to main. This shows the code samples I've put together and how I've been using this privately up until now.

Choosing the next version for your application or side-project can be a tricky process - when you do increase your major version, and what if your patch number is getting a little high? v1.0.0 looks a lot better than v0.1.567 but what's the best approach? I wanted a way of calculating the version automatically using commit messages and built some generic Groovy scripts that can be used in Jenkins builds to increment a version automatically when I merge a PR or push straight to main.

Part of this was to have a path of CI and CD for my side projects, blog and infrastructure; but part of it was to take the hard work out of semantic versioning and determining the correct approach to recording this, providing a consistent approach for everything I put together.

### Semantic Versioning

There's been a lot written on Semantic Versioning in various locations, with [https://semver.org/](https://semver.org/) as the main source. The general and simple approach is as follows:

* You increase **major** when you're making a *breaking change* to an API
* You increase **minor** when you're adding a new *feature* or *change* that isn't breaking, and is an addition to an API while maintaining backwards compatibility
* You use **patch** for *bug fixes* and incidental fixes

I tend to start from version **v0.0.1** (I'm still afraid of starting with **v1** it seems) and evolve from there.

The automated process I use runs in the following way:

1. The CI pipeline fires for a main branch build, detecting that it requires a release
2. The usual tests and builds are made to ensure stability
3. The current version is retrieved from the GitHub API
4. The release type is calculated by checking the commit messages between the last releases
5. This is used to calculate the next semantic version
6. The new version is pushed to GitHub and any packages are made and pushed, e.g. Docker images

### Get Current Version

This Groovy function takes in a repo (e.g. `jamiefdhurst/journal`), connects to the GitHub API to get the version, and returns a map of details to pass into the next step:

```groovy
def getVersion(String repo) {
    withCredentials([usernameColonPassword(credentialsId: 'github-personal-access-token', variable: 'GITHUB_API_TOKEN')]) {
        latestVersion = sh(
            script: 'curl --silent -u ' + GITHUB_API_TOKEN + ' "https://api.github.com/repos/' + repo + '/releases/latest" | grep \'"tag_name":\' | sed -E \'s/.*"([^"]+)".*/\\1/\'',
            returnStdout: true
        ).trim()
    }
    if (!latestVersion) {
        versionParts = [0]
        latestVersion = 'v0'
    } else {
        versionParts = latestVersion.tokenize('v')[0].tokenize('.')
    }
    major = versionParts[0].toInteger()
    try {
        minor = versionParts[1].toInteger()
    } catch (Exception e) {
        minor = 0
    }
    try {
        patch = versionParts[2].toInteger()
    } catch (Exception e) {
        patch = 0
    }

    return [full: latestVersion, major: major, minor: minor, patch: patch]
}
```

### Calculating the Release Type

Next, the release type is calculated using the commit messages in-between the last release and this one. Major takes precidence over minor, and minor over patch. These commit message sare captured and built into a changelog, and are scanned for keywords to determine the release:

```groovy
import groovy.json.JsonSlurperClassic

def calculateReleaseType(String repo, String latestVersion) {
    url = "https://api.github.com/repos/${repo}/commits"

    // Ensure support for a brand new repo with no current version
    if (lastVersion && lastVersion != 'v0') {
        url = "https://api.github.com/repos/${repo}/compare/${lastVersion}...HEAD"
    }
    withCredentials([usernameColonPassword(credentialsId: 'github-personal-access-token', variable: 'GITHUB_API_TOKEN')]) {
        responseJson = sh(script: "curl --silent -u ${GITHUB_API_TOKEN} '${url}'", returnStdout: true)
    }
    JsonSlurperClassic slurper = new JsonSlurperClassic()
    details = slurper.parseText(responseJson)

    // Parse the commits to find anything of value
    countMajorKeywords = 0
    countMinorKeywords = 0
    countSkips = 0
    commits = details.clone()
    if (!(details instanceof List)) {
        commits = details.commits.clone()
    }

    release = [changeLog: [], release: '']

    commits.each{ commit ->
        if (commit.commit.message.toLowerCase() =~ /^(break|release)/) {
            countMajorKeywords += 1
            release.changeLog.push(commit.commit.message)
        }
        if (commit.commit.message.toLowerCase() =~ /^(feature|new|add|update)/) {
            countMinorKeywords += 1
            release.changeLog.push(commit.commit.message)
        }
        if (commit.commit.message.toLowerCase() =~ /^(skip ci)/) {
            countSkips += 1
        }
    }

    if (countMajorKeywords) {
        release.release = 'major'
        return release
    }
    if (countMinorKeywords) {
        release.release = 'minor'
        return release
    }
    if (countSkips) {
        return release
    }
    release.release = 'patch'
    return release
}
```

A keep a provision for skipping a release if I'm generating a commit via CI, this might be to record a changelog for example, and generating a new version here would produce an infinite loop.

### Next Version

Now this release type is used to calculate the next version:

```groovy
def calculateNextVersion(Map version, String release) {
    switch (release) {
        case 'major':
            version.major += 1
            version.minor = 0
            version.patch = 0
            break;
        case 'minor':
            version.minor += 1
            version.patch = 0
            break;
        case 'patch':
            version.patch += 1
    }
    newVersion = 'v' + version.major.toString()
    if (version.minor > 0 || version.patch > 0) {
        newVersion = newVersion + '.' + version.minor.toString()
        if (version.patch > 0) {
            newVersion = newVersion + '.' + version.patch.toString()
        }
    }
    version.full = newVersion
    return version
```

### Building a Changelog and a Release

All of these utility functions are wrapped in a main release function that calls out where required, which can then be inserted into a Jenkinsfile:

```groovy
node {
    stage('Get Latest Version') {
        print 'Getting latest version for: ' + env.repository
        version = getVersion(env.repository)
        print 'Latest version is: ' + version.full
    }

    stage('Determine Next Version') {
        releaseDetails = calculateReleaseType(env.repository, version.full)
        release = releaseDetails.release
        print 'Releasing a ' + release + ' version'

        nextVersion = calculateNextVersion(version.clone(), release)
        print 'Calculated new version to be: ' + nextVersion.full

        releaseText = "Release ${nextVersion.full}"
        if (releaseDetails.changeLog.size()) {
            releaseText += ", including the following commits: \n- " + releaseDetails.changeLog.join("\n- ")
        }
    }
    stage('Checkout Code and Push Tag') {
        if (nextVersion.full != version.full) {
            print "Releasing ${nextVersion.full}..."

            releaseData = JsonOutput.toJson([
                tag_name: nextVersion.full,
                target_commitish: env.releaseBranch ?: 'main',
                name: nextVersion.full,
                body: releaseText,
                draft: false,
                prerelease: false
            ])

            print "Changelog: \n" + releaseText

            withCredentials([usernameColonPassword(credentialsId: 'github-personal-access-token', variable: 'GITHUB_API_TOKEN')]) {
                sh "curl -u $GITHUB_API_TOKEN -X POST -H 'Accept: application/vnd.github.v3+json' 'https://api.github.com/repos/${env.repository}/releases' -d '$releaseData'"
            }
        } else {
            print 'Not releasing, no new version has been calculated...'
        }
    }
    stage('Push Docker Image') {
        print "Pushing Docker image..."
        withCredentials([usernamePassword(credentialsId: 'github-personal-access-token', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]) {
            sh "docker login -u $GITHUB_USERNAME -p $GITHUB_PASSWORD ghcr.io"
            sh """
            docker tag ${env.dockerImage} ghcr.io/jamiefdhurst/${env.dockerImage}:latest
            docker tag ${env.dockerImage} ghcr.io/jamiefdhurst/${env.dockerImage}:${nextVersion.full}
            docker push ghcr.io/jamiefdhurst/${env.dockerImage}:latest
            docker push ghcr.io/jamiefdhurst/${env.dockerImage}:${nextVersion.full}
            """
        }
    }
}
```

### Putting It All Together

Finally, you can place it into your Jenkinsfile, such as the one used within this blog:

```groovy
pipeline {
    agent any

    stages {
        stage('Build and Test') {
            // ...
        }

        stage('Package and Release') {
            when {
                branch 'main'
            }
            steps {
                sh "docker build -t blog -f Dockerfile ."
                build job: '/github/blog-folder/release', wait: true
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                build job: '/github/blog-folder/deploy', wait: true, parameters: [
                    string(name: 'targetVersion', value: getVersion(repo: 'jamiefdhurst/blog').full)
                ]
            }
        }
    }
}
```
