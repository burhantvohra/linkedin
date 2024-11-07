LinkedIn Automation Script
Code Flow Overview
This script automates interactions on LinkedIn, such as logging in, liking, commenting, and reposting on posts. Below is an overview of the main code flow:

1. Connection Verification
Ensure an active internet connection before running the script.
Continuously monitor the connection to prevent interruptions.
2. Login Process
New Users: Perform a fresh login and save cookies for future sessions.
Returning Users: Authenticate using previously saved cookies for a faster login process.
3. Main Loop
Start each iteration by checking for an internet connection.
Save each post link to Link.txt for reference.
For each post, perform the required actions (like, comment, repost), then move to the next post.
When reaching the last post on the page, scroll down to load more posts and repeat the process.
Periodically check the internet connection and, every 2 minutes, pause the script for 1 minute before resuming the loop.
