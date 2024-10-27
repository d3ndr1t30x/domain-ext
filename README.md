Python script that reads a list of URLs from a .txt file, extracts the domain name of each URL, and writes the domain names to a new .txt file:

Random User-Agent: The script now picks a random User-Agent from the USER_AGENTS list for each request to make it seem like the requests are coming from different browsers and devices.
Random Delay: After each URL is processed, the script waits for a random amount of time (between 2 to 5 seconds) before making the next request. This helps to simulate human browsing behavior and avoid detection by anti-bot systems.

Example Usage:

When running the script, you'll be prompted to input the filenames:

```Enter the input .txt filename (with path if needed): urls.txt```
```Enter the output .txt filename (with path if needed): domains.txt```

The script will process the URLs from urls.txt, follow redirects, and append the domains to domains.txt. 
It will pause for a random interval between each request to avoid rate-limiting or blocking.
